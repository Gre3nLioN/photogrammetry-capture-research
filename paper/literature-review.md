---
title: Capture Research Literature Review — Targeted Evidence Map
type: synthesis
tags: [life, work, photogrammetry, literature]
created: 2026-10-03
updated: 2026-10-07
sources: [Crossref, Computer Vision Foundation, Tanks and Temples, COLMAP author website]
---

# Capture Research Literature Review — Targeted Evidence Map

A focused reference map for the final exploratory report, distinguishing metadata verification from full-text methodological review.

## Key Points

- Ten references cover sparse/dense reconstruction, benchmark evaluation, view planning, mobile reconstruction, global subsets, keyframes, and acquisition geometry.
- Full texts of [2, 7–10] were reviewed; background sources [1, 3–6] were checked through metadata and abstracts.
- All ten DOI records were checked against Crossref on 2026-10-07; final Springer metadata resolves the MVS author-order issue.
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
| kolev2014mobile | CVF abstract and proceedings record; Crossref DOI record rechecked 2026-10-07 | Interactive mobile depth integration with confidence and visibility handling | Not a controlled minimum-image-budget study |
| snavely2008skeletal | Crossref and complete author PDF including supplement | Uncertainty/graph-based sparse core, followed by registering remaining views | Not permanent removal of dense-reconstruction inputs |
| azimi2022keyframe | Crossref and complete publisher PDF | Geometric visual-inertial keyframes and trajectory/runtime evaluation | Localization endpoint differs from dense-object agreement |
| hosseininaveh2021network | Crossref and complete publisher PDF | Building network design, viewpoint selection, completeness/precision tradeoffs | Different scene, selector, pipeline, and quality endpoints |
| wenzel2013acquisition | Crossref and complete eight-page publisher PDF | Baseline/matching/precision tradeoffs and overlap-aware capture | Supports useful complementary redundancy, not elimination of all overlap |

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
- **Bibliographic discrepancy resolved 2026-10-07:** the author-hosted PDF puts Pollefeys before Frahm, but the final Springer chapter page explicitly lists Schönberger, Zheng, Frahm, and Pollefeys, matching Crossref. The bibliography follows the final proceedings order and pages 501–518. Verified source: <https://link.springer.com/chapter/10.1007/978-3-319-46487-9_31>.

### Full-text review: Image Acquisition and Model Selection for Multi-View Stereo

Read the complete eight-page publisher PDF on 2026-10-07. Source: <https://isprs-archives.copernicus.org/articles/XL-5-W1/251/2013/isprsarchives-XL-5-W1-251-2013.pdf>. SHA-256: `98bacb85205c2e0e66796fcc00e8d6cfde6dc7c0896d4d8d864a4e723fab103b`.

- **Sections 2.1–2.2, pp. 253–255:** small baselines can aid matching but weaken depth precision; larger baselines improve geometry while reducing similarity and increasing matching failure, especially on tilted surfaces. Multiple complementary stereo models can reduce noise and reject outliers.
- **Section 2.3, pp. 255–256:** orientation errors affect reconstructed surfaces despite successful SfM; structured-light reference comparisons show baseline and redundancy effects. Their alignment and noise measures are different from our occupancy metric.
- **Section 3, pp. 256–258:** the proposed “one panorama each step” strategy preserves overlapping stations and multiple heights, rather than pursuing the fewest images. The paper expressly cautions against gaps. Do not interpret our burst results as evidence that extra overlap is intrinsically harmful.
- **Scope:** SURE/VisualSFM and the evaluated scenes differ from our COLMAP ablation. Their acquisition examples and numerical overlap suggestions do not validate our 97% recall or 80% occupancy bands.

### Metadata conventions and retained review scope

- ETH3D's official CVF record gives pages 3260–3269; the IEEE Crossref record gives 2538–2547 for the same DOI. The manuscript/BibTeX consistently retain the verified CVF proceedings pagination. These are alternative proceedings records, not different papers.
- Tanks and Temples uses Crossref's 1–13 pagination; article-number metadata was not required or inferred.
- All cited identities, author order, year, and available page/volume fields were checked on 2026-10-07. This does not constitute full-text review of the five background-only sources.
- A broader systematic search, earlier photogrammetric selectors, and modern smartphone/video studies remain useful future work if the project pursues stronger novelty or capture guidance. The finished report instead retains a descriptive contribution and no universal recommendations.
- Barn's start-burst camera residual was audited from existing artifacts; independent alignment and an equivalent surface-refinement campaign remain limitations, not implicitly completed checks. See [[supplementary-results]] and [[helenenschacht-alignment-sensitivity]].

## Related Pages

- [[manuscript]]
- [[external-validation-helenenschacht-lite]]
- [[core-study-summary]]
- [[subset-keyframe-review]]

## Source Notes

`references.bib` stores ten citation records. The initial six-reference abstract/metadata pass was extended on 2026-10-04 by full-text reviews of Snavely et al. (2008), Azimi et al. (2022), and Hosseininaveh and Remondino (2021). Their publication identities were checked through Crossref and PDF title pages; source hashes and detailed distinctions are recorded in `subset-keyframe-review.md`. A fifth full-text review (Wenzel et al., 2013) and final metadata pass were completed on 2026-10-07. Metadata omitted from the BibTeX was not guessed. The targeted review does not support universal capture thresholds or a validated perceptual detail metric.
