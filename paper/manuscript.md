---
title: "Image Budget and Viewpoint Distribution in Photogrammetry: An Exploratory Study"
type: synthesis
tags: [life, work, photogrammetry, research]
created: 2026-10-03
updated: 2026-10-07
sources: [Barn experiment artifacts, Helenenschacht reports, references.bib]
---

# Image Budget and Viewpoint Distribution in Photogrammetry: An Exploratory Study

**Exploratory technical report · 7 October 2026 · Not peer reviewed**

**Keywords:** photogrammetry; image subsets; viewpoint distribution; structure from motion; reference recall; alignment sensitivity.

## Abstract

Image count alone does not describe the geometric support of a photogrammetric capture. We examine deterministic image removal from the 410-image Tanks and Temples Barn sequence using a fixed CUDA-enabled COLMAP pipeline. Sixteen reconstructions comprise a full-capture reference and 15 reduced conditions: uniform strides, angular-sector omissions, route gaps, and concentrated bursts. Evaluation separates internal reconstruction screening, one-way dense-reference recall, and normalized multi-scale voxel occupancy. A 137-image uniform subset achieved 99.5% recall and 80.9% fine occupancy; a 103-image uniform subset achieved 98.4% and 69.9%. Thirteen equal-budget 103-image conditions ranged from 29.4% to 98.8% recall despite all receiving a good internal verdict. However, the lowest-scoring burst also had a large camera-alignment residual, preventing attribution solely to missing geometry. Excluding that condition, recall still ranged from 88.8% to 98.8% and fine occupancy from 57.6% to 71.2%. A separate Helenenschacht stride-2 check registered 87 of 88 images but yielded 70.6% recall and 3.6% fine occupancy. Exploratory surface refinement increased these to 83.8% and 51.3% while worsening camera agreement. These observations support reporting internal consistency, reference agreement, spatial occupancy, and alignment diagnostics separately. The study is descriptive and scene- and recipe-specific: reconstructed references are not ground truth, quality bands are exploratory, and neither an optimal image selector nor general phone-video capture guidance is established.

## 1. Introduction

Image-based mobile reconstruction motivates practical questions about distributing a limited capture budget [6]. Many images can cover a restricted portion of a route, whereas fewer images distributed along it may retain broader geometric support. Photogrammetric network design already recognizes the importance of viewpoint geometry, overlap, and visibility [9, 10]. The present question is therefore not whether viewpoint selection matters in principle, but how particular deterministic reductions behave under a recorded reconstruction recipe and separate diagnostic axes.

We ask: **How do image budget and distribution affect internal screening, dense-reference agreement, and spatial occupancy in a controlled reconstruction study?** The primary experiment uses an existing Barn image sequence, not a new phone-video capture. Its contributions are:

1. A documented set of global image-removal conditions, including equal-budget sector, route-gap, and burst profiles, with immutable inputs and explicit selection manifests.
2. A descriptive comparison of internal screening and two dense-reference metrics under one Barn reconstruction recipe.
3. An artifact-based alignment audit and a second-scene sensitivity diagnostic showing why low geometric scores cannot automatically be interpreted as missing surface or lost detail.

No optimal subset algorithm, absolute geometric accuracy, perceptual usefulness, or universal minimum budget is claimed. The full-capture reconstruction is a reference with its own errors, not independently measured truth.

## 2. Related Work

### 2.1 Reconstruction and reference evaluation

Schönberger and Frahm [1] describe a robust incremental structure-from-motion (SfM) pipeline. For dense reconstruction, Schönberger et al. [2, Section 4.2] select source views per pixel using photometric evidence and geometric priors, including triangulation angle, relative resolution, and incident angle. Nearly zero-baseline views can be photometrically similar without providing useful depth information. Their geometric consistency and fusion requirements [2, Sections 4.5 and 4.7] are distinct from sparse registration. Pixelwise source-view selection occurs inside multi-view stereo (MVS); our conditions remove images globally before SfM. Their “temporal” smoothness refers to optimization iterations, not video cadence [2, Section 4.3].

Tanks and Temples [3] and ETH3D [4] evaluate reconstructions using independently acquired laser-scanned references. We use Barn images from the former but do not use its laser ground truth. Our one-way recall against a reconstructed full-capture cloud is not equivalent to benchmark accuracy or a symmetric reconstruction-quality score.

