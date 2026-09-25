from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pycolmap
from scipy.spatial import cKDTree

from photogrammetry_capture_research.experiments import ExperimentError

_MAX_REFERENCE_POINTS = 250_000
_MAX_EXPERIMENT_POINTS = 1_000_000


@dataclass(frozen=True)
class Similarity:
    scale: float
    rotation: np.ndarray
    translation: np.ndarray

    def transform(self, points: np.ndarray) -> np.ndarray:
        return self.scale * points @ self.rotation.T + self.translation


def _ply_vertex_positions(path: Path, limit: int) -> np.ndarray:
    with path.open("rb") as handle:
        header = bytearray()
        while b"end_header\n" not in header and b"end_header\r\n" not in header:
            line = handle.readline()
            if not line:
                raise ExperimentError(f"PLY header is incomplete: {path}")
            header.extend(line)
        offset = handle.tell()
    lines = header.decode("ascii").splitlines()
    if "format binary_little_endian 1.0" not in lines:
        raise ExperimentError(f"Only binary_little_endian PLY is supported: {path}")
    vertex_count = 0
    properties: list[tuple[str, str]] = []
    in_vertex = False
    for line in lines:
        tokens = line.split()
        if tokens[:2] == ["element", "vertex"]:
            vertex_count = int(tokens[2])
            in_vertex = True
        elif tokens[:1] == ["element"]:
            in_vertex = False
        elif in_vertex and tokens[:1] == ["property"] and len(tokens) == 3:
            properties.append((tokens[2], tokens[1]))
    scalar_types = {
        "char": "i1",
        "uchar": "u1",
        "short": "i2",
        "ushort": "u2",
        "int": "i4",
        "uint": "u4",
        "float": "f4",
        "double": "f8",
    }
    try:
        dtype = np.dtype([(name, f"<{scalar_types[type_name]}") for name, type_name in properties])
    except KeyError as error:
        raise ExperimentError(f"Unsupported PLY vertex property type in {path}: {error}") from error
    if not vertex_count or not {"x", "y", "z"}.issubset(dtype.names or ()):
        raise ExperimentError(f"PLY lacks vertex x/y/z properties: {path}")
    vertices = np.memmap(path, dtype=dtype, mode="r", offset=offset, shape=(vertex_count,))
    step = max(1, int(np.ceil(vertex_count / limit)))
    sampled = vertices[::step]
    return np.column_stack((sampled["x"], sampled["y"], sampled["z"])).astype(np.float64)


def _camera_centers(model: Path) -> dict[str, np.ndarray]:
    reconstruction = pycolmap.Reconstruction(str(model))
    return {
        image.name: np.asarray(image.projection_center(), dtype=np.float64)
        for image in reconstruction.images.values()
    }


def _similarity(source: np.ndarray, target: np.ndarray) -> Similarity:
    if len(source) < 3:
        raise ExperimentError("At least three shared registered cameras are required for alignment")
    source_mean, target_mean = source.mean(axis=0), target.mean(axis=0)
    source_centered, target_centered = source - source_mean, target - target_mean
    covariance = target_centered.T @ source_centered / len(source)
    left, singular_values, right_t = np.linalg.svd(covariance)
    correction = np.eye(3)
    if np.linalg.det(left) * np.linalg.det(right_t) < 0:
        correction[-1, -1] = -1
    rotation = left @ correction @ right_t
    source_variance = np.sum(source_centered * source_centered) / len(source)
    if source_variance == 0:
        raise ExperimentError("Shared camera centers have zero variance")
    scale = float(np.sum(singular_values * np.diag(correction)) / source_variance)
    return Similarity(scale, rotation, target_mean - scale * rotation @ source_mean)


