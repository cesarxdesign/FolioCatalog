# Mara, Sqsp: the live page on the 2020 Squarespace site

Rebuilt 2026-09-24 with the image2code skill from the Figma frame 87:72069 in "-cxd.com".

## Sources

- `screenshots/` - four captures of the old live page, taken 2024-07-07, 2x of a 2048 px window
  (one CSS pixel is two image pixels). They overlap by 248, 223 and 862 rows; aligned on the
  shared rows (seam differences 0.5, 1.3, 0.2 levels) into `page.png`, 3893.5 CSS px tall from
  the top of the Figma frame. `5-...-patch.png` is a Penfold capture Figma used only to patch a
  bit of footer; it is not used here.
- `build/` - the stitching, measuring, fitting and verification scripts.

## The page, in the old site's CSS pixels

- Same template as the Penfold and Starcount pages: column 980, Helvetica Neue body 11/17
  #757575, headings bold 13.5 #333, title bold 60, text column 578 at x 201, same footer.
- Mara's own: a 24.2 #FAFAFA strip at the top (the bottom of the site header); divider 0.5
  #DDDDDD, 579 wide; NEXT button 60.65 x 27.17; three #EEEEEE bands about 403.7 tall; phones
  135.33 x 300.79 (iPhones 138.8 x 298.46), radius 6, shadow 0 0 8px rgba(0,0,0,.1).
- Text taken out of pictures (painted over in the picture's own fill, set as live text):
  - hero: the App Store / Google Play badge wording, in the system UI face fitted to the
    measured widths;
  - sketch board: "Mara app 2.0", DM Sans 700 66.5 px, -0.45 spacing (OFL, vendored);
  - montage: "Screens: 24 down to 8 / 66% reduction", Inter;
  - redesign band: the "Mara app 1.0 / 2.0" captions, Inter.
- Kept in pictures: the Mara logo, the handwriting on the sketch board, UI text inside screens.
- Pictures, each in a fixed box: the hero, the sketch board, the montage, 11 phone screens, the arrow.

## How close

- 44 text lines: 40 within 0.5 px, 42 within 1 px, worst 1.5 ("Google Play" +1.5,
  "components." -1.5, where the row profiles match and it looks like a measurement quirk).
- Not recovered: the site header; link targets; the badges' real fonts; exact colours of the
  lossy fills; the sketch board's dot grid where the title was painted out.
