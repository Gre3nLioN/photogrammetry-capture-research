---
title: Frozen Results and Artifact Map
type: synthesis
tags: [life, work, photogrammetry, reproducibility]
created: 2026-10-07
updated: 2026-10-07
sources: [16 Barn comparison.json artifacts, Helenenschacht frozen completeness report]
---

# Frozen Results and Artifact Map

Complete Barn multi-scale scores and artifact identifiers support the final technical report without changing the evaluator or measurements.

## Key Points

- These are the existing frozen comparison results, not new reconstruction experiments.
- Camera-center RMSE divided by fine voxel width is an alignment-context ratio, not surface error or a validated acceptance test.
- The start burst has a ratio of 31.459; all other reduced Barn conditions are between 0.029 and 0.204.
- The full reference's self-recall is 99.96%, rather than mathematically exact 100%, because deterministic query and comparison samples differ.

## Details

### Table S1. Full multi-scale and alignment results

Recall, largest component L, and occupancy are percentages. Fine/reference/coarse cell widths are 0.0958236, 0.1916472, and 0.3832943 in arbitrary reference units, respectively. The reference-query sample contains 249,473 points and its bounding-box diagonal is 38.3294327. The reference distance tolerance is 0.1916472. Values below are rounded, not used to recompute classifications.

| Exact experiment ID | Images | Recall | L | Fine | Reference scale | Coarse | Camera RMSE / fine width |
|---|---:|---:|---:|---:|---:|---:|---:|
| `barn-full-controlled` | 410 | 99.96 | 0.00 | 100.00 | 100.00 | 100.00 | 0.000 |
| `barn-stride-3` | 137 | 99.52 | 0.11 | 80.90 | 80.43 | 81.95 | 0.044 |
| `barn-stride-4` | 103 | 98.37 | 0.51 | 69.89 | 69.99 | 72.68 | 0.041 |
| `barn-stride-5` | 82 | 96.91 | 1.66 | 68.07 | 66.23 | 67.90 | 0.029 |
| `barn-sector-0-103` | 103 | 96.14 | 1.37 | 61.02 | 59.47 | 61.59 | 0.204 |
| `barn-sector-3-103` | 103 | 97.85 | 0.85 | 70.31 | 68.41 | 72.07 | 0.059 |
| `barn-sector-6-103` | 103 | 98.77 | 0.32 | 71.24 | 69.83 | 71.81 | 0.070 |
| `barn-sectors-0-1-103` | 103 | 93.62 | 3.14 | 57.56 | 59.55 | 63.79 | 0.119 |
| `barn-sectors-3-4-103` | 103 | 88.82 | 9.98 | 68.97 | 68.38 | 70.55 | 0.049 |
| `barn-sectors-6-7-103` | 103 | 97.92 | 0.72 | 68.22 | 63.62 | 61.74 | 0.088 |
| `barn-gap-start-103` | 103 | 97.85 | 1.16 | 68.71 | 66.60 | 67.55 | 0.049 |
| `barn-gap-middle-103` | 103 | 98.08 | 0.65 | 69.36 | 65.34 | 67.06 | 0.051 |
| `barn-gap-end-103` | 103 | 98.68 | 0.43 | 68.56 | 68.10 | 71.50 | 0.078 |
| `barn-burst-start-103` | 103 | 29.36 | 69.47 | 3.64 | 5.11 | 7.22 | 31.459 |
| `barn-burst-middle-103` | 103 | 96.75 | 1.76 | 66.22 | 66.36 | 69.15 | 0.046 |
| `barn-burst-end-103` | 103 | 94.71 | 3.44 | 62.44 | 58.41 | 59.76 | 0.046 |

All reduced Barn conditions registered their selected images: the number of shared cameras equals the image count in Table S1. This does not establish camera or surface accuracy. The controlled-reference alignment is a numerically near-identity self-transform, with camera RMSE approximately 2.15 × 10⁻¹⁴.

