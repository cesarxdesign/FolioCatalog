# DONE, Sqsp: the live page on the 2020 Squarespace site

Rebuilt 2026-09-24 with the image2code skill from the Figma frame 87:72052 in "-cxd.com".

## Sources

- `screenshots/` - six captures of the old live page, taken 2024-07-07, 2x of a 2048 px window
  (one CSS pixel is two image pixels). Overlaps 199-1103 rows; each pair joined at its
  lowest-error row into `page.png`, 11075 image px, exactly the Figma frame.
- `build/` - the stitching, measuring and verification scripts.

## The page, in the old site's CSS pixels

- Penfold template (column 980, Helvetica Neue body 11/17 #757575, headings bold 13.5 #333),
  with every margin re-measured. Body spacing 0.39; text column 579 at x 200.5; title 61.3 px,
  -0.1 spacing.
- Bands: grey #E8E8E8 (551 and 551.5 tall), dark panel #424747 (817 tall).
- Screens 161 x 348.5, radius 17, or scaled SE / 8 / 8 Plus (square) and X / Max (radius 17);
  shadow 0 1.5px 3.5px rgba(0,0,0,.2).
- Captions: IBM Plex Mono 500 8.2 px #424747; "touch target" Plex Mono 600 8.15 px. The lilac
  swatch is CSS.
- Text taken out of pictures: the band captions, and the hero's App Store rating ("5.0",
  "out of 5", star-row counts), painted over in the hero's #2F2F2F and set as live text
  (Helvetica Neue stands in); the rating bars stay in the picture.
- Kept in pictures: the "Download on the App Store" badge and the DONE WORKOUTS wordmark
  (logos), the handwriting in the scanned sketches, UI text inside screens.

## How close

- 47 text lines: 46 within 0.5 px, all within 1 px (max 0.6). 23 small items (captions,
  label, rating) within 0.5 px. Every picture and band edge exact; mean difference 0.7 levels.
- Differences: the top 24 px is white (template) rather than the header's #FAFAFA strip; a
  0.25 px seam in the sketches where two captures join.
- Not recovered: link targets (stores, NEXT, footer), the site header, the rating block's
  real fonts.
