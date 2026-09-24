# DONE, Figma: the "06 Done _folio" frame

Built 2026-09-24 with the figma2code skill from Figma file 9Hmml1HBkNn8rMcn3KlK2R, node 88:4103
(1920 x 19325, 13 sections). `build/` holds the scripts used to build and verify it.

## What is what

- Live text: all narrative text - headings, paragraphs, captions, callouts, the role/dates/details
  block and the list. Quote marks, corner brackets, star, dashed rules, arrow and leader lines are
  Figma's own SVGs, inlined.
- Figma renders (2x WebP q88; 1x lossless WebP for UI renders, q88 for the photographic 06 and 09):
  the hero, sections 06 and 13 whole (no text), all phone mockups and the photo strip, and the one
  SF Symbol icon in 12.
- Fonts in `site/fonts`: Roboto, Roboto Italic, Roboto Mono (variable, from the cable-air build),
  Roboto Slab and Roboto Mono Italic (google/fonts, subset to Latin).

## How close

Headless Chrome from file://, 1920 wide, against Figma's render of each section: 0.227% of pixels
differ by more than 24 levels overall (per section 0.000-1.291%), antialiasing and sub-pixel
placement on thin text. 169 text lines within 2px of Figma's render; all 65 text boxes at Figma's
heights; every paragraph wraps as in Figma.

Set by judgement: small caps on the quote, the three zone labels, "live testing", "Onboarding" and
"Home" (the API does not report small caps; the renders show them); the list indent 26.7px as
Figma renders it (the API says 33); three text styles moved down 1px to Figma's baseline; a 28px
space after the section 12 icon. SF Pro cannot be shipped, so that icon is a render. 2x images
were not pixel-checked.

The page shrinks itself to a 1280 column in a browser; `#1x` shows it at 1920, as the catalog does.
