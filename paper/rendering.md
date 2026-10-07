---
title: Photogrammetry Report Rendering Notes
type: synthesis
tags: [life, work, photogrammetry, documentation]
created: 2026-10-07
updated: 2026-10-07
sources: [paper/manuscript.md, paper/render-metadata.yaml]
---

# Photogrammetry Report Rendering Notes

Document-maintenance instructions for the neutral report PDF and its presentation assets, kept separate from the reader-facing paper summary.

## Key Points

- The PDF is a neutral technical report, not an official venue template.
- Rendering does not rerun reconstruction or change frozen measurements.
- These commands are not sensitivity runners; no new public sensitivity script or test code is provided.

## Details

### Rebuild the PDF

Rendering uses **Pandoc 3.8.2**, **Typst 0.14.0**, and the fonts in [render-metadata.yaml](render-metadata.yaml). These tools are not research runtime dependencies. From the research repository root on Linux/POSIX, with `pandoc` and `typst` on PATH:

```bash
pandoc paper/manuscript.md \
  --from=markdown+wikilinks_title_after_pipe \
  --standalone --shift-heading-level-by=-1 \
  --metadata-file=paper/render-metadata.yaml \
  --pdf-engine=typst --pdf-engine-opt=--root=/ \
  --resource-path=paper \
  --output=paper/manuscript.pdf
```

The Typst root option permits Pandoc's temporary media paths; render only trusted local sources. PDF creation metadata may differ between rebuilds; no byte-identical-PDF claim is made. Pandoc 3.8.2's mapping of set intersection emits a Typst deprecation warning, but the equations render correctly.

The manuscript's author metadata renders Ivan Roumec's name, independent-researcher affiliation, and contact email. Its AI Assistance section records Codex/AI assistance separately from authorship.

### Presentation assets

With librsvg and ImageMagick installed:

```bash
rsvg-convert --width=2400 --height=2160 \
  paper/figures/coverage-detail-summary.svg \
  --output=paper/figures/coverage-detail-summary.png

magick paper/figures/helenenschacht-alignment-overlays.png \
  -crop 940x915+980+100 +repage \
  paper/figures/helenenschacht-distance-panels.png
```

The first command rasterizes the vector figure. The second retains the four existing distance-map panels unchanged; no point, distance band, or score is recomputed. The complete eight-panel overlay figure remains available.

### Check the result

- Verify the author/contact and AI disclosure in extracted PDF text.
- Inspect the title, complete result tables, and both figure pages at reading size.
- Ensure captions stay with figures/tables and are not numbered twice.
- Keep the reader-facing README's abstract and summary consistent with the manuscript.

## Related Pages

- [[manuscript]]
- [[manuscript-audit]]
- [[helenenschacht-alignment-sensitivity]]

## Source Notes

These instructions were moved from `paper/README.md` when it became a content summary. The PDF, manuscript, frozen evaluator, and measurements were not changed by that documentation reorganization.
