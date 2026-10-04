---
title: Helenenschacht Alignment Sensitivity
type: synthesis
tags: [work, photogrammetry, validation, sensitivity]
created: 2026-10-03
updated: 2026-10-04
sources: [Helenenschacht full and stride-2 derived reconstructions]
---

# Helenenschacht Alignment Sensitivity

Read-only diagnostics show that the external check's fine occupancy score is strongly dependent on residual alignment, while remaining below acceptance thresholds under the tested refinement.

## Key Points

- Frozen camera-aligned recall: 70.64%; normalized fine occupancy: 3.62%.
- Five tested grid phases produced 3.45–3.62% occupancy: grid-origin choice alone does not explain the score.
- Diagnostic rigid surface refinement raised recall to 83.79% and fine occupancy to 51.33%.
- The original 3.62% score cannot be interpreted as pure loss of geometric detail.
- Surface refinement is exploratory, not a replacement evaluation or ground-truth alignment.

## Details

### Inputs and frozen evaluation

The full `helenenschacht-colmap-v1` and reduced `helenenschacht-stride-2-lite` reconstructions were read without modification. The existing evaluator's camera-center similarity alignment, sampling caps, and thresholds were retained for the frozen result.

- Shared cameras: 87.
- Fine voxel width: 0.0541695 scene units.
- Frozen distance tolerance: 0.1083390 scene units.
- Camera residual median / P95 / maximum: 0.04258 / 0.07885 / 0.12270.
- Surface nearest-neighbor distance median / P90 / P95: 0.10270 / 0.27273 / 0.57875.

### Grid-phase test

Offsets are fractions of fine voxel width and were applied equally to the reference sample, reference sampling ceiling, and aligned subset.

| Phase (x, y, z) | Normalized fine occupancy |
|---|---:|
| (0, 0, 0) | 3.619% |
| (0.5, 0, 0) | 3.576% |
| (0, 0.5, 0) | 3.584% |
| (0, 0, 0.5) | 3.603% |
| (0.5, 0.5, 0.5) | 3.454% |

### Distance-tolerance test

With the camera alignment unchanged, recall was 4.51%, 70.64%, 85.25%, and 88.09% at 0.5×, 1×, 1.5×, and 2× the frozen tolerance, respectively. These are diagnostics, not retuned thresholds.

### Exploratory rigid surface refinement

Starting from the camera-aligned cloud, run 20 nearest-neighbor rigid refinement iterations against the deterministic reference sample. Use every eighth point of the sampled subset for fitting, reject correspondences beyond twice the frozen tolerance, then trim the highest 20% of remaining distances. Estimate rotation and translation by SVD without further scale changes. Apply each update to the complete sampled subset and aligned camera centers. Re-evaluate using the original tolerance and fine voxel width.

| Metric | Frozen camera alignment | Diagnostic surface refinement |
|---|---:|---:|
| Reference recall | 70.64% | 83.79% |
| Normalized fine occupancy | 3.62% | 51.33% |
| Median surface distance | 0.10270 | 0.00803 |
| Camera-center RMSE | 0.04859 | 0.11952 |

The refined recall remains below the 97% completeness requirement and occupancy remains below the 60% poor/degraded boundary. The largest missing-component metric was not recomputed for this diagnostic. Recall alone is sufficient to fail the complete-object rule.

## Interpretation and Limitations

Substantial alignment-dependent variation prevents attributing the original occupancy score solely to detail loss. Reference recall also combines absent geometry and geometric disagreement. The surface refinement optimizes against the same reconstructed reference used for scoring, can favor dominant surfaces, and worsens camera agreement. Neither alignment is independently established as correct. Results support failure under both tested alignments, not a universal threshold or exact estimate of lost detail.

This check was executed interactively using existing evaluator helpers and NumPy/SciPy, then repeated to produce the figure below with identical aggregate results. In accordance with the report-only publication scope, no sensitivity script or test code is published. The sampling, fitting, and rendering procedures are documented here; broader alignment/initialization checks and independent verification remain outstanding.

### Visual findings

![Shared-projection overlays and reference-distance maps](../paper/figures/helenenschacht-alignment-overlays.png)

The figure uses one reference-derived PCA basis, common reference bounds, and equal aspect scales for both alignments. Rows show PC1/PC2 and PC1/PC3 projections; columns compare cloud overlays and reference-to-subset nearest-neighbor distances before and after refinement. Blue overlay points are the reference; orange points are the subset. Distance colors use fixed bands: blue ≤ fine voxel width, green ≤ frozen tolerance, amber ≤ twice that tolerance, red above twice the tolerance. Red denotes reference disagreement, not proven missing geometry.

Visual inspection shows the dominant near-planar surface becomes substantially better aligned after refinement, while peripheral and below-plane disagreement remains. This is consistent with the changed distance statistics but cannot separate missing geometry, scene differences, and local reconstruction errors. Two-dimensional projections can hide depth differences and are not independent ground truth.

The overlays display 24,000 equally spaced reference-sample indexes and 18,000 subset-sample indexes. The maps display the same reference indexes colored by distances computed against the complete sampled subset, with higher distances drawn last. The PCA basis is derived by SVD from every eighth reference-sample point, centered on the full reference sample; each basis-vector sign is fixed by making its largest-magnitude component positive.

The repeated refinement produced a centroid displacement of 0.10890 scene units. Its additional rigid translation, applied after camera alignment, was (-0.002235, 0.007740, 0.108873). These quantities are in arbitrary reconstruction units and should not be reported as metric survey distances.

## Related Pages

- [[external-validation-helenenschacht-lite]]
- [[literature-review]]
- [[manuscript]]

## Source Notes

Published frozen results remain unchanged in `helenenschacht-stride-2-completeness.json`. No new COLMAP reconstruction was run and no raw data was modified.