### 2.2 Global subsets, keyframes, and capture geometry

Snavely et al. [7] select a skeletal image core using camera-position uncertainty and graph connectivity, then register remaining images through pose estimation, with optional full bundle adjustment. Their sparse-optimization reduction does not permanently exclude those images from the reconstruction. Runtime, registration, and camera-position comparisons consequently address different endpoints from our dense-reference ablation.

Azimi et al. [8] select geometric keyframes within visual-inertial SLAM using viewing-vector changes, image-point distribution, and IMU events. Their two-sequence EuRoC evaluation addresses trajectory error and processing time, including repeated trajectory-error runs. Online positioning quality does not establish complete-object dense recovery; we do not benchmark their selector or sensor constraints.

More directly, Hosseininaveh and Remondino [9] design building imaging networks using a rough model, camera/range constraints, and visibility-based selection. Their simulation and real-building experiments compare center/façade capture directions and continuous versus selected capture. Survey errors, gaps, point density, and plane-fit noise already distinguish multiple reconstruction-quality dimensions. Their 1,489-image continuous capture and 236-image selected subset use a different scene, selection method, and Metashape pipeline, so their outcomes do not validate our thresholds.

Wenzel et al. [10] examine small- and large-baseline stereo geometry, surface inclination, and orientation error. Small baselines can aid matching and provide complementary observations, while larger baselines improve depth precision only within matching constraints. Their “one panorama each step” guidance combines distributed stations with substantial overlap. This is an important qualification: redundancy is not inherently wasteful, and our burst experiment is not evidence that additional overlapping images generally harm reconstruction.

Scott et al. [5] provide view-planning context for active triangulation sensors rather than direct evidence for passive phone capture. Kolev et al. [6] demonstrate interactive mobile reconstruction with confidence-weighted depth integration and visibility handling, not a universal image-budget rule.

### 2.3 Contribution boundary

Geometry-aware selection and completeness/precision tradeoffs are established prior art. This study contributes a fixed-recipe descriptive ablation and transparent diagnostic disagreements, not a new selector or demonstrated superiority over earlier methods. Full texts of [2, 7–10] were reviewed; the remaining background references were checked through metadata and abstracts. This targeted review is not systematic coverage of all photogrammetric subset or modern smartphone/video methods.

## 3. Data and Reference Reconstructions

### 3.1 Barn

The immutable Barn source contains 410 ordered JPEG images from the Tanks and Temples training set [3]. Archive and image-tree SHA-256 fingerprints are recorded in `datasets/tanks-and-temples-barn.json`. Reduced conditions use symbolic links, with complete selected filename lists and deterministic fingerprints. The raw image-tree fingerprint remained unchanged throughout the study.

The full controlled condition, `barn-full-controlled`, registered 410/410 images and produced 206,930 sparse points, a fused dense cloud, and a Poisson mesh. Its internal verdict was good. This run supplies the dense reference. Archived internal-metric deltas retain an earlier 206,801-point full-capture baseline; those deltas are not used in the paper's results. Reported internal verdicts belong to each condition itself.

### 3.2 Helenenschacht

A separate 176-image OpenDroneMap aerial dataset provides a limited second-scene check. All 176 images registered in its full reference run. A deterministic stride-2 subset retains 88 images. This pair is not a replication of the complete Barn condition campaign and does not represent handheld phone capture.

## 4. Methods

### 4.1 Reconstruction and selection

Every Barn condition used COLMAP 4.1.0 with CUDA [1, 2]: GPU SIFT extraction with one shared camera model, exhaustive GPU matching, incremental mapping, undistortion capped at 1200 pixels, GPU PatchMatch stereo, stereo fusion capped at 1200 pixels, and Poisson meshing. ReconCheck 0.1.0 supplied separate internal diagnostics. Exact commands, software versions, stage times, exit codes, and log paths are recorded in each execution artifact. Unspecified settings follow the recorded COLMAP version's defaults; results are not assumed portable across recipes.

The 16 Barn runs include one full reference and the following 15 reductions:

