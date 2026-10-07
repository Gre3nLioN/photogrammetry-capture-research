---
title: Core Study Summary — Barn Capture Budget, Coverage, and Cadence
type: synthesis
tags: [life, work, photogrammetry, research]
created: 2026-10-07
updated: 2026-10-07
sources: [Barn experiment artifacts]
---

# Core Study Summary — Barn Capture Budget, Coverage, and Cadence

A descriptive ablation of image count and distribution under one fixed CUDA COLMAP recipe, using all 410 Barn images as a reconstructed reference.

## Objective

Compare internal screening, one-way dense-reference agreement, and spatial occupancy under deterministic capture reductions. This is not an actual phone-video study or a validated minimum-budget estimate.

## Evaluation

- **Completeness:** dense-reference surface recall after similarity alignment to the controlled baseline, plus the largest connected missing region.
- **Detail fidelity:** normalized fine-scale voxel occupancy against the controlled baseline.
- **Internal consistency:** ReconCheck's existing registration, reprojection, track, view-angle, dense, and mesh checks.
- Task verdicts combine completeness and detail; an internal `good` result alone is insufficient.

## Results

| Condition | Task | Completeness | Detail | Recall | Fine occupancy |
|---|---|---|---|---:|---:|
| Full controlled baseline | good | complete | preserved | 100.0% | 100.0% |
| Stride 3 / 33% | good | complete | preserved | 99.5% | 80.9% |
| Stride 4 / 25% | warning | complete | degraded | 98.4% | 69.9% |
| Stride 5 / 20% | warning | partial | degraded | 96.9% | 68.1% |
| Sector 0 omitted | warning | partial | degraded | 96.1% | 61.0% |
| Sector 3 omitted | warning | complete | degraded | 97.8% | 70.3% |
| Sector 6 omitted | warning | complete | degraded | 98.8% | 71.2% |
| Sectors 0–1 omitted | poor | incomplete | poor | 93.6% | 57.6% |
| Sectors 3–4 omitted | poor | incomplete | degraded | 88.8% | 69.0% |
| Sectors 6–7 omitted | warning | complete | degraded | 97.9% | 68.2% |
| Start route gap | warning | complete | degraded | 97.8% | 68.7% |
| Middle route gap | warning | complete | degraded | 98.1% | 69.4% |
| End route gap | warning | complete | degraded | 98.7% | 68.6% |
| Burst at start | poor | incomplete | poor | 29.4% | 3.6% |
| Burst in middle | warning | partial | degraded | 96.8% | 66.2% |
| Burst at end | poor | incomplete | degraded | 94.7% | 62.4% |

## Findings

1. A uniform 33% subset meets the exploratory recall/occupancy bands; 25% meets completeness but not preserved occupancy; 20% is warning-level. These are operational labels, not demonstrated usability or perceptual detail loss.
2. Equal image counts produce different reference scores. The remaining equal-budget conditions still span 88.8–98.8% recall when the extreme start burst is set aside descriptively.
3. All route gaps meet the completeness rule but have fine occupancy near 69%.
4. The start burst has 29.4% recall and 3.6% occupancy **and camera-center RMSE 3.0145 scene units, 31.46 times the fine voxel width**. The scores cannot be attributed solely to genuinely missing geometry or a cadence-only mechanism.
5. Internal screening can remain `good` while the derived reference-based verdict is warning or poor. Neither verdict establishes downstream task quality.

## Practical conclusion

For this Barn scene and recipe, count alone does not predict reference agreement. A one-third subset meets the declared bands, while a one-quarter subset does not meet preserved occupancy. Useful complementary overlap should not be eliminated indiscriminately. No phone-specific fraction, actual frame rate, perceptual usefulness, or universal minimum is established.

## Related Pages

- [[manuscript]]
- [[supplementary-results]]
- [[manuscript-audit]]

## Source Notes

The table preserves all frozen measurements and classifications. The final interpretation was narrowed on 2026-10-07 after the alignment-residual audit; no evaluator or comparison artifact was rewritten. “Completeness” and “detail fidelity” are historical metric labels for reference recall and spatial occupancy, not independently validated physical or perceptual quality.
