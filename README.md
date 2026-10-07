# Photogrammetry Capture Research

An exploratory study of image budget and viewpoint distribution in photogrammetry. The project uses [ReconCheck](https://github.com/Gre3nLioN/reconcheck) as a separate measurement instrument; it does not develop or duplicate ReconCheck itself.

**Completed report:** [PDF](paper/manuscript.pdf) · [Markdown](paper/manuscript.md) · [Supplementary frozen results](paper/supplementary-results.md). This is an exploratory technical report, not a peer-reviewed publication.

## Research question

> How do image budget and distribution affect internal screening, dense-reference agreement, and spatial occupancy under one recorded reconstruction recipe?

The completed campaign comprises 16 deterministic Barn runs and one additional full/subset Helenenschacht check. Reconstructed references are not ground truth, and the extreme Barn start burst is strongly alignment-confounded. The report does **not** establish an exact minimum budget, perceptual usefulness, an optimal selector, or a general phone-video rule. Broader image-quality studies and practical guidance remain future work.

## Data immutability

Raw datasets are source-of-truth inputs. This repository never modifies them.

- `datasets/` contains manifests and references only, never raw image copies.
- A controlled subset is represented by an ordered manifest of source image IDs.
- Any resized, compressed, blurred, or otherwise degraded image is written under that experiment's derived run directory only.
- Each report records source and subset fingerprints, so results cannot silently be attributed to changed input data.

## Broader planned study tracks

1. **Coverage and frame rate** — uniform decimation, random subsets, trajectory gaps, removed sectors, reduced obliquity, and one-sided capture.
2. **Phone image budget** — resolution, JPEG compression, blur, noise, exposure variation, and clipping.
3. **Capture discipline** — overlap, duplicate-heavy captures, focal-length changes, and calibration/model errors.
4. **Reconstruction sensitivity** — separately controlled reconstruction settings; never conflated with capture changes.

## Experiment contract

```text
experiments/<experiment-id>/
├── experiment-manifest.json   # hypothesis, source, selection, transformations
├── execution.json             # reconstruction recipe, timings, tool versions, status
├── reconcheck-quality-report.json
├── comparison.json            # baseline deltas and quality-profile transitions
└── report.md                  # human-readable result and limitations
```

The broader protocol calls for stochastic conditions to use at least three recorded seeds; none was part of the completed deterministic core campaign. Deterministic conditions record a selected-image list and subset SHA-256. Single-run results do not estimate reconstruction uncertainty.

## First protocol

`protocols/01-coverage-and-frame-rate.md` defines the broader exploratory capture-reduction protocol. The completed report describes the tested conditions rather than claiming that they locate a minimum or finish every planned study track.

## CLI

```bash
uv run pcr create \
  --id barn-stride-5 \
  --baseline /path/to/baseline-quality-report.json \
  --strategy stride --every 5

uv run pcr compare \
  --experiment experiments/barn-stride-5 \
  --quality-report /path/to/experiment-quality-report.json
```

`create` produces only a manifest. It does not alter raw images or invoke COLMAP. `compare` records an independently generated ReconCheck report and calculates metric deltas against the validated baseline.

## Documents

- `paper/` — completed technical-report manuscript/PDF, figures, verified bibliography, artifact audit, and publication-route checklist.
- `guidance/` — intended guidance track; recommendations must remain bounded by completed evidence and must not be described as validated phone-video rules.
