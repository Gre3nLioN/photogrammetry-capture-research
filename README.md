# Photogrammetry Capture Research

A reproducible study of the minimum capture resources needed for useful photogrammetry. The project uses [ReconCheck](https://github.com/Gre3nLioN/reconcheck) as an independent measurement instrument; it does not develop or duplicate ReconCheck itself.

## Research question

> Given a high-quality reference capture, which reductions in coverage, image count, resolution, and image quality still produce a reconstruction that passes a declared quality profile?

The intended outcome is both an academic paper and practical phone-capture guidance. Results measure internal reconstruction consistency unless a reference geometry is supplied; they do **not** claim absolute geometric accuracy without ground truth.

## Data immutability

Raw datasets are source-of-truth inputs. This repository never modifies them.

- `datasets/` contains manifests and references only, never raw image copies.
- A controlled subset is represented by an ordered manifest of source image IDs.
- Any resized, compressed, blurred, or otherwise degraded image is written under that experiment's derived run directory only.
- Each report records source and subset fingerprints, so results cannot silently be attributed to changed input data.

## Study tracks

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

Every stochastic condition is repeated for at least three explicitly recorded seeds. Conditions that select images deterministically record an explicit selected-image list and subset SHA-256.

## First protocol

`protocols/01-coverage-and-frame-rate.md` defines the initial controlled study: the minimum temporal sampling and camera-sector coverage that preserve a `good` ReconCheck result.

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

- `paper/` — academic manuscript, figures, methods, and bibliography.
- `guidance/` — practical capture guidance derived only from completed, cited experiment conditions.
