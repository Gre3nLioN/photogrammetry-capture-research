---
title: Photogrammetry Manuscript Consistency Audit
type: synthesis
tags: [life, work, photogrammetry, publication]
created: 2026-10-04
updated: 2026-10-07
sources: [Barn comparison artifacts, frozen evaluator, Helenenschacht reports, Crossref, Springer, CVF, ISPRS guidelines]
---

# Photogrammetry Manuscript Consistency Audit

The final technical-report audit verifies the frozen results and narrows interpretation where alignment, reference construction, or exploratory rules prevent stronger claims.

## Key Points

- All 16 main-table rows and all 16 supplementary multi-scale/alignment rows match the archived artifacts at printed precision.
- All 16 comparison-file SHA-256 hashes were independently recomputed and matched the supplementary map.
- The extreme Barn start burst has a camera-alignment residual 31.46 times its fine cell width; pure geometry-loss claims were removed.
- MVS author order was resolved against final Springer metadata; ten citation identities were checked.
- The completed 10-page neutral report is not peer reviewed or already an official venue submission.

## Details

### Data and numerical checks

- Confirmed one controlled reference, three stride conditions, and twelve fixed-budget sector/gap/burst conditions. Stride 4 makes thirteen equal-budget 103-image conditions.
- Compared every main-table count, internal verdict, derived verdict, recall, fine occupancy, and largest disagreement-component fraction with the corresponding JSON. All pass.
- Compared every supplementary recall, largest component, all three occupancy scales, and camera-RMSE/fine-width ratio with stored fields. All pass.
- Recomputed every comparison-file SHA-256 and matched the exact-byte map. These are file hashes, distinct from dataset/subset fingerprints.
- Verified all sixteen stored registration ratios equal 1.0 and shared-camera counts equal selected-image counts.
- Confirmed full-reference self-recall is 99.96%, rounding to 100.0%, rather than exactly 100%.
- Distinguished the controlled reference's 206,930 sparse points from the legacy internal-delta baseline's 206,801. No legacy artifact was rewritten.
- Confirmed the start-burst camera RMSE of 3.0144980 against the fine width 0.0958236. Other reduced Barn ratios are 0.029–0.204.
- Descriptively excluding the start burst leaves equal-budget recall 88.82–98.77% and fine occupancy 57.56–71.24%. The original row remains present; this is neither a replacement score nor statistical inference.

### Method and claim checks

- Read the frozen evaluator and reconciled the SVD camera-center similarity, deterministic PLY sampling caps, sampled diagonal, one-way recall, zero-origin voxelization, reference sampling ceiling, clipping, and 26-neighbor component rule.
- Added mathematical definitions and the absent independent object-only mask; fused background/outliers can affect support and scale.
- Replaced perceptual “detail loss” language with spatial occupancy and clearly identified artifact labels as operational bands.
- Distinguished PCA-plane omission sectors from world-XY screening sectors; neither proves surface visibility.
- Distinguished Barn 1200-pixel dense processing from Helenenschacht 1600-pixel processing.
- Retained full Helenenschacht frozen and refined values without substituting fitted scores. Fitting uses the scoring reference and worsens camera agreement; no independently correct alignment is established.
- Explicitly reported that Barn has not received equivalent surface-refinement analysis, and that surface fitting does not verify ground truth.
- Removed universal minimum-budget, phone-capture fraction, actual-frame-rate, validated-usability, and new-optimal-selector claims.
- Qualified the 80.9% stride-3 score's proximity to the exploratory 80% band. No repetition or confidence interval is implied.

### Literature and editorial checks

- Ten DOI identities/author records were checked against Crossref on 2026-10-07. Final Springer author order resolves the MVS discrepancy in favor of Schönberger, Zheng, Frahm, Pollefeys; pages 501–518 added.
- Official CVF ETH3D pagination (3260–3269) is retained consistently; alternative IEEE Crossref pagination (2538–2547) is documented in the evidence map.
- Full texts of the MVS, skeletal-SfM, geometric-keyframe, building-network, and acquisition-geometry papers were reviewed. Remaining background sources were checked through abstracts/metadata, not described as full-text reviewed.
- Wenzel et al. supplies the necessary counterpoint that complementary overlap and redundancy can benefit dense reconstruction. The bursts replace distributed observations; they do not test simply adding more overlapping images.
- Reconciled abstract, results, discussion, conclusion, README, and core summary with the narrower interpretation.
- Abstract: 209 words; six keywords. No invented author, affiliation, funding, or conflict statement.

### PDF and figure checks

- Built `paper/manuscript.pdf` with Pandoc 3.8.2 and Typst 0.14.0 using checked-in neutral layout metadata. A4, 10 pages, embedded text, tagged PDF; no JavaScript.
- Inspected the title/abstract, complete Table 1, and both figure pages at rendered reading size. Captions are attached to their tables/figures without duplicate numbering.
- Figure 1 displays all thirteen 103-image conditions and flags the alignment-confounded start burst. The connecting segments are explicitly not uncertainty bars.
- Figure 2 retains the four original fixed-band distance panels as an unchanged crop, enlarged for readable labels. The full eight-panel overlay/map figure remains in the sensitivity report.
- Checked image paths and the PDF text extraction. Both formulas, ten references, and section text are present.
- `git diff --check` passed. No differences in experiments, evaluator/selection source, scripts, tests, protocols, or dataset manifests were introduced during finalization.

### Retained scientific boundaries

These are stated limitations, not implied completed experiments:

- No independent ground truth or correct alignment, equivalent Barn surface refinement, or repeat-run uncertainty campaign.
- No perceptual/task validation, optimized-selector benchmark, actual phone-video tests, or universal threshold validation.
- One primary scene and one limited external pair, with different dense resolutions.
- Targeted literature coverage rather than a systematic review.
- Public Barn artifacts versus local-only Helenenschacht manifests/logs/reconstructions; no public sensitivity runner.

A broader or more demanding venue may require extra evidence. Those choices are a separate research phase, not hidden behind the word “finished.”

### Actual submission requirements

The personal technical report is complete. Ivan Roumec subsequently supplied his publication name and contact email and clarified that he does not intend to submit it to any venue. He is credited as an independent researcher, with Codex/AI assistance disclosed separately. The PDF was rebuilt with this credit and disclosure; no scientific result changed. [[submission-notes]] is now explicitly archived guidance, not a pending task list. No submission, acceptance, preprint registration, or DOI minting was performed.

## Related Pages

- [[manuscript]]
- [[supplementary-results]]
- [[literature-review]]
- [[submission-notes]]

## Source Notes

Finalization changes reporting and interpretation only. Frozen measurements, classifications, thresholds, evaluator code, and immutable raw inputs remain unchanged. Transient read-only validation commands were not added as public scripts or tests.
