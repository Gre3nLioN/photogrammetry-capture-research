import json
from pathlib import Path

import pytest

from photogrammetry_capture_research.experiments import (
    ExperimentError,
    compare_experiment,
    create_manifest,
    select_images,
    trajectory_sectors,
    write_experiment,
)


def quality_report(ids: list[str]) -> dict:
    per_image = [{"id": image_id, "name": f"frame-{image_id}.jpg"} for image_id in ids]
    diagnostics = {
        "registration": {"registration_ratio": 1.0},
        "reprojection_error_px": {"p95": 1.0},
        "tracks": {"median_length": 5},
        "view_angle_degrees": {"median": 10.0},
    }
    return {
        "report_type": "photogrammetry-quality-report",
        "dataset": {"source_fingerprint_sha256": "a" * 64},
        "input_image_health": {"per_image": per_image},
        "reconstruction_quality": {
            "diagnostics": diagnostics,
            "coverage": {"coverage_sector_ratio": 1.0},
            "scene_stats": {"sparse_points": 100},
        },
        "verdict": {"status": "good", "checks": [{"metric": "registration_ratio", "passed": True}]},
    }


def write_json(path: Path, value: dict) -> Path:
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_stride_manifest_is_deterministic(tmp_path: Path) -> None:
    baseline = write_json(tmp_path / "baseline.json", quality_report(["0", "1", "2", "3", "4"]))

    manifest = create_manifest(
        experiment_id="stride-2", baseline_path=baseline, strategy="stride", every=2
    )

    assert manifest["selection"]["selected_image_ids"] == ["0", "2", "4"]
    assert manifest["selection"]["excluded_image_ids"] == ["1", "3"]
    assert len(manifest["subset_fingerprint_sha256"]) == 64


def test_random_selection_requires_seed(tmp_path: Path) -> None:
    baseline = write_json(tmp_path / "baseline.json", quality_report(["0", "1", "2"]))

    with pytest.raises(ExperimentError, match="explicit --seed"):
        create_manifest(experiment_id="random", baseline_path=baseline, strategy="random", count=2)


def test_sector_removal_preserves_budget_and_removes_pca_sector() -> None:
    images = [{"id": str(index), "name": f"frame-{index}.jpg"} for index in range(8)]
    scene = {
        "cameras": [
            {"image_id": str(index), "center": [float(index % 4), float(index // 4), 0.0]}
            for index in range(8)
        ]
    }
    sector_by_id, _ = trajectory_sectors(scene)
    removed = next(iter(sector_by_id.values()))

    selected, parameters = select_images(
        images, "sector-removal", count=4, sectors=(removed,), scene=scene
    )

    assert len(selected) == 4
    assert all(sector_by_id[item["id"]] != removed for item in selected)
    assert parameters["removed_sectors"] == [removed]


def test_uneven_cadence_keeps_requested_budget() -> None:
    images = [{"id": str(index), "name": f"frame-{index}.jpg"} for index in range(20)]

    selected, parameters = select_images(images, "uneven-cadence", count=8, profile="burst-middle")

    assert len(selected) == 8
    assert parameters["burst_selected_count"] == 4


def test_compare_rejects_manifest_image_mismatch(tmp_path: Path) -> None:
    baseline = write_json(tmp_path / "baseline.json", quality_report(["0", "1", "2", "3"]))
    manifest = create_manifest(
        experiment_id="stride-2", baseline_path=baseline, strategy="stride", every=2
    )
    directory = write_experiment(manifest, tmp_path / "experiments")
    wrong_report = write_json(tmp_path / "wrong.json", quality_report(["0", "1"]))

    with pytest.raises(ExperimentError, match="manifest_mismatch"):
        compare_experiment(directory, wrong_report)
