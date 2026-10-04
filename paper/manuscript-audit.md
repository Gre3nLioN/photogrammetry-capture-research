---
title: Photogrammetry Manuscript Consistency Audit
type: synthesis
tags: [work, photogrammetry, publication]
created: 2026-10-04
updated: 2026-10-04
sources: [Barn comparison artifacts, frozen evaluator, Helenenschacht reports, MVS author paper]
---

# Photogrammetry Manuscript Consistency Audit

An artifact and claim audit of the exploratory manuscript, with unresolved submission blockers recorded explicitly.

## Key Points

- All 16 Barn table rows match the archived comparison scores to the reported precision.
- The controlled Barn reference has 206,930 sparse points; legacy internal-delta reports use a different 206,801-point baseline.
- Reference recall and fine occupancy are operational metrics, not direct proof of true missing geometry or lost perceptual detail.
- The tested budgets do not locate an exact minimum or establish phone-video recommendations.

## Details

### Checks completed

- Read all 16 `comparison.json` artifacts and corresponding internal-quality report metadata.
- Confirmed table internal/task verdicts and rounded recall/occupancy values.
- Confirmed the experiment count: one controlled reference, three variable-budget stride conditions, and twelve 103-image sector/gap/cadence conditions.
- Compared the manuscript with the frozen dense evaluator: deterministic sampling caps, one-way nearest-neighbor recall, sampled reference diagonal, voxel scales, normalization ceiling, and 26-neighbor missing-component construction.
- Distinguished PCA-plane selection sectors from ReconCheck's world-XY camera-sector diagnostic.
- Distinguished the Barn 1200-pixel dense recipe from the Helenenschacht 1600-pixel recipe.
- Documented that research CI is not a cross-platform GPU replication campaign.

### Corrections made

1. Changed the title to avoid claiming an established minimum viable budget.
2. Replaced unsupported phone-resolution framing with a qualified mobile-reconstruction motivation.
3. Added exact screening requirements and definitions of the geometric proxies.
4. Explained that archival internal deltas refer to the legacy quality baseline, whereas dense-reference scores use the controlled reference. No stored artifact was rewritten.
5. Qualified practical-use and detail-loss statements; no user-task or perceptual validation was performed.
6. Described the public/local artifact boundary and report-only sensitivity procedure accurately.
7. Read the full author-hosted MVS paper, grounding redundancy in triangulation geometry without claiming that insight is novel.

### Remaining submission blockers

- **Direct prior art:** full-text global image-subset and video-keyframe-selection studies remain unreviewed; a novelty claim is not justified.
- **Bibliography:** resolve the MVS author-order discrepancy between author-hosted PDF and Crossref; verify final proceedings metadata and remaining complete papers.
- **Alignment:** Helenenschacht diagnostic refinement improves surface agreement while worsening camera agreement; no independent correct alignment is established. The Barn occupancy scores have not received the same sensitivity audit.
- **Evaluation scope:** thresholds remain exploratory. No independent geometry, repeat-run uncertainty, perceptual-quality assessment, or actual phone-video experiment is reported.
- **Replication boundary:** Helenenschacht's large outputs and run artifacts remain local. Published report descriptions are not a portable complete replication package.
- **Editorial:** reconcile abstract/detail terminology consistently; review figures at publication size and select a target venue/template before declaring submission readiness.

These items need either additional evidence or explicit retention as limitations; not every exploratory paper requires a new reconstruction campaign. No inference of statistical significance or universal threshold performance is warranted.

## Related Pages

- [[manuscript]]
- [[literature-review]]
- [[helenenschacht-alignment-sensitivity]]

## Source Notes

The audit changes presentation and interpretation only. Frozen thresholds, evaluator code, measurements, and immutable raw inputs remain unchanged.
