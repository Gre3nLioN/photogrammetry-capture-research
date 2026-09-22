# Protocol 01 — Coverage and frame-rate budget

## Objective

Estimate the minimum temporal image sampling and spatial coverage that preserve a high-quality reconstruction of the Barn reference scene.

## Hypotheses

1. Uniformly reducing frame rate degrades reconstruction more gradually than removing a contiguous trajectory segment at the same image count.
2. Missing a camera sector causes coverage and viewing-angle failures before uniform frame reduction does.
3. A quality profile can identify a practical minimum image budget only when registration, reprojection, track support, viewing geometry, and coverage are evaluated together.

## Constants

- Parent dataset: Tanks and Temples Barn image set.
- Parent baseline: full-resolution, full-trajectory reconstruction.
- Reconstruction recipe: fixed and versioned before any condition runs.
- Quality instrument: ReconCheck `general-photogrammetry-v1` report.
- Raw inputs: immutable; all subsets/degradations are derived artifacts.

## Conditions

### A. Uniform temporal decimation

| Condition | Selection | Expected fraction |
|---|---|---:|
| A0 | Full baseline | 100% |
| A1 | Every 2nd source image | 50% |
| A2 | Every 3rd source image | 33% |
| A3 | Every 5th source image | 20% |
| A4 | Every 10th source image | 10% |

### B. Fixed-seed random subsets

For 75%, 50%, 33%, 20%, and 10% image budgets, run seeds `101`, `202`, and `303`. Report the mean, standard deviation, worst case, and pass rate; a single random subset is not evidence of a reliable minimum.

### C. Contiguous trajectory gaps

Remove contiguous ordered segments of 10%, 20%, and 33% of source images. Repeat at three non-overlapping trajectory positions.

### D. Camera-sector removal

Partition registered camera centers into eight azimuthal sectors around their centroid. Remove one sector at a time, then adjacent pairs. Record sector definition and every removed image ID in the manifest.

## Required outputs per condition

- `experiment-manifest.json`
- Materialized derived image directory, if the reconstruction tool cannot consume a manifest directly
- Exact reconstruction recipe and stage status
- ReconCheck Quality Report
- Comparison to the full baseline
- Human-readable conclusion and limitations

## Primary endpoints

- Quality profile verdict and individual check transitions
- Registration ratio
- P95 reprojection error
- Median track length
- Median maximum view angle
- Trajectory-sector coverage ratio
- Sparse point count
- Dense-cloud and mesh availability

## Decision rule

The provisional minimum viable budget is the smallest budget that passes the quality profile across all required repetitions and does not conceal a localized coverage failure. It is a scene- and protocol-specific result, not a universal threshold.