- **Uniform strides:** every third, fourth, or fifth image, retaining 137, 103, or 82 images (33.4%, 25.1%, or 20.0%).
- **Single-sector omission:** exclude sector 0, 3, or 6, then sample 103 images evenly from the retained ordered trajectory.
- **Adjacent-sector omission:** exclude sectors 0–1, 3–4, or 6–7, then similarly retain 103 images.
- **Route gaps:** remove a contiguous 103-frame segment from the start, middle, or end, then sample 103 images evenly from the remainder.
- **Bursts:** concentrate approximately half the 103-image budget inside one fifth of the ordered route, with the remainder sampled outside it; place that window at the start, middle, or end.

Selection sectors partition reference-camera centers into eight angular bins after projection onto a best-fit PCA plane. They are location proxies, not measured surface visibility. Ordered-index sampling is likewise not a calibrated time or frame-rate measurement. The cadence conditions do not reproduce compression, rolling shutter, blur, exposure transitions, or other phone-video effects. Selected filename lists resolve rounding and endpoint details.

The three stride conditions vary count and separation simultaneously. The 13 conditions with 103 images—including stride 4—hold nominal count fixed, but vary geometry and potentially reconstruction stability together. Only these deterministic conditions were completed; random-seed and decimation campaigns in the broader protocol were not.

### 4.2 Internal screening

ReconCheck's `general-photogrammetry-v1` profile checks registration ≥95%, P95 reprojection error ≤2 pixels, median track length ≥4 views, median maximum view angle ≥8°, camera-sector occupancy ≥75%, and dense-cloud/mesh availability. Reprojection percentiles summarize errors associated with reconstructed 3D points, not a pooled percentile of every image residual. The view-angle statistic summarizes each point's maximum supported angle.

These heuristic checks describe support among supplied images, not independent accuracy or complete observation of the intended object. Screening sectors use camera centers in the world XY plane, unlike the PCA-plane selection sectors. Neither sector diagnostic directly measures visibility. Completing a pipeline or obtaining a good verdict is not validated downstream usability.

### 4.3 Reference recall and disagreement regions

A similarity transform estimated by SVD aligns subset camera centers to reference centers shared by filename. The corresponding transform is applied to the subset cloud. Camera-center RMSE is recorded, but is not itself a surface-error estimate.

PLY vertices are sampled deterministically in file order: at most 250,000 reference-query points, and at most 1,000,000 points each for the reference sampling ceiling and experiment cloud. Let these samples be Q, R, and E, respectively, with E already aligned. The integer sampling stride can produce fewer points than the cap. Let D be the bounding-box diagonal of Q and set the distance tolerance to 0.005D. Reference recall is

$$
C = \frac{1}{|Q|}\sum_{q\in Q}\mathbf{1}\left[\min_{e\in E}\|q-e\|\leq 0.005D\right].
$$

This one-way score does not directly penalize additional subset geometry. Disagreement includes missing surfaces, displaced geometry, and reference errors. There is no independently validated object-only mask; the sampled fused reference, including its background and outliers, defines the scored support and scale.

Out-of-tolerance reference points are voxelized at twice the tolerance, with 26-neighbor connected components. The largest component is selected by reference-point count, not physical area. Its fraction L is relative to all query points. “Missing component” in the artifacts is therefore a disagreement-region label, not verified absence.

### 4.4 Spatial occupancy

For cell widths h of 0.0025D, 0.005D, and 0.01D, let $V_h(X)$ denote the occupied cells of sample X under floor-based voxelization with coordinate-zero grid origin. The raw occupancy fraction is the proportion of $V_h(Q)$ also occupied by $V_h(E)$. The sampling ceiling is the corresponding fraction for $V_h(R)$. Normalized occupancy is

$$
O_h = \min\left(1,\frac{|V_h(Q)\cap V_h(E)|}{|V_h(Q)\cap V_h(R)|}\right).
$$

The query-cell denominator cancels between raw occupancy and ceiling. Normalization accounts for the reference's own finite sampling support; it does not eliminate experiment-density effects, residual alignment, grid-phase sensitivity, or file-order sampling bias. Occupancy describes spatial support rather than edge sharpness, texture, topology, or perceptual detail. The artifacts call this metric “detail fidelity”; we use spatial occupancy to avoid that stronger interpretation.

