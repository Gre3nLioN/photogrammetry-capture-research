from __future__ import annotations

import hashlib
import json
import random
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np


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


def evenly_sample(images: list[dict[str, str]], count: int) -> list[dict[str, str]]:
    if not 1 <= count <= len(images):
        raise ExperimentError(f"Selection count must be between 1 and {len(images)}")
    indexes = [(index * len(images)) // count for index in range(count)]
    return [images[index] for index in indexes]


def trajectory_sectors(scene: dict[str, Any]) -> tuple[dict[str, int], dict[str, object]]:
    cameras = scene.get("cameras", [])
    if not cameras:
        raise ExperimentError("Scene manifest has no registered cameras")
    centers = np.asarray([camera["center"] for camera in cameras], dtype=float)
    centroid = centers.mean(axis=0)
    _, _, basis = np.linalg.svd(centers - centroid, full_matrices=False)
    plane_basis = basis[:2]
    coordinates = (centers - centroid) @ plane_basis.T
    angles = np.arctan2(coordinates[:, 1], coordinates[:, 0])
    sectors = ((angles + np.pi) / (2 * np.pi) * 8).astype(int) % 8
    mapping = {
        str(camera["name"]): int(sector) for camera, sector in zip(cameras, sectors, strict=True)
    }
    definition = {
        "method": "eight azimuthal sectors in the first two PCA axes of registered camera centers",
        "sector_count": 8,
        "centroid": centroid.tolist(),
        "plane_basis": plane_basis.tolist(),
    }
    return mapping, definition


def select_images(
    images: list[dict[str, str]],
    strategy: str,
    *,
    every: int | None = None,
    count: int | None = None,
    seed: int | None = None,
    sectors: tuple[int, ...] = (),
    gap_start: int | None = None,
    gap_count: int | None = None,
    profile: str | None = None,
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
        if scene is None or not sectors or any(not 0 <= sector < 8 for sector in sectors):
            raise ExperimentError("Sector removal requires --scene and --sectors in 0 through 7")
        if count is None:
            raise ExperimentError("Sector removal requires --count to preserve image budget")
        sector_by_id, definition = trajectory_sectors(scene)
        candidates = [
            image for image in images if sector_by_id.get(image["name"]) not in set(sectors)
        ]
        selected = evenly_sample(candidates, count)
        return selected, {
            "removed_sectors": list(sectors),
            "candidate_count": len(candidates),
            "sampling": "even-over-retained-trajectory",
            "sector_definition": definition,
        }
    if strategy == "contiguous-gap":
        if count is None or gap_start is None or gap_count is None or gap_count < 1:
            raise ExperimentError("Contiguous gap requires --count, --gap-start, and --gap-count")
        if not 0 <= gap_start < len(images) or gap_start + gap_count > len(images):
            raise ExperimentError("Contiguous gap is outside the ordered source-image range")
        candidates = images[:gap_start] + images[gap_start + gap_count :]
        return evenly_sample(candidates, count), {
            "gap_start": gap_start,
            "gap_count": gap_count,
            "candidate_count": len(candidates),
            "sampling": "even-over-retained-trajectory",
        }
    if strategy == "uneven-cadence":
        if count is None or profile not in {"burst-start", "burst-middle", "burst-end"}:
            raise ExperimentError(
                "Uneven cadence requires --count and a burst-start, burst-middle, "
                "or burst-end profile"
            )
        span = max(1, len(images) // 5)
        offsets = {
            "burst-start": 0,
            "burst-middle": (len(images) - span) // 2,
            "burst-end": len(images) - span,
        }
        start = offsets[profile]
        burst = images[start : start + span]
        burst_count = min(len(burst), count // 2)
        remaining = images[:start] + images[start + span :]
        selected = evenly_sample(burst, burst_count) + evenly_sample(remaining, count - burst_count)
        return sorted(selected, key=lambda image: images.index(image)), {
            "profile": profile,
            "burst_window_start": start,
            "burst_window_count": span,
            "burst_selected_count": burst_count,
            "sampling": "half-budget-in-one-fifth-of-route",
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
    sectors: tuple[int, ...] = (),
    gap_start: int | None = None,
    gap_count: int | None = None,
    profile: str | None = None,
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
        images,
        strategy,
        every=every,
        count=count,
        seed=seed,
        sectors=sectors,
        gap_start=gap_start,
        gap_count=gap_count,
        profile=profile,
        scene=scene,
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


def compare_experiment(
    experiment_dir: Path,
    quality_report_path: Path,
    reference_experiment: Path | None = None,
) -> dict[str, Any]:
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
    if reference_experiment is None:
        candidate = Path(str(manifest["baseline"]["quality_report"])).parent
        reference_experiment = (
            candidate if (candidate / "colmap/dense/fused.ply").is_file() else None
        )
    if reference_experiment is None:
        completeness: dict[str, Any] = {
            "status": "unavailable",
            "scope": "No controlled dense-reference experiment was provided.",
        }
    else:
        from photogrammetry_capture_research.completeness import evaluate_dense_completeness

        completeness = evaluate_dense_completeness(reference_experiment, experiment_dir)
    internal_verdict = str(experiment["verdict"]["status"])
    completeness_status = completeness["status"]
    task_verdict = (
        "poor"
        if completeness_status == "incomplete"
        else "warning"
        if completeness_status == "partially_complete"
        else internal_verdict
        if completeness_status == "complete"
        else "unverified"
    )
    internal_conclusion = (
        f"Internal consistency changed from {baseline['verdict']['status']} to {internal_verdict}; "
        f"failed requirements: {', '.join(failed)}."
        if failed
        else f"Internal consistency retained the {internal_verdict} verdict."
    )
    conclusion = (
        f"{internal_conclusion} Complete-object task verdict: {task_verdict} "
        f"({completeness_status} reference completeness)."
    )
    return {
        "schema_version": 1,
        "experiment_id": manifest["experiment_id"],
        "baseline_fingerprint_sha256": manifest["baseline"]["dataset_fingerprint_sha256"],
        "experiment_fingerprint_sha256": experiment["dataset"]["source_fingerprint_sha256"],
        "quality_transition": {
            "baseline": baseline["verdict"]["status"],
            "experiment": internal_verdict,
            "checks": transitions,
        },
        "reference_completeness": completeness,
        "task_verdict": task_verdict,
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


def write_comparison(
    experiment_dir: Path,
    quality_report_path: Path,
    reference_experiment: Path | None = None,
) -> Path:
    comparison = compare_experiment(experiment_dir, quality_report_path, reference_experiment)
    target = experiment_dir / "comparison.json"
    target.write_text(json.dumps(comparison, indent=2) + "\n", encoding="utf-8")
    quality_target = experiment_dir / "reconcheck-quality-report.json"
    quality_target.write_text(quality_report_path.read_text(encoding="utf-8"), encoding="utf-8")
    changed_checks = [
        item["metric"] for item in comparison["quality_transition"]["checks"] if item["changed"]
    ]
    completeness = comparison["reference_completeness"]
    largest_missing = completeness.get("largest_missing_component", {})
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
            "## Reference Completeness",
            "",
            f"- Status: **{completeness['status']}**",
            f"- Complete-object task verdict: **{comparison['task_verdict']}**",
            *(
                [
                    f"- Reference-surface recall: {completeness['reference_surface_recall']:.1%}",
                    "- Missing reference surface: "
                    f"{completeness['missing_reference_surface_fraction']:.1%}",
                    f"- Distance tolerance: {completeness['distance_tolerance']:.4f}",
                    "- Largest connected missing region: "
                    f"{largest_missing['reference_surface_fraction']:.1%} of reference surface, "
                    f"spanning {largest_missing['bounding_box_diagonal']:.2f}",
                ]
                if completeness["status"] != "unavailable"
                else [f"- Note: {completeness['scope']}"]
            ),
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
