---
title: Image Subsets and Keyframes — Full-Text Review
type: synthesis
tags: [life, work, photogrammetry, literature]
created: 2026-10-04
updated: 2026-10-04
sources: [snavely2008skeletal, azimi2022keyframe, hosseininaveh2021network]
---

# Image Subsets and Keyframes — Full-Text Review

Three primary full-text reviews establish that geometry-aware selection and the inadequacy of image count alone are prior knowledge, not a new discovery of this study.

## Key Points

- Skeletal SfM reduces optimization cost, then registers remaining images; it is not permanent capture removal.
- Visual-inertial keyframe selection assesses positioning, which is different from dense-surface recall.
- Photogrammetric image-network design directly studies camera placement, subset selection, dense-cloud completeness, and noise.
- Our defensible scope is a descriptive fixed-recipe ablation with separate diagnostic axes, not a new optimal selection algorithm or universal minimum budget.

## Details

### 1. Snavely, Seitz, and Szeliski (2008)

**Paper:** *Skeletal Graphs for Efficient Structure from Motion*. CVPR. DOI: `10.1109/CVPR.2008.4587678`.

**Read:** complete 8-page paper and the three appended supplemental pages in the author-hosted PDF.

- **Sections 1–2, pp. 1–3:** build a reduced image core using pairwise camera-position uncertainty and graph connectivity. Completeness in this formulation concerns spanning the image graph and enabling subsequent pose estimation/triangulation; it is not our dense reference-recall metric.
- **Sections 3–4, pp. 4–6:** detect near-duplicates, construct a skeletal graph, reconstruct its interior nodes, then add other views through pose estimation and optionally apply full bundle adjustment.
- **Section 5, pp. 6–7:** compares runtime, registered-image count, and camera-position disagreement, with runtime figures explicitly excluding matching. These are not directly comparable to our end-to-end GPU pipeline durations.
- **Supplement, p. 3:** reports an additional camera-center ground-truth experiment on the Temple set. Do not conflate that dataset with our Barn study or this study's reconstructed reference.

**Implication:** successful sparse optimization from a small skeletal core does not establish that permanently retaining that core alone preserves dense object support. Conversely, our unoptimized stride/burst selections do not test or refute their graph-selection method.

**Source:** <https://www.cs.cornell.edu/~snavely/publications/papers/SkeletalSets_cvpr08.pdf>.

**PDF SHA-256:** `8692a3948c230d199310a7b38fd70db85d44b68a20b84b9f2c0aaaf70ba037fc`.

### 2. Azimi, Hosseininaveh, and Remondino (2022)

**Paper:** *A Novel Geometric Key-Frame Selection Method for Visual-Inertial SLAM and Odometry Systems*. ISPRS Archives, XLIII-B2-2022, 9–14. DOI: `10.5194/isprs-archives-XLIII-B2-2022-9-2022`.

**Read:** complete six-page publisher PDF.

- **Section 3, pp. 10–11:** adapts keyframe selection on ORB-SLAM3 using changes in viewing-vector zones, image-point spatial balance, and independently triggered IMU acceleration events.
- **Section 4, pp. 11–12:** evaluates EuRoC MH01 and MH02 in mono-inertial and stereo-inertial modes using trajectory alignment, absolute trajectory error, and processing time. ATE results are averaged over ten executions.
- **Sections 5–6, p. 13:** parameters remain dependent on angular zones and platform-specific acceleration thresholds; dense coherent point-cloud selection is identified as future work.

**Implication:** frame selection for localization is not interchangeable with dense-object completeness. Our study does not evaluate their algorithm, IMU signals, real-time constraints, or trajectory accuracy. We should not generalize their two-sequence performance to phone photogrammetry or repeat the paper's broad robustness language as an established universal result.

**Source:** <https://isprs-archives.copernicus.org/articles/XLIII-B2-2022/9/2022/isprs-archives-XLIII-B2-2022-9-2022.pdf>.

**PDF SHA-256:** `da66808d4c6aa0a3e344264598a9eb43afe9e4c9e105b3adf4e64bf9c989e37e`.

### 3. Hosseininaveh and Remondino (2021)

**Paper:** *An Imaging Network Design for UGV-Based 3D Reconstruction of Buildings*. Remote Sensing, 13(10), 1923. DOI: `10.3390/rs13101923`.

**Read:** complete 28-page publisher-hosted PDF, including duplicated text layers in the extracted document; substantive methods, results, discussion, and references were reviewed.

- **Sections 1–2, pp. 2–9:** distinguishes next-best-view, selection from an existing dense network, and model-based complete network design. Candidate poses use a rough building model, camera calibration, range constraints, and alternative center/façade directions. Selection operates on a visibility matrix with angular zones and accuracy/completeness stopping conditions.
- **Section 3.1, pp. 12–15:** simulation experiments identify corner gaps and alignment failures for some configurations. Lower image count is not sufficient evidence of a good capture network.
- **Section 3.3, pp. 17–24:** real-building capture includes a 1,489-image continuous sequence and a 236-image selected subset; dense processing is in Agisoft Metashape, not our COLMAP recipe. Surveyed points provide control and checks. Completeness is assessed through visual gaps and point counts in selected mosaics/building regions, not laser-reference surface recall. Plane-fit deviations assess local noise.
- **Section 4, pp. 24–25:** selection reduces noise while also reducing point density; viewpoint geometry affects intersection precision differently from dense matching. It already separates multiple dimensions of reconstruction quality.
- **Section 5, p. 25:** roof/top parts are out of scope due to terrestrial camera limitations; video keyframe selection is proposed as follow-up work.

**Implication:** “viewpoints matter more than image count” and “quality has several dimensions” are not novel claims. The paper provides direct prior art for building capture selection and geometric completeness/accuracy tradeoffs. Our occupancy proxy is different, but is not automatically more valid or more informative than their metrics. Their illustrative 95% visibility stopping condition must not be treated as validation of our 97% dense-recall threshold.

**Source:** <https://mdpi-res.com/d_attachment/remotesensing/remotesensing-13-01923/article_deploy/remotesensing-13-01923.pdf>.

**PDF SHA-256:** `eaab72a6e7152325aa57b59fba5152ad0ee237ec7054505bc593d80ee483634b`.

### Contribution boundary

The present research supplies an exploratory controlled set of global image-removal conditions, including equal-budget sectors, route gaps, and burst profiles, evaluated under one reconstruction recipe. It documents disagreement between internal verdicts and baseline-relative surface/occupancy scores and exposes alignment sensitivity in a second scene. It does not propose or benchmark a state-of-the-art subset selector, prove an optimal capture budget, validate a perceptual detail metric, or establish novelty over the entire literature.

A broader search should follow the direct image-selection references cited by these papers, including 2012–2014 photogrammetric image-network work, and inspect modern video/phone-specific studies before submission. A three-paper targeted review is not systematic coverage.

## Related Pages

- [[literature-review]]
- [[manuscript]]
- [[manuscript-audit]]

## Source Notes

Full texts were accessed on 2026-10-04. Citation identity was checked against Crossref records and PDF title pages. PDFs were used locally for review and are not redistributed in the report repository. No reconstruction measurements or frozen rules changed.