### 4.5 Exploratory classification

The frozen rules assign **complete** when C ≥97% and L <2%; **partially complete** when 95% ≤ C <97% and L <2%; and **incomplete** otherwise. Fine-occupancy bands are **preserved** at ≥80%, **degraded** at 60–<80%, and **poor** below 60%.

A derived verdict is good only for complete recall classification and preserved occupancy; it is poor for incomplete classification or poor occupancy, and warning otherwise. These labels do not certify object completeness or practical fitness. The rules were calibrated after inspection of early conditions and frozen before the burst tests. They are exploratory rather than externally validated quality thresholds.

Helenenschacht used 1600-pixel dense processing for both full and reduced runs, rather than Barn's 1200 pixels. Evaluation rules were unchanged. Its diagnostic surface refinement starts from camera alignment and performs 20 trimmed nearest-neighbor rigid SVD updates without scale changes. Correspondences beyond twice the tolerance are rejected and the highest remaining 20% of distances are trimmed. This optimizes against the scoring reference and is not independent alignment verification.

## 5. Results

### 5.1 Barn outcomes

Table: Frozen Barn scores. Recall and fine occupancy are percentages; L is the largest disagreement component as a percentage of query points. Internal and derived verdicts refer to separate rules. Unrounded artifacts determine labels; displayed values are rounded. Full-reference recall rounds to 100.0%, but its underlying value is 99.96% because the query and comparison samples differ.

| Condition | N | Internal | Derived | Recall | Fine occupancy | L |
|---|---:|---|---|---:|---:|---:|
| Full reference | 410 | good | good | 100.0 | 100.0 | 0.00 |
| Stride 3 | 137 | good | good | 99.5 | 80.9 | 0.11 |
| Stride 4 | 103 | good | warning | 98.4 | 69.9 | 0.51 |
| Stride 5 | 82 | warning | warning | 96.9 | 68.1 | 1.66 |
| Sector 0 omitted | 103 | good | warning | 96.1 | 61.0 | 1.37 |
| Sector 3 omitted | 103 | good | warning | 97.8 | 70.3 | 0.85 |
| Sector 6 omitted | 103 | good | warning | 98.8 | 71.2 | 0.32 |
| Sectors 0–1 omitted | 103 | good | poor | 93.6 | 57.6 | 3.14 |
| Sectors 3–4 omitted | 103 | good | poor | 88.8 | 69.0 | 9.98 |
| Sectors 6–7 omitted | 103 | good | warning | 97.9 | 68.2 | 0.72 |
| Start route gap | 103 | good | warning | 97.8 | 68.7 | 1.16 |
| Middle route gap | 103 | good | warning | 98.1 | 69.4 | 0.65 |
| End route gap | 103 | good | warning | 98.7 | 68.6 | 0.43 |
| Burst at start | 103 | good | poor | 29.4 | 3.6 | 69.47 |
| Burst in middle | 103 | good | warning | 96.8 | 66.2 | 1.76 |
| Burst at end | 103 | good | poor | 94.7 | 62.4 | 3.44 |

Uniform stride 3 met both declared bands. Stride 4 met the completeness rule but not preserved occupancy; stride 5 was partially complete with degraded occupancy and an internal warning. The 80.9% stride-3 score is close to the exploratory 80% boundary, so it should not be interpreted as a robust minimum-budget estimate.

Single-sector omissions yielded 96.1–98.8% recall and 61.0–71.2% fine occupancy. Adjacent-sector omissions were location-dependent: sectors 0–1 and 3–4 failed completeness, whereas sectors 6–7 met it. All three route gaps met completeness, with 97.8–98.7% recall, but had fine occupancy near 69%. These are differences in operational reference agreement, not direct measurements of perceptual quality.

All 13 equal-budget conditions received an internal good verdict. Their derived verdicts nevertheless included four poor results. Pipeline completion and internal support thus did not predict acceptance under the dense-reference rules.

