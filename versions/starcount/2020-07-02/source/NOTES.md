# Starcount Audiences, Sqsp: the live page on the 2020 Squarespace site

Rebuilt 2026-09-24 with the image2code skill from the Figma frame 87:72061 in "-cxd.com".

## Sources

- `screenshots/` - five captures of the old live page, `1-top` to `5-footer` in page order, 2x
  of a 2048 px window (one CSS pixel is two image pixels). Overlaps 226, 274, 162, 1322 rows;
  seams differ by at most 9 levels on text rows. Stitched into `page.png`, 9440 image px, the
  Figma frame's height, starting 48 image px into the first capture. `6-patch-...` is the Figma
  patch 87:72067, a capture of the Penfold page; not used.
- `build/` - the measuring, fitting and verification scripts.

## The page, in the old site's CSS pixels

- Penfold template (column 980, Helvetica Neue body 11/17 #757575, bold 13.5 headings, #F5F5F5
  band, divider, NEXT, footer), with: body spacing 0.385; text column 579 at x 200.5 (the only
  width at which all 26 section lines wrap as in the source); title 61 px, 0.05 spacing;
  divider 0.5 #DDDDDD.
- The hero's "STARCOUNT / AUDIENCES" wordmark is painted out of the picture and set as live
  text, #FEFEFE: STARCOUNT in Bodoni Moda 500 15.2 px, -1.8 spacing (OFL, standing in for
  Bodoni 72 Book, a macOS font that cannot be redistributed); "/" IBM Plex Sans 300 21.5 px;
  AUDIENCES IBM Plex Sans 500 15.8 px, -0.2 spacing.
- Pictures, each in a fixed box: hero, the grey band of windows, three design stages, the flow
  board, four grid screens, the MacBook.
- The flow board keeps its ~45 small artboard labels ("Audiences Home Copy 3" ...) in the
  picture: they are the design tool's layer names, crossed by connector arrows.

## How close

- 48 text lines: 47 within 0.5 px, all within 1 px (the outlier "market.", bottom 1.0 off).
  Line widths within 1 px. Whole-page mean difference 1.06 levels.
- Not recovered: the site header (a 24 px sliver in the frame, left out as in the template),
  link targets, the true image colours and originals, the real font files.
