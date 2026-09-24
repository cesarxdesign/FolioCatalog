# Starcount Observatory, Sqsp: the live page on the 2020 Squarespace site

Rebuilt 2026-09-24 with the image2code skill from the Figma frame 87:72082 in "-cxd.com".

## Sources

- `screenshots/` - four captures of the old live page, taken 2024-07-23, 4096 x 2304 each: 2x of
  a 2048 px window, so one CSS pixel is two image pixels. They overlap by 94, 105 and 1810 rows;
  aligned on the shared rows (seam differences 0.09, 0.36, 1.05 levels) into `page.png`,
  7111 image px (3555.5 CSS px). The page starts where the Figma frame does, 24 px above the
  column, inside the bottom of the #FAFAFA site header.
- `build/` - the measuring, fitting and verification scripts.

## The page, in the old site's CSS pixels

- Column 980 (measured 980.4), centred. Same template as the Penfold and Mara pages: Helvetica
  Neue, body 11/17 #757575, headings bold 13.5 #333, title bold 60.
- Body letter spacing 0.39 (at 0.4 one line in the second section wraps differently).
- Second section top margin 85.85. The 2x2 screen grid: boxes 482.2 x 271.2, gaps 15.8
  (columns) and 16.4 (rows). Footer link line height 15.5.
- The hero carried the "STARCOUNT / OBSERVATORY" wordmark baked in. It is painted out of the
  picture and set as live text, colour #F6F6F6:
  - STARCOUNT: Bodoni Moda 500, 15.2 px, letter spacing -1.8. The original face looks like
    Bodoni 72 Book, a macOS system font that cannot be redistributed; Bodoni Moda (OFL) fits
    the measured width and height exactly.
  - "/": IBM Plex Sans weight 250, 21.3 px. OBSERVATORY: IBM Plex Sans weight 575, 15.7 px.
- Pictures, each in a fixed box so an original can replace it: the hero, the grey usage panel,
  the four screen crops, the desk photo.

## How close

- 33 text bands: 32 within 0.5 px, all within 1 px (worst: the title, 0.73). Line widths
  within 1 px. Wordmark pieces within 0.5 px. Image blocks at zero shift.
- Not recovered: the typefaces are visual matches; the site header above its last 24 px; link
  targets (starcount.com/observatory, NEXT, footer), inert text here; exact colours of the
  lossy screenshot fills. The macOS screenshot thumbnail in the corner of each capture is left out.