![All 13 conditions retain 103 images. Circles show recall and squares fine occupancy; joining lines connect two different metrics for the same condition, not confidence intervals. Dashed lines show the 97% recall and 80% occupancy bands; the component rule L <2% also applies. The highlighted start burst has a large camera-alignment residual and must not be interpreted as pure missing surface. Conditions are deterministic runs, with no repeat-run uncertainty bars.](figures/coverage-detail-summary.png)

### 5.2 Barn alignment audit

Existing comparison artifacts expose a major confound in the start burst: shared-camera RMSE is 3.0145 scene units, or 31.46 times the fine cell width of 0.09582. Other reduced Barn conditions have RMSE/fine-width ratios of 0.029–0.204. The start burst's 29.4% recall and 3.6% occupancy therefore combine dense-reference disagreement with substantially inconsistent camera geometry. They cannot identify the amount of genuinely absent surface or establish a cadence-only mechanism.

Excluding that condition descriptively—not rewriting its result—the remaining equal-budget conditions still span 88.8–98.8% recall and 57.6–71.2% fine occupancy. Three of them fail the completeness rule. Smaller camera residuals do not prove correct surface alignment, however, and Barn has not undergone the surface-refinement sensitivity analysis performed on Helenenschacht. Supplementary tables provide all three occupancy scales, alignment ratios, experiment IDs, and comparison-file hashes.

### 5.3 Helenenschacht check and sensitivity

The 88-image subset registered 87/88 images, achieved full screening-sector coverage, and had a median view angle of 19.95°. Its internal verdict was warning because P95 reprojection error was 2.266 pixels and median track length was three views. With 87 shared-camera centers, frozen reference recall was 70.64%, L was 29.29%, and fine occupancy was 3.62%.

Table: Helenenschacht frozen evaluation and exploratory rigid surface refinement. Distances are arbitrary reference reconstruction units. The refined condition is diagnostic, not a replacement result.

| Diagnostic | Camera alignment | Surface refinement |
|---|---:|---:|
| Reference recall | 70.64% | 83.79% |
| Normalized fine occupancy | 3.62% | 51.33% |
| Median surface distance | 0.10270 | 0.00803 |
| Camera-center RMSE | 0.04859 | 0.11952 |

Fine cell width is 0.05417 scene units. Camera alignment RMSE is therefore about 90% of one fine cell width. Five tested grid phases yielded 3.45–3.62% fine occupancy, whereas surface refinement increased it to 51.33%. With camera alignment unchanged, recall at 0.5×, 1×, 1.5×, and 2× the tolerance was 4.51%, 70.64%, 85.25%, and 88.09%. These diagnostics expose sensitivity; no tolerance was retuned for acceptance.

Both tested alignments fail the declared recall and occupancy bands. The largest component was not recomputed after refinement, but refined recall alone fails the completeness rule. Surface fitting improves nearest-neighbor agreement with its own fitting target while worsening camera agreement. Neither transform is independently established as correct, and dominant near-planar surfaces may disproportionately determine the fit.

![Reference-to-subset distance maps before and after diagnostic refinement, using shared reference-derived PCA projections, common bounds, and fixed distance bands. Top and bottom rows show PC1/PC2 and PC1/PC3 projections. The four map panels are cropped unchanged from the full overlay-and-map figure preserved in the sensitivity report. Distance-map colors denote reference-to-subset disagreement: blue ≤ fine width, green ≤ tolerance, amber ≤ twice tolerance, red above twice tolerance. The dominant near-planar surface aligns better after fitting, while peripheral and below-plane disagreement persists. Red is not independently verified missing geometry; projections can hide depth differences. Full rendering details are in the sensitivity report.](figures/helenenschacht-distance-panels.png)

## 6. Discussion

### 6.1 What the equal-budget comparison establishes

Nominal image count did not determine the observed scores. Even excluding the alignment-confounded start burst, 103-image subsets differed in recall, occupancy, and derived verdict. This is consistent with established geometric network-design principles [9, 10], not evidence of a new optimal selection method. The tested removals alter overlap, viewpoint distribution, and reconstruction conditioning together; the study does not isolate each mechanism or establish causal effects transferable to other scenes.

### 6.2 Separate diagnostics, separate meanings

Internal screening concerns consistency among retained observations. Reference recall concerns tolerance-based agreement with another reconstruction. Occupancy concerns sampled spatial support. Their disagreement is informative, but none is independently validated task quality. Dense-reference recall and occupancy also share the same alignment and reference, so they are complementary operational scores rather than statistically independent quality measures.