The extreme burst has camera RMSE 3.0144980, versus 0.0027987–0.0195717 for other reduced conditions. Camera geometry differs substantially under the frozen similarity fit. No equivalent Barn surface-refinement check was performed, and no independently correct alignment is established. Descriptively excluding that condition retains a 12-condition equal-budget recall range of 88.82–98.77% and fine occupancy of 57.56–71.24%. This is a reported robustness qualification, not a replacement table or a statistical sensitivity estimate.

### Table S2. Exact comparison-file hashes

Every row refers to `experiments/<experiment-id>/comparison.json` in the research repository. SHA-256 hashes identify the exact bytes audited on 2026-10-07. The corresponding selection manifest contains the full filename list and subset fingerprint; the execution record preserves commands and outcomes. Table 1's human-readable names map in the same order to these IDs.

| Experiment ID | SHA-256 of comparison.json |
|---|---|
| `barn-full-controlled` | `59263aa49331475f35ff441fb9e9b7c4c7f8920d3e6fe425b181b8d8e01b7fe1` |
| `barn-stride-3` | `cfb2582c9039c8db91def1af661915aa1c618b76a344f4705ea913b9d7c1d9ef` |
| `barn-stride-4` | `a4bbb1b6dca8ee25f6b4dd0324b9c58b1a0eee6afcddcc976d27f608cea2d4d4` |
| `barn-stride-5` | `8d66be69d3919355985b8be361a4586f6ec31e0129ea35fd6571568b1a23ebc4` |
| `barn-sector-0-103` | `9bd609eb26f2fe7d74ceeaa4df81b403255779ce16449c3b0f03631a619aba58` |
| `barn-sector-3-103` | `c98a69a87615f14872643f70d756249fb1e66a4481d3c13464500d991d6e6045` |
| `barn-sector-6-103` | `e4a430942e2a9214860287a3b0cedc4aae8ad484fb7f251a94cb6429139fc7cd` |
| `barn-sectors-0-1-103` | `22d158033423fb1e06c1bacb3187c3f45bf7bf1463f544ed2bfa65043ca389af` |
| `barn-sectors-3-4-103` | `b5b6a9db152dc6859b3a40eca208a0783962186dd0e4d16c40a89549ee749911` |
| `barn-sectors-6-7-103` | `75d384bcd9b8c2a6433987d509615635cfffc5a6d16361db9a45330d29d1bb51` |
| `barn-gap-start-103` | `155a310c752f9821f5e9234068cc7648d92d3142dd7f387c2cd441b49c135915` |
| `barn-gap-middle-103` | `a43f3476bc7c57bf67e9034938d43c739b99df0a242db75736300b87aaa897d2` |
| `barn-gap-end-103` | `b59f360b041029a18163077021d2e6faca9268fa7c581f543e0e0e1c4b228a5c` |
| `barn-burst-start-103` | `2561371ba58d5d4c9d0e79b05e5830ee489e8b6903cebbe9d30b04714136d6eb` |
| `barn-burst-middle-103` | `6cf089e908b3596a611338a2257ce275ded7e94aaceadf441b0ef83effa7fd39` |
| `barn-burst-end-103` | `35d6a983591818c62ed0a7010ddf58df0f9be04cae82485561d9a94508da81d8` |

### External-check artifact boundary

Frozen Helenenschacht results remain in `reports/helenenschacht-stride-2-completeness.json`. Diagnostic values and methods are in `reports/helenenschacht-alignment-sensitivity.md`. Local reconstructed references, source-selection manifests, and stage logs are not distributed here. The sensitivity runner is intentionally not published; the manuscript does not describe this pair as a complete public replication package.

## Related Pages

- [[manuscript]]
- [[manuscript-audit]]
- [[helenenschacht-alignment-sensitivity]]

## Source Notes

Tables were transcribed from read-only inspection of the existing JSON artifacts. Normalized ratios and printed rounding were derived from their stored values. No frozen score, source image, classification, or evaluator was changed.
