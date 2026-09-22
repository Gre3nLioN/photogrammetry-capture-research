from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from reconcheck.analysis import analyze_project
from reconcheck.project import discover_project

from photogrammetry_capture_research.experiments import ExperimentError, write_comparison


def now() -> str:
    return datetime.now(UTC).isoformat()


def load_manifest(experiment: Path) -> dict[str, Any]:
    return json.loads((experiment / "experiment-manifest.json").read_text(encoding="utf-8"))


def materialize_links(experiment: Path, source_images: Path, names: list[str]) -> Path:
    target = experiment / "derived/images"
    if target.exists():
        existing = sorted(
            path.relative_to(target).as_posix()
            for path in target.rglob("*")
            if path.is_file() or path.is_symlink()
        )
        if existing != sorted(names):
            raise ExperimentError(
                f"Existing derived image directory does not match manifest: {target}"
            )
        return target
    target.mkdir(parents=True)
    for name in names:
        source = (source_images / name).resolve()
        if not source.is_file():
            raise ExperimentError(f"Manifest source image is missing: {source}")
        link = target / name
        link.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(source, link)
    return target


def run_stage(command: list[str], log_path: Path) -> dict[str, Any]:
    started = now()
    timer = time.monotonic()
    with log_path.open("w", encoding="utf-8") as log:
        log.write("$ " + " ".join(command) + "\n\n")
        completed = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
    return {
        "command": command,
        "started_at_utc": started,
        "finished_at_utc": now(),
        "duration_seconds": round(time.monotonic() - timer, 3),
        "exit_code": completed.returncode,
        "log": str(log_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a derived COLMAP experiment without modifying raw inputs"
    )
    parser.add_argument("--experiment", type=Path, required=True)
    parser.add_argument("--source-images", type=Path, required=True)
    parser.add_argument("--gpu-index", default="0")
    args = parser.parse_args()
    experiment = args.experiment.resolve()
    source_images = args.source_images.resolve()
    manifest = load_manifest(experiment)
    previous_execution = (
        json.loads((experiment / "execution.json").read_text(encoding="utf-8"))
        if (experiment / "execution.json").is_file()
        else {"stages": {}}
    )
    names = list(manifest["selection"]["selected_image_names"])
    images = materialize_links(experiment, source_images, names)
    colmap_root = experiment / "colmap"
    logs = experiment / "logs"
    colmap_root.mkdir(exist_ok=True)
    logs.mkdir(exist_ok=True)
    sparse_root = colmap_root / "sparse"
    sparse_root.mkdir(exist_ok=True)
    dense_root = colmap_root / "dense"
    database = colmap_root / "database.db"
    sparse_model = sparse_root / "0"
    commands = [
        (
            "feature-extractor",
            [
                "colmap",
                "feature_extractor",
                "--database_path",
                str(database),
                "--image_path",
                str(images),
                "--ImageReader.single_camera",
                "1",
                "--FeatureExtraction.use_gpu",
                "1",
                "--FeatureExtraction.gpu_index",
                args.gpu_index,
            ],
        ),
        (
            "exhaustive-matcher",
            [
                "colmap",
                "exhaustive_matcher",
                "--database_path",
                str(database),
                "--FeatureMatching.use_gpu",
                "1",
                "--FeatureMatching.gpu_index",
                args.gpu_index,
            ],
        ),
        (
            "mapper",
            [
                "colmap",
                "mapper",
                "--database_path",
                str(database),
                "--image_path",
                str(images),
                "--output_path",
                str(sparse_root),
            ],
        ),
        (
            "image-undistorter",
            [
                "colmap",
                "image_undistorter",
                "--image_path",
                str(images),
                "--input_path",
                str(sparse_model),
                "--output_path",
                str(dense_root),
                "--output_type",
                "COLMAP",
                "--copy_policy",
                "SOFT_LINK",
                "--max_image_size",
                "1200",
            ],
        ),
        (
            "patch-match-stereo",
            [
                "colmap",
                "patch_match_stereo",
                "--workspace_path",
                str(dense_root),
                "--workspace_format",
                "COLMAP",
                "--PatchMatchStereo.gpu_index",
                args.gpu_index,
            ],
        ),
        (
            "stereo-fusion",
            [
                "colmap",
                "stereo_fusion",
                "--workspace_path",
                str(dense_root),
                "--workspace_format",
                "COLMAP",
                "--output_path",
                str(dense_root / "fused.ply"),
                "--StereoFusion.max_image_size",
                "1200",
            ],
        ),
        (
            "poisson-mesher",
            [
                "colmap",
                "poisson_mesher",
                "--input_path",
                str(dense_root / "fused.ply"),
                "--output_path",
                str(dense_root / "mesh.ply"),
            ],
        ),
    ]
    execution: dict[str, Any] = {
        "schema_version": 1,
        "status": "running",
        "started_at_utc": now(),
        "software": {
            "colmap_version": subprocess.check_output(["colmap", "--version"], text=True).strip(),
            "python": sys.version,
            "platform": platform.platform(),
        },
        "inputs": {
            "source_images": str(source_images),
            "derived_images": str(images),
            "selected_image_count": len(names),
            "subset_fingerprint_sha256": manifest["subset_fingerprint_sha256"],
        },
        "stages": {},
    }
    (experiment / "execution.json").write_text(
        json.dumps(execution, indent=2) + "\n", encoding="utf-8"
    )
    for index, (name, command) in enumerate(commands):
        previous_stage = previous_execution.get("stages", {}).get(name, {})
        if index < 2 and previous_stage.get("exit_code") == 0 and database.is_file():
            execution["stages"][name] = {**previous_stage, "reused_from_previous_attempt": True}
            continue
        if index == 3 and not sparse_model.is_dir():
            execution["status"] = "failed_sparse"
            execution["failure"] = "Mapper did not create sparse/0"
            break
        result = run_stage(command, logs / f"{name}.log")
        execution["stages"][name] = result
        (experiment / "execution.json").write_text(
            json.dumps(execution, indent=2) + "\n", encoding="utf-8"
        )
        if result["exit_code"] != 0:
            execution["status"] = "failed_sparse" if index < 3 else "incomplete_dense"
            execution["failure"] = f"{name} exited with {result['exit_code']}"
            break
    else:
        execution["status"] = "complete"
    if sparse_model.is_dir():
        dense_cloud = dense_root / "fused.ply"
        mesh = dense_root / "mesh.ply"
        project = discover_project(
            experiment,
            images=images,
            sparse=sparse_model,
            database=database,
            dense=dense_cloud if dense_cloud.is_file() else None,
            mesh=mesh if mesh.is_file() else None,
        )
        cache = analyze_project(project, refresh=True)
        quality_report = cache / "quality-report.json"
        write_comparison(experiment, quality_report)
        execution["reconcheck_cache"] = str(cache)
        execution["quality_report"] = str(experiment / "reconcheck-quality-report.json")
    execution["finished_at_utc"] = now()
    (experiment / "execution.json").write_text(
        json.dumps(execution, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Experiment status: {execution['status']}")
    return 0 if sparse_model.is_dir() else 1


if __name__ == "__main__":
    raise SystemExit(main())
