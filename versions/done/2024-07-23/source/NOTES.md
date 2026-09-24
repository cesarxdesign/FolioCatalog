# DONE, Done2: the Figma frame "06 Done2 _air"

Built 2026-09-24 with the figma2code skill from CG-Folio-WIP, node 15:3578 (1920 x 20434,
11 sections). `build/` holds the scripts used to build and verify it.

## What is what

- Live text: all narrative text - the 02 summary card and details, the 03 schedule and list,
  every heading, paragraph and caption. The 03 box and rules, the 06 fades and the 07 background
  are CSS.
- Figma renders: the hero, the emoji, the 04 hexagon glyph and card grid, the phone rows in
  05, 06, 08, 09 and 10. Where a mockup sits on a patterned background (06 grid, 07 gradient,
  11 grid) it is a crop of the section's render, since Figma exports carry their background.
  07 is one plate with holes where the live text sits.
- Images are AVIF 4:4:4 with WebP q88 fallback, at 1x and 2x. Fonts: Roboto, Roboto Italic and
  Roboto Mono (variable), in `site/fonts`.

## How close

Headless Chrome from file://, 1920 wide, against Figma's render of each section: 0.166% of
pixels differ by more than 24 levels overall, all on glyph edges (per section 0.000-1.373%).
All 38 live strings wrap as in Figma; text blocks within 0.12px (the centred 08 intro 0.43px).

Not matched: the emoji is 1x only (Figma's exporter has no emoji font); list number offsets are
taken from Figma's render (the API does not expose them); faint shadow edges under the 07 text
holes (<=3 levels); the page frame's 24px corner radius (white on white).

The page shrinks itself to a 1280 column in a browser; `#1x` shows it at 1920, as the catalog does.
