# Completed exploratory paper

**Image Budget and Viewpoint Distribution in Photogrammetry: An Exploratory Study**

- **Read the paper:** [10-page PDF](manuscript.pdf)
- **Editable source:** [Markdown manuscript](manuscript.md)
- **Frozen supplementary data:** [Multi-scale scores, alignment ratios, experiment IDs, and hashes](supplementary-results.md)
- **Final audit:** [Numerical, methodological, bibliographic, and rendering checks](manuscript-audit.md)
- **Publication route:** [Venue recommendation and author/submission checklist](submission-notes.md)
- **References:** [BibTeX](references.bib), [evidence map](literature-review.md), and [subset/keyframe full-text notes](subset-keyframe-review.md)

## Status and scope

Completed on 7 October 2026 as an exploratory technical report. It is **not peer reviewed, submitted, accepted, or formatted as an official conference paper**. Author identity/affiliation and required declarations have not been guessed. A suitable ISPRS workshop/Archives route is recommended conditionally, with general guidelines verified; no live event or deadline was selected.

The report includes all 16 Barn conditions, the Helenenschacht frozen/refined comparison, mathematical metric definitions, alignment diagnostics, public/local replication boundaries, and ten verified citation identities. All main and supplementary Barn rows and comparison-file hashes were checked against the unchanged artifacts.

The principal interpretation was tightened during the final audit: the start burst's camera RMSE is 31.46 fine cell widths, so its very low scores cannot establish pure missing geometry or a cadence-only effect. Differences remain among the other equal-budget conditions. Spatial occupancy is not a validated perceptual detail metric, and no general phone-video fraction or exact minimum is claimed.

## Figures

- [Equal-budget comparison, SVG](figures/coverage-detail-summary.svg) — editable/vector source showing all thirteen 103-image conditions.
- [Equal-budget comparison, PNG](figures/coverage-detail-summary.png) — 2400 × 2160 rendering used in the PDF.
- [Helenenschacht distance panels](figures/helenenschacht-distance-panels.png) — unchanged crop of the original four fixed-band distance maps, with readable labels.
- [Complete Helenenschacht overlays/maps](figures/helenenschacht-alignment-overlays.png) — original eight-panel diagnostic figure, retained for inspection.

The PDF title, Table 1, and both figure pages were visually inspected at reading size. Captions are rendered from Pandoc table captions and image descriptions, so they remain attached and are not numbered twice.

## Rebuild the neutral PDF

Rendering uses **Pandoc 3.8.2**, **Typst 0.14.0**, and fonts specified in [render-metadata.yaml](render-metadata.yaml). Tools are not added as research runtime dependencies. From the research repository root on Linux/POSIX, with `pandoc` and `typst` on PATH:

```bash
pandoc paper/manuscript.md \
  --from=markdown+wikilinks_title_after_pipe \
  --standalone --shift-heading-level-by=-1 \
  --metadata-file=paper/render-metadata.yaml \
  --pdf-engine=typst --pdf-engine-opt=--root=/ \
  --resource-path=paper \
  --output=paper/manuscript.pdf
```

The Typst root option permits Pandoc's temporary media paths; render only trusted local sources. This is a document-rendering command, not a reconstruction or sensitivity runner. PDF creation metadata may differ between rebuilds; no byte-identical-PDF claim is made. Pandoc 3.8.2's mapping of set intersection emits a Typst deprecation warning, but the equations render correctly.

To recreate the two presentation-only image assets, with librsvg/ImageMagick installed:

```bash
rsvg-convert --width=2400 --height=2160 \
  paper/figures/coverage-detail-summary.svg \
  --output=paper/figures/coverage-detail-summary.png

magick paper/figures/helenenschacht-alignment-overlays.png \
  -crop 940x915+980+100 +repage \
  paper/figures/helenenschacht-distance-panels.png
```

No new public sensitivity scripts or test code are included. The original evaluator, classifications, and reconstruction measurements remain unchanged.

## Next action

The research deliverable can stop here. Actual scholarly submission requires author details, a live venue choice, the current venue template/citation format, any necessary anonymization, policy/declaration checks, and human approval. See [submission-notes.md](submission-notes.md); additional experiments should be driven by that venue's expectations, not presented as already completed.