The extreme Barn burst and the Helenenschacht refinement show why alignment diagnostics belong alongside these scores. A low score cannot alone distinguish absent geometry from drift, scale/pose discrepancies, local deformation, density differences, or reference errors. Conversely, improved fitted surface agreement need not imply improved camera accuracy.

### 6.3 Bounded practical interpretation

For this Barn recipe, uniform stride 3 met the declared bands and stride 4 did not meet preserved occupancy. That result does not justify telling a phone user to retain exactly one third of video frames. Distributed capture should preserve overlap and complementary viewpoints; it should not be framed as eliminating redundancy indiscriminately [10]. Inspecting geometry and reference disagreement in addition to registration is a reasonable diagnostic practice, not a validated guarantee of usability. Roof-, corner-, or material-specific capture requirements were not separately tested.

## 7. Reproducibility and Availability

The public research repository contains selection/evaluation code, schemas, tests, and 16 Barn experiment directories. Each includes a selection manifest, execution record, internal quality report, dense comparison JSON, and human-readable report. Filename lists, subset fingerprints, exact commands, recorded software versions, and stage outcomes allow inspection and recipe-based rerunning with separately obtained inputs. `paper/supplementary-results.md` maps table rows to exact experiment IDs and SHA-256 hashes of comparison files.

CI exercises research software on Linux, macOS, and Windows; it is not a cross-platform GPU replication campaign. Raw images, databases, dense clouds, meshes, and large derived outputs are not versioned. Absolute paths in archived execution records must be adapted on another machine. The repository is an auditable artifact package, not a guarantee of numerically identical reconstruction.

Helenenschacht is documented through the external-check, frozen-completeness, and alignment-sensitivity reports. Its selection manifests, pipeline logs, and large reconstructions remain local; it is not a complete portable public replication package. Surface-refinement and rendering procedures are described without new public sensitivity scripts or test code. This limits automated replication of that diagnostic.

- Research: <https://github.com/Gre3nLioN/photogrammetry-capture-research>
- Evaluation instrument: <https://github.com/Gre3nLioN/reconcheck>
- Barn source: <https://www.tanksandtemples.org/download/>
- Helenenschacht source: <https://github.com/OpenDroneMap/odm_data_helenenschacht>

Data use remains subject to upstream terms. Only derived report figures, not third-party paper PDFs or raw datasets, are redistributed here.

## 8. Limitations

**Scene and acquisition scope.** The primary campaign covers one Barn sequence. Helenenschacht adds one aerial pair, not a replicated multi-scene campaign. No phone video, user-task validation, reflective/vegetation test suite, or sensor-quality ablation was conducted. The ordered still-image proxy does not establish an actual frame rate.

**Reference and alignment.** The scored clouds are reconstructed references rather than independent truth. Shared errors can be rewarded, valid differences penalized, and whole-cloud background/outliers can affect scale. Camera-center agreement does not guarantee surface agreement. The start-burst result is strongly alignment-confounded; other Barn scores have not received equivalent surface-fitting checks. Helenenschacht fitting is optimized on the scoring reference and is not a correction established by ground truth.

**Exploratory rules and uncertainty.** Thresholds were calibrated after early result inspection. They are not preregistered, task-validated decision boundaries. One deterministic run per condition does not estimate stochastic, numerical, or platform uncertainty; there are no confidence intervals or significance claims. Near-boundary classifications may change under another run, alignment, sample, or threshold.

**Recipe and metric dependence.** Conclusions depend on the recorded COLMAP version, shared-camera assumption, exhaustive matching, dense resolution, defaults, fusion, and sampled cloud support. Barn and Helenenschacht use different dense resolutions. Occupancy is not a measure of texture, edge sharpness, surface normals, topology, or perceptual fidelity. File-order stride sampling is deterministic but not random or area-uniform; normalization and clipping do not remove every sampling or density bias. One-way recall does not penalize spurious extra geometry.

