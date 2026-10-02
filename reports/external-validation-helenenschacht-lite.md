---
title: Lightweight External Validation — Helenenschacht
type: synthesis
tags: [work, photogrammetry, validation]
created: 2026-10-02
updated: 2026-10-02
sources: [Helenenschacht COLMAP reconstruction, ReconCheck frozen quality profile]
---

# Lightweight External Validation — Helenenschacht

A fast external check of the frozen ReconCheck internal-consistency metrics on the independent Helenenschacht reconstruction.

## Key Points

- All 176/176 images registered.
- Median view angle and eight-sector camera coverage pass the frozen thresholds.
- P95 reprojection error (2.27 px) and median track length (3 views) fail the frozen screening thresholds.
- This validates that the protocol is discriminative outside Barn, but does not validate completeness or detail-fidelity thresholds.

## Details

### Reproduction

Existing outputs were reused; no COLMAP rerun was performed.

```bash
cd wiki/projects/photogrammetry-quality-auditor
uv run python - <<'PY'
from pathlib import Path
from reconcheck.project import discover_project
from reconcheck.analysis import analyze_project
root = Path.cwd()
run = root / "runs/helenenschacht-colmap-v1"
project = discover_project(
    run,
    images=root / "raw/opendronemap/odm_data_helenenschacht/images",
    sparse=run / "colmap/sparse/0",
    dense=run / "colmap/dense/fused.ply",
    mesh=run / "colmap/dense/mesh.ply",
)
print(analyze_project(project, refresh=True))
PY
```

ReconCheck cache fingerprint: `f1ba53082444f141df7512bcf53d911748fc048ec560789fc55b34b684d91e6d`.

### Frozen internal-consistency checks

| Metric | Result | Threshold | Status |
|---|---:|---:|---|
| Registration ratio | 1.000 | ≥ 0.95 | Pass |
| Reprojection P95 | 2.269 px | ≤ 2.0 px | Fail |
| Median track length | 3.0 views | ≥ 4.0 views | Fail |
| Median view angle | 12.93° | ≥ 8.0° | Pass |
| Camera-sector coverage | 1.000 | ≥ 0.75 | Pass |
| Dense output | Present | Required | Pass |
| Mesh output | Present | Required | Pass |

The resulting ReconCheck status is `warning`, not `poor`: the reconstruction is fully registered and has broad viewpoint coverage, but has weaker feature-track support and somewhat higher residual error than the frozen screening profile expects.

### Reduced geometry sanity check

The existing dense artifacts are structurally readable binary PLY files:

- Dense cloud: 4,234,473 vertices.
- Mesh: 9,901,128 vertices and 19,558,404 faces.

This confirms output availability only. No absolute accuracy, completeness, or detail-fidelity claim is made because this pass did not construct a matched reduced baseline or independent reference geometry.

## Interpretation

This lightweight external check supports retaining the separation between internal consistency and object/detail evaluation. A reconstruction can register every image and cover all camera sectors while still failing stricter track and residual thresholds. It is evidence that the frozen profile detects meaningful variation outside the Barn study, not evidence that the thresholds generalize universally.

## Related Pages

- [[core-study-summary]]
- [[protocols/01-coverage-and-frame-rate]]
- [[../photogrammetry-quality-auditor/runs/helenenschacht-colmap-v1/README]]

## Source Notes

- Source reconstruction: `wiki/projects/photogrammetry-quality-auditor/runs/helenenschacht-colmap-v1/`.
- Immutable images: `wiki/projects/photogrammetry-quality-auditor/raw/opendronemap/odm_data_helenenschacht/images/`.
- Quality report: ReconCheck cache under `~/.local/share/reconcheck/datasets/f1ba53082444f141df7512bcf53d911748fc048ec560789fc55b34b684d91e6d/quality-report.json`.
