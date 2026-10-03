---
title: Capture Research Literature Review — Initial Evidence Map
type: synthesis
tags: [work, photogrammetry, literature]
created: 2026-10-03
updated: 2026-10-03
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
| schoenberger2016mvs | Crossref; COLMAP author citation page | Dense MVS implementation attribution | Full view-selection method still requires paper reading |
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

### Remaining review work

1. Read the complete cited papers and record relevant method/evaluation passages.
2. Review direct image-subset selection, video keyframe extraction, and controlled overlap/baseline studies.
3. Review modern smartphone photogrammetry studies, including compression, rolling shutter, blur, and calibration effects.
4. Verify the novelty claim against that literature; retain only descriptive contributions meanwhile.
5. Check scene alignment and voxel-grid sensitivity before interpreting low occupancy as detail loss alone. Helenenschacht camera-center RMSE is approximately 90% of the fine voxel width, so geometric drift/grid phase may contribute substantially to its occupancy score.

## Related Pages

- [[manuscript]]
- [[external-validation-helenenschacht-lite]]
- [[core-study-summary]]

## Source Notes

`references.bib` stores the six citation records. Metadata omitted from the BibTeX was not guessed. The initial literature pass does not support universal capture thresholds or a validated perceptual detail metric.