**Review and replication scope.** The literature review is targeted, not exhaustive, and no optimized selector is benchmarked. Public Barn artifacts are substantially more complete than the local-only Helenenschacht runs. These boundaries limit the work to descriptive exploration rather than a universal capture recommendation or fully replicated external validation.

## 9. Conclusion

Under the tested Barn recipe, a 137-image uniform subset met the declared recall and fine-occupancy bands; a 103-image uniform subset met completeness but not preserved occupancy. Equal-budget subsets produced different reference agreement despite uniformly good internal screening. That variation persists when the extremely alignment-confounded start burst is set aside, although no pure geometry-loss mechanism is established.

The Helenenschacht diagnostic further shows that reference metrics can change substantially with alignment while camera agreement worsens. Internal consistency, dense-reference recall, spatial occupancy, and alignment diagnostics should therefore be reported with distinct meanings and explicit limitations. This study establishes neither an exact minimum capture budget nor an optimal image selector, perceptual-quality metric, or general phone-video rule.

## Related Materials

- [[supplementary-results|Frozen Results and Artifact Map]] — full multi-scale scores, artifact IDs, and hashes.
- [[literature-review|Literature Evidence Map]] and [[subset-keyframe-review|Subset and Keyframe Review]] — source-verification and full-text notes.
- [[helenenschacht-alignment-sensitivity|Helenenschacht Alignment Sensitivity]] — fitting and rendering procedure.

## References

1. Schönberger, J. L., and Frahm, J.-M. (2016). *Structure-from-Motion Revisited*. CVPR, 4104–4113. <https://doi.org/10.1109/CVPR.2016.445>
2. Schönberger, J. L., Zheng, E., Frahm, J.-M., and Pollefeys, M. (2016). *Pixelwise View Selection for Unstructured Multi-View Stereo*. ECCV, 501–518. <https://doi.org/10.1007/978-3-319-46487-9_31>
3. Knapitsch, A., Park, J., Zhou, Q.-Y., and Koltun, V. (2017). *Tanks and Temples: Benchmarking Large-Scale Scene Reconstruction*. ACM Transactions on Graphics, 36(4), 1–13. <https://doi.org/10.1145/3072959.3073599>
4. Schöps, T., Schönberger, J. L., Galliani, S., Sattler, T., Schindler, K., Pollefeys, M., and Geiger, A. (2017). *A Multi-View Stereo Benchmark with High-Resolution Images and Multi-Camera Videos*. CVPR, 3260–3269. <https://doi.org/10.1109/CVPR.2017.272>
5. Scott, W. R., Roth, G., and Rivest, J.-F. (2003). *View Planning for Automated Three-Dimensional Object Reconstruction and Inspection*. ACM Computing Surveys, 35(1), 64–96. <https://doi.org/10.1145/641865.641868>
6. Kolev, K., Tanskanen, P., Speciale, P., and Pollefeys, M. (2014). *Turning Mobile Phones into 3D Scanners*. CVPR, 3946–3953. <https://doi.org/10.1109/CVPR.2014.504>
7. Snavely, N., Seitz, S. M., and Szeliski, R. (2008). *Skeletal Graphs for Efficient Structure from Motion*. CVPR, 1–8. <https://doi.org/10.1109/CVPR.2008.4587678>
8. Azimi, A., Hosseininaveh, A., and Remondino, F. (2022). *A Novel Geometric Key-Frame Selection Method for Visual-Inertial SLAM and Odometry Systems*. ISPRS Archives, XLIII-B2-2022, 9–14. <https://doi.org/10.5194/isprs-archives-XLIII-B2-2022-9-2022>
9. Hosseininaveh, A., and Remondino, F. (2021). *An Imaging Network Design for UGV-Based 3D Reconstruction of Buildings*. Remote Sensing, 13(10), 1923. <https://doi.org/10.3390/rs13101923>
10. Wenzel, K., Rothermel, M., Fritsch, D., and Haala, N. (2013). *Image Acquisition and Model Selection for Multi-View Stereo*. ISPRS Archives, XL-5/W1, 251–258. <https://doi.org/10.5194/isprsarchives-XL-5-W1-251-2013>

Machine-readable bibliography: `paper/references.bib`. The MVS author order follows the final Springer proceedings record, verified on 7 October 2026, rather than the differing author-hosted manuscript order.