def largest_missing_component(points: np.ndarray, cell_size: float) -> dict[str, float | int]:
    if not len(points):
        return {
            "reference_point_count": 0,
            "voxel_count": 0,
            "bounding_box_diagonal": 0.0,
        }
    voxel_keys, inverse, counts = np.unique(
        np.floor(points / cell_size).astype(np.int64),
        axis=0,
        return_inverse=True,
        return_counts=True,
    )
    lookup = {tuple(key): index for index, key in enumerate(voxel_keys)}
    visited: set[int] = set()
    largest: list[int] = []
    for start in range(len(voxel_keys)):
        if start in visited:
            continue
        component: list[int] = []
        pending = [start]
        visited.add(start)
        while pending:
            index = pending.pop()
            component.append(index)
            key = voxel_keys[index]
            for x_offset in (-1, 0, 1):
                for y_offset in (-1, 0, 1):
                    for z_offset in (-1, 0, 1):
                        neighbor = lookup.get(
                            (
                                int(key[0] + x_offset),
                                int(key[1] + y_offset),
                                int(key[2] + z_offset),
                            )
                        )
                        if neighbor is not None and neighbor not in visited:
                            visited.add(neighbor)
                            pending.append(neighbor)
        if not largest or counts[component].sum() > counts[largest].sum():
            largest = component
    component_keys = voxel_keys[largest]
    extent = (component_keys.max(axis=0) - component_keys.min(axis=0) + 1) * cell_size
    return {
        "reference_point_count": int(counts[largest].sum()),
        "voxel_count": len(largest),
        "bounding_box_diagonal": float(np.linalg.norm(extent)),
    }


def classify_completeness(recall: float, largest_component_fraction: float) -> str:
    if recall >= 0.97 and largest_component_fraction < 0.02:
        return "complete"
    if recall >= 0.95 and largest_component_fraction < 0.02:
        return "partially_complete"
    return "incomplete"


def evaluate_dense_completeness(reference_experiment: Path, experiment: Path) -> dict[str, Any]:
    reference_model = reference_experiment / "colmap/sparse/0"
    experiment_model = experiment / "colmap/sparse/0"
    reference_dense = reference_experiment / "colmap/dense/fused.ply"
    experiment_dense = experiment / "colmap/dense/fused.ply"
    for path in (reference_model, experiment_model, reference_dense, experiment_dense):
        if not path.exists():
            raise ExperimentError(f"Completeness reference asset is unavailable: {path}")
    reference_cameras, experiment_cameras = (
        _camera_centers(reference_model),
        _camera_centers(experiment_model),
    )
    shared_names = sorted(set(reference_cameras) & set(experiment_cameras))
    source = np.asarray([experiment_cameras[name] for name in shared_names])
    target = np.asarray([reference_cameras[name] for name in shared_names])
    alignment = _similarity(source, target)
    aligned_centers = alignment.transform(source)
    alignment_rmse = float(np.sqrt(np.mean(np.sum((aligned_centers - target) ** 2, axis=1))))
    reference_points = _ply_vertex_positions(reference_dense, _MAX_REFERENCE_POINTS)
    experiment_points = alignment.transform(
        _ply_vertex_positions(experiment_dense, _MAX_EXPERIMENT_POINTS)
    )
    diagonal = float(np.linalg.norm(reference_points.max(axis=0) - reference_points.min(axis=0)))
    tolerance = diagonal * 0.005
    distances, _ = cKDTree(experiment_points).query(reference_points, k=1, workers=-1)
    missing_points = reference_points[distances > tolerance]
    largest_component = largest_missing_component(missing_points, tolerance * 2)
    recall = float(np.mean(distances <= tolerance))
    largest_component_fraction = largest_component["reference_point_count"] / len(reference_points)
    return {
        "method": "dense-reference-recall-v1",
        "reference_experiment": str(reference_experiment.resolve()),
        "shared_camera_count": len(shared_names),
        "similarity_alignment": {
            "scale": alignment.scale,
            "camera_center_rmse": alignment_rmse,
        },
        "reference_point_sample_count": len(reference_points),
        "experiment_point_sample_count": len(experiment_points),
        "scene_diagonal": diagonal,
        "distance_tolerance": tolerance,
        "reference_surface_recall": recall,
        "missing_reference_surface_fraction": 1.0 - recall,
        "largest_missing_component": {
            **largest_component,
            "reference_surface_fraction": largest_component_fraction,
        },
        "status": classify_completeness(recall, largest_component_fraction),
        "scope": (
            "Dense-cloud recall against the controlled full-capture reference; it estimates "
            "completeness, not absolute geometric accuracy."
        ),
    }
