from __future__ import annotations

import hashlib
import json
import random
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class ExperimentError(ValueError):
    """Raised when an experiment cannot be created or compared reproducibly."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ExperimentError(f"Cannot read JSON file {path}: {error}") from error
    if not isinstance(payload, dict):
        raise ExperimentError(f"JSON root must be an object: {path}")
    return payload


def stable_hash(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def baseline_images(report: dict[str, Any]) -> list[dict[str, str]]:
    try:
        records = report["input_image_health"]["per_image"]
    except (KeyError, TypeError) as error:
        raise ExperimentError(
            "Baseline is not a ReconCheck Quality Report with per-image records"
        ) from error
    images = [{"id": str(item["id"]), "name": str(item["name"])} for item in records]
    if not images or len({item["id"] for item in images}) != len(images):
        raise ExperimentError("Baseline image IDs are missing or not unique")
    return images


def select_images(
    images: list[dict[str, str]],
    strategy: str,
    *,
    every: int | None = None,
    count: int | None = None,
    seed: int | None = None,
    sector: int | None = None,
    scene: dict[str, Any] | None = None,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    if strategy == "stride":
        if every is None or every < 1:
            raise ExperimentError("Stride selection requires --every >= 1")
        return images[::every], {"every": every}
    if strategy == "random":
        if count is None or not 1 <= count <= len(images):
            raise ExperimentError(f"Random selection requires --count between 1 and {len(images)}")
        if seed is None:
            raise ExperimentError("Random selection requires an explicit --seed")
        chosen = sorted(random.Random(seed).sample(images, count), key=lambda item: item["name"])
        return chosen, {"count": count, "seed": seed}
    if strategy == "sector-removal":
        if scene is None or sector is None or not 0 <= sector < 8:
            raise ExperimentError("Sector removal requires --scene and --sector 0 through 7")
        cameras = scene.get("cameras", [])
        if not cameras:
            raise ExperimentError("Scene manifest has no registered cameras for sector removal")
        centers = [camera["center"] for camera in cameras]
        centroid = [sum(center[index] for center in centers) / len(centers) for index in range(2)]
        removed_ids = set()
        for camera in cameras:
            dx, dy = camera["center"][0] - centroid[0], camera["center"][1] - centroid[1]
            angle = __import__("math").atan2(dy, dx)
            camera_sector = (
                int((angle + __import__("math").pi) / (2 * __import__("math").pi) * 8) % 8
            )
            if camera_sector == sector:
                removed_ids.add(str(camera["image_id"]))
        selected = [image for image in images if image["id"] not in removed_ids]
        if not selected:
            raise ExperimentError(f"Sector {sector} removes every image")
        return selected, {
            "removed_sectors": [sector],
            "sector_count": 8,
            "removed_image_count": len(removed_ids),
        }
    raise ExperimentError(f"Unsupported selection strategy: {strategy}")


def create_manifest(
    *,
    experiment_id: str,
    baseline_path: Path,
    strategy: str,
    every: int | None = None,
    count: int | None = None,
    seed: int | None = None,
    sector: int | None = None,
    scene_path: Path | None = None,
    hypothesis: str = "",
    transformations: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if not experiment_id.replace("-", "").isalnum() or experiment_id != experiment_id.lower():
        raise ExperimentError("Experiment ID must be lowercase alphanumeric kebab-case")
    baseline = load_json(baseline_path)
    if baseline.get("report_type") != "photogrammetry-quality-report":
        raise ExperimentError("Baseline must be a ReconCheck photogrammetry-quality-report")
    images = baseline_images(baseline)
    scene = load_json(scene_path) if scene_path else None
    selected, parameters = select_images(
        images, strategy, every=every, count=count, seed=seed, sector=sector, scene=scene
    )
    selected_ids = [item["id"] for item in selected]
    excluded_ids = [item["id"] for item in images if item["id"] not in set(selected_ids)]
    baseline_fingerprint = str(baseline["dataset"]["source_fingerprint_sha256"])
    transformation_list = transformations or []
    subset_fingerprint = stable_hash(
        {
            "baseline": baseline_fingerprint,
            "selected_ids": selected_ids,
            "transformations": transformation_list,
        }
    )
    return {
        "schema_version": 1,
        "experiment_id": experiment_id,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "protocol": "01-coverage-and-frame-rate",
        "hypothesis": hypothesis,
        "baseline": {
            "quality_report": str(baseline_path.resolve()),
            "dataset_fingerprint_sha256": baseline_fingerprint,
        },
        "source_images": [item["name"] for item in images],
        "selection": {
            "strategy": strategy,
            "parameters": parameters,
            "selected_image_ids": selected_ids,
            "selected_image_names": [item["name"] for item in selected],
            "excluded_image_ids": excluded_ids,
            "excluded_image_names": [
                item["name"] for item in images if item["id"] in set(excluded_ids)
            ],
        },
        "transformations": transformation_list,
        "subset_fingerprint_sha256": subset_fingerprint,
        "repetitions": [{"id": f"{experiment_id}-r1", "seed": seed}],
    }


def write_experiment(manifest: dict[str, Any], output_root: Path) -> Path:
    directory = output_root / str(manifest["experiment_id"])
    if directory.exists():
        raise ExperimentError(f"Experiment directory already exists: {directory}")
    directory.mkdir(parents=True)
    (directory / "experiment-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    execution = {
        "schema_version": 1,
        "status": "pending",
        "note": (
            "Record the immutable reconstruction recipe, tool versions, timings, and "
            "output paths after reconstruction."
        ),
    }
    (directory / "execution.json").write_text(
        json.dumps(execution, indent=2) + "\n", encoding="utf-8"
    )
    return directory


def nested(payload: dict[str, Any], *keys: str) -> Any:
    value: Any = payload
    for key in keys:
        value = value[key]
    return value


def compare_experiment(experiment_dir: Path, quality_report_path: Path) -> dict[str, Any]:
    manifest = load_json(experiment_dir / "experiment-manifest.json")
    baseline = load_json(Path(str(manifest["baseline"]["quality_report"])))
    experiment = load_json(quality_report_path)
    if experiment.get("report_type") != "photogrammetry-quality-report":
        raise ExperimentError(
            "Experiment report must be a ReconCheck photogrammetry-quality-report"
        )
    expected = set(manifest["selection"].get("selected_image_names", []))
    if not expected:
        raise ExperimentError("Manifest has no stable selected_image_names")
    actual = {str(item["name"]) for item in experiment["input_image_health"]["per_image"]}
    if expected != actual:
        missing, unexpected = sorted(expected - actual), sorted(actual - expected)
        raise ExperimentError(
            f"manifest_mismatch: missing={missing[:5]}, unexpected={unexpected[:5]}"
        )
    metrics = [
        (
            "registration_ratio",
            ("reconstruction_quality", "diagnostics", "registration", "registration_ratio"),
        ),
        (
            "reprojection_p95_px",
            ("reconstruction_quality", "diagnostics", "reprojection_error_px", "p95"),
        ),
        (
            "median_track_length",
            ("reconstruction_quality", "diagnostics", "tracks", "median_length"),
        ),
        (
            "median_view_angle_deg",
            ("reconstruction_quality", "diagnostics", "view_angle_degrees", "median"),
        ),
        ("coverage_sector_ratio", ("reconstruction_quality", "coverage", "coverage_sector_ratio")),
        ("sparse_point_count", ("reconstruction_quality", "scene_stats", "sparse_points")),
    ]
    comparison_metrics = []
    for name, path in metrics:
        baseline_value = nested(baseline, *path)
        experiment_value = nested(experiment, *path)
        comparison_metrics.append(
            {
                "name": name,
                "baseline": baseline_value,
                "experiment": experiment_value,
                "absolute_delta": experiment_value - baseline_value,
                "relative_delta": (experiment_value - baseline_value) / baseline_value
                if baseline_value
                else None,
            }
        )
    baseline_checks = {item["metric"]: item["passed"] for item in baseline["verdict"]["checks"]}
    experiment_checks = {item["metric"]: item["passed"] for item in experiment["verdict"]["checks"]}
    transitions = [
        {
            "metric": name,
            "baseline": passed,
            "experiment": experiment_checks.get(name),
            "changed": passed != experiment_checks.get(name),
        }
        for name, passed in baseline_checks.items()
    ]
    failed = [item["metric"] for item in transitions if item["baseline"] and not item["experiment"]]
    execution_path = experiment_dir / "execution.json"
    execution = load_json(execution_path) if execution_path.is_file() else {}
    stages = execution.get("stages", {})
    duration = sum(float(stage.get("duration_seconds", 0.0)) for stage in stages.values())
    derived_bytes = sum(
        path.stat().st_size
        for path in experiment_dir.rglob("*")
        if path.is_file() and not path.is_symlink()
    )
    conclusion = (
        f"The condition changed the quality verdict from {baseline['verdict']['status']} "
        f"to {experiment['verdict']['status']}; failed requirements: {', '.join(failed)}."
        if failed
        else f"The condition retained the {experiment['verdict']['status']} quality verdict."
    )
    return {
        "schema_version": 1,
        "experiment_id": manifest["experiment_id"],
        "baseline_fingerprint_sha256": manifest["baseline"]["dataset_fingerprint_sha256"],
        "experiment_fingerprint_sha256": experiment["dataset"]["source_fingerprint_sha256"],
        "quality_transition": {
            "baseline": baseline["verdict"]["status"],
            "experiment": experiment["verdict"]["status"],
            "checks": transitions,
        },
        "metrics": comparison_metrics,
        "execution": {
            "status": execution.get("status", "not recorded"),
            "total_stage_duration_seconds": duration,
            "derived_storage_bytes": derived_bytes,
            "stages": {
                name: {
                    "exit_code": stage.get("exit_code"),
                    "duration_seconds": stage.get("duration_seconds"),
                }
                for name, stage in stages.items()
            },
        },
        "conclusion": conclusion,
        "limitations": [
            "Internal reconstruction consistency is not absolute geometric accuracy.",
            "This condition must be interpreted with its recorded reconstruction recipe "
            "and repetitions.",
        ],
    }


def write_comparison(experiment_dir: Path, quality_report_path: Path) -> Path:
    comparison = compare_experiment(experiment_dir, quality_report_path)
    target = experiment_dir / "comparison.json"
    target.write_text(json.dumps(comparison, indent=2) + "\n", encoding="utf-8")
    quality_target = experiment_dir / "reconcheck-quality-report.json"
    quality_target.write_text(quality_report_path.read_text(encoding="utf-8"), encoding="utf-8")
    changed_checks = [
        item["metric"] for item in comparison["quality_transition"]["checks"] if item["changed"]
    ]
    report = "\n".join(
        [
            f"# {comparison['experiment_id']}",
            "",
            "## Quality transition",
            "",
            f"- Baseline: **{comparison['quality_transition']['baseline']}**",
            f"- Experiment: **{comparison['quality_transition']['experiment']}**",
            f"- Changed checks: {', '.join(changed_checks) if changed_checks else 'none'}",
            "",
            "## Conclusion",
            "",
            str(comparison["conclusion"]),
            "",
            "## Execution",
            "",
            f"- Status: `{comparison['execution']['status']}`",
            "- Total stage duration: "
            f"{comparison['execution']['total_stage_duration_seconds']:.1f} seconds",
            f"- Derived storage: {comparison['execution']['derived_storage_bytes']:,} bytes",
            "",
            "## Limitations",
            "",
            *[f"- {value}" for value in comparison["limitations"]],
            "",
        ]
    )
    (experiment_dir / "report.md").write_text(report, encoding="utf-8")
    return target
