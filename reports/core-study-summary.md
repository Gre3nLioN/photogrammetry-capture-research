# Core Study Summary — Barn Capture Budget, Coverage, and Cadence

## Objective

Estimate how a realistic phone capture budget affects complete-object coverage and retained detail. The controlled reference uses all 410 Barn images and the fixed CUDA COLMAP pipeline.

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

1. A uniformly distributed 33% capture remains good; 25% preserves the object but loses measurable detail; 20% is warning-level.
2. Equal image counts do not imply equal reconstruction quality. Missing sectors are scene-position dependent.
3. Contiguous route gaps preserved the Barn as an object, but all degraded detail.
4. Uneven video-like sampling is the most dangerous condition. A burst at the beginning lost most of the reference object despite retaining 103 images.
5. Internal COLMAP consistency can remain `good` while the complete-object task result is warning or poor.

## Practical conclusion

For this Barn scene and recipe, a modern phone capture should prioritize **distributed, distinct viewpoints** over nominal image count. A roughly one-third uniform sample was good; one-quarter was usable but detail-degraded. Redundant bursts and missing angular coverage can be substantially worse than uniform temporal reduction.

These are scene- and protocol-specific findings, not universal minimums.
