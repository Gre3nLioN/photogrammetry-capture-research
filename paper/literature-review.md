---
title: Capture Research Literature Review — Initial Evidence Map
type: synthesis
tags: [work, photogrammetry, literature]
created: 2026-10-03
updated: 2026-10-04
sources: [Crossref, Computer Vision Foundation, Tanks and Temples, COLMAP author website]
---

# Capture Research Literature Review — Initial Evidence Map

A focused initial reference map for the manuscript, with verification scope distinguished from full-paper review.

## Key Points

- Six references cover sparse/dense reconstruction, benchmark evaluation, view planning, and mobile reconstruction.
- Bibliographic verification is not equivalent to full methodological review.
- None of these sources validates our 97% completeness or 80% occupancy thresholds.
- No claim of novelty over all image-subset or keyframe-selection methods is justified yet.

## Details

Verified on 2026-10-03 using Crossref metadata, official CVF proceedings pages, the COLMAP author page, and the Tanks and Temples website. This pass reviewed available abstracts and bibliographic records, not complete papers.

| Key | Evidence consulted | Supported use | Important boundary |
|---|---|---|---|
| schoenberger2016sfm | Crossref; CVF abstract and proceedings record | Incremental SfM background; COLMAP citation | Registration/residuals do not establish reference accuracy |
| schoenberger2016mvs | Crossref; COLMAP author page; full author-hosted paper read on 2026-10-04 | Pixelwise geometry/visibility selection; insufficient baseline despite photometric similarity | Per-pixel MVS selection is not a global image-budget or video-keyframe experiment |
| knapitsch2017tanks | Crossref abstract; official benchmark description/BibTeX | Barn source attribution; benchmark has independently laser-scanned references | Our study uses a reconstructed baseline, not that ground truth |
| schoeps2017eth3d | Crossref; CVF abstract and proceedings record | Diverse indoor/outdoor scenes, DSLR and stereo-video inputs, laser-scanned reference | Does not supply a universal phone frame-rate recommendation |
| scott2003viewplanning | Crossref abstract and metadata | Pose selection for reconstruction/inspection objectives | Survey concerns active triangulation range sensors, not our passive SfM recipe |
| kolev2014mobile | CVF abstract and proceedings record; DOI in Tanks and Temples Crossref references | Interactive mobile depth integration with confidence and visibility handling | Not a controlled minimum-image-budget study; DOI not independently resolved in this pass |

### Verification links

- SfM: <https://openaccess.thecvf.com/content_cvpr_2016/html/Schonberger_Structure-From-Motion_Revisited_CVPR_2016_paper.html>
- MVS DOI: <https://doi.org/10.1007/978-3-319-46487-9_31>
- COLMAP author citation page: <https://demuc.de/colmap/>
- Tanks and Temples: <https://www.tanksandtemples.org/>
- ETH3D: <https://openaccess.thecvf.com/content_cvpr_2017/html/Schops_A_Multi-View_Stereo_CVPR_2017_paper.html>
- View-planning metadata: <https://api.crossref.org/works/10.1145/641865.641868>
- Mobile reconstruction: <https://openaccess.thecvf.com/content_cvpr_2014/html/Kolev_Turning_Mobile_Phones_2014_CVPR_paper.html>

### Full-text review: Pixelwise View Selection for Unstructured Multi-View Stereo

Read the complete 17-page author-hosted PDF, including methods, experiments, and references, on 2026-10-04. URL: <https://demuc.de/papers/schoenberger2016mvs.pdf>. PDF SHA-256: `c08164a02adba577604e2e2fcac3d5f36ae272bee29418a079cf1efad71677a5`. Supplementary material was not reviewed.

- **Section 4.2, pp. 6–8:** pixelwise selection favors sufficient triangulation baseline, comparable resolution, and suitable incident angle. Photometrically similar views may have very small baseline; the zero-baseline case contains no depth information. This directly grounds the rationale for studying redundant capture, without establishing our thresholds.
- **Section 4.3, p. 8:** “temporal” smoothness concerns optimization iterations, not capture frame rate. Do not cite it as a video-cadence result.
- **Sections 4.5 and 4.7, pp. 9 and 11–12:** geometric consistency, filtering, and fusion require cross-view support. Sparse registration is not the same process as dense-surface recovery.
- **Section 5, pp. 12–14:** evaluates algorithm-component ablations and benchmark reconstruction; not our fixed-budget, global input-subset protocol. The existence of geometric view-selection literature means “viewpoints matter” itself is not a novelty claim.
- **Bibliographic discrepancy:** the author-hosted PDF lists Pollefeys before Frahm, unlike the Crossref author order used in the current bibliography. Retain the publisher-metadata record provisionally and check the final proceedings before submission.

### Remaining review work

1. Read the remaining complete cited papers and record relevant method/evaluation passages; MVS full-text review is complete, excluding its supplement.
2. Review direct image-subset selection, video keyframe extraction, and controlled overlap/baseline studies.
3. Review modern smartphone photogrammetry studies, including compression, rolling shutter, blur, and calibration effects.
4. Verify the novelty claim against that literature; retain only descriptive contributions meanwhile.
5. Extend independent alignment checks: the completed Helenenschacht diagnostic confirms strong surface-alignment sensitivity, while the five tested grid phases change scores little. See [[helenenschacht-alignment-sensitivity]].

## Related Pages

- [[manuscript]]
- [[external-validation-helenenschacht-lite]]
- [[core-study-summary]]

## Source Notes

`references.bib` stores the six citation records. Metadata omitted from the BibTeX was not guessed. The initial literature pass does not support universal capture thresholds or a validated perceptual detail metric.
