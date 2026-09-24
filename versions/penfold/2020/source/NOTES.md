# Penfold, the old live page (2020)

Rebuilt 2026-09-24 with the image2code skill from the Figma section
"Penfold _new" > Section 1 (120:5410).

## Sources

- `screenshots/` - the old live page, six captures taken 2024-07-07. 4096 px wide: 2x of a
  2048 px browser window, so one CSS pixel of the old site is two image pixels. They overlap
  and were aligned on their shared rows (worst seam difference 1.3 levels), then measured as
  one page 5776 px tall.
- `originals/hero`, `originals/sketches`, `originals/craft` - the Figma frames that were on
  the page, exported at 2x/3x, with the raw images inside them. The page uses them at 2x of
  their 980 px width. craft's export carries an 80-unit shadow margin, cropped off.

## The page, in the old site's CSS pixels

- Column 980 wide, centred. Intro: two columns of 479 with a 22 gap. Section text: a 578
  column, centred (x 201 in the page).
- Helvetica Neue throughout (the Mac system face; no web font was served, so none is here).
  Body 11/17, 0.4 letter spacing, #757575. Headings bold 13.5, #333. Title bold 60, 0.6
  spacing, black. Footer headings bold 10, links 8.
- Transactions captions: IBM Plex Mono 500, 12/16, #0E3153 (vendored in `site/_vendor`).
- Beneficiary and Transactions bands: #EEEEEE, 551.5 and 552 tall. Four screens each,
  191 x 414, radius 15, at x 52 / 280.5 / 508.5 / 737 in the column; soft shadow.
- Milestones: a #FBFBFB panel 980 x 1225.5; twelve phones in slots of 198.5 x 346.5 on a
  222 x 408.5 grid. Each slot holds the device and its shadow (the render has no crisp
  device edge to clip to).
- Every image slot has a fixed box. Replacing an image with an original keeps placement.

## How close

- Every text line lands within 1 px of the source; 61 of 62 within 0.5 px. Line widths
  within 1.5 px.
- Snapped: letter spacings to 0.05 steps; the footer link line height to 15.3.
- Not recovered: the site's own header (the Figma frame starts below it), the link targets
  (App Store, Play Store, NEXT, footer), exact colours of the lossy screenshot fills.
- The live hero also showed App Store / Google Play / Trustpilot badges and the Penfold logo
  on its left, over a different crop. The original hero frame is the plain device photo,
  and that is what is used.
- Copy is verbatim, typos included ("notifcations", "helpfull" in the montage).
