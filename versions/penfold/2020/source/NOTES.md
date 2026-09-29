# Penfold, Sqsp: the live page on the 2020 Squarespace site

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

## Montage notes as live text (2026-09-24)

The six handwritten notes on the craft montage ("Review copy. Tighten, more clear.", "More
contrast check WCAG", "Check touch targets", "Not helpfull for small values", "Allows
unconsistent state", "Spacing": Figma text nodes 120:5392-5397) are now live HTML text, placed at
their Figma x/y in the 2212 x 1416 frame scaled by 980/2212, 44/1.05 black. `img/craft.webp` is
`originals/craft/export.png` with only those six text areas painted out: the frame's #FAFAFA, and
where a note overlaps Frame 3 (120:5380, "Spacing" and "Tighten") that frame's own 3x export;
no coloured pixel was touched. The crop was also corrected: the export's shadow margin is 80 left
and right but 76 top / 84 bottom (shadow offset y 4), so the old crop sat 4 units high and ended in
a 2 px black strip. Figma's font is Journal (Fontourist), which is not in google/fonts, so it is
not shipped; Loved by the King (OFL, `site/fonts/`) stands in, with size-adjust 75% to match
Journal's line widths and ascent/descent overrides that put the baseline where Journal's was.
The unedited frame stays in `originals/craft/export.png`.

## Montage rebuilt as code (2026-09-29)

`site/craft.html` replaces `img/craft.webp` (now unused) so the montage can be edited. It rebuilds
the craft frame (120:5379, 2212 x 1416) whole: Frame 3's two 2020 screenshots become the 12 Estimate
screens coded from Figma "05 Estimate" (kt8yiHLl862LQIAT8GLvkP, section 10:4927), drawn twice,
once in Figma's outline mode (left of the diagonal) and once in colour (right of it, clipped by
Rectangle 1 with Rectangle 2's shadow). On top: the file's 59 prototype links, read with the Plugin
API and drawn as connectors, Figma's frame selection and badges, then the orange marks, the six
notes (moved here from index.html, same Loved by the King stand-in) and the elbow arrows at their
Figma transforms.

- Each screen's 2020 state is the `STATES` table: the file now holds every toggle off and every
  field empty. Values the file lacks were read from the 2020 screenshot (`originals/craft/raw3.png`):
  filled fields #FBFBFB, the 87% dot #4CD964, toggles on #FF5081.
- Canvas zoom in the screenshot: 0.617363 craft units per canvas unit (screen edges 562 px apart
  at 2x for 455 units), frame corner at (47.5, 43.5) in Frame 3.
- Connector routing is not in the API; the curves leave the hotspot's right-middle sideways and
  enter the facing edge of the destination (its side on the same row, its top or bottom across rows).
- Outline mode: shapes solid, frames and groups dashed (6.5/3.2), 1 screen px (1.62 canvas units),
  glyphs stroked. It mimics Figma's Outline view; it is not Figma's renderer.
- SF Pro Text (status bar) is not shipped; the system font stands in. Montserrat is the variable
  OFL font in `site/fonts/Montserrat.woff2`.
