# Mara, Figma: the "MARA _air" frame

Built 2026-09-24 with figma2code from Figma Z9p4dGIT13UAJSSESrOAd5 "-cxd.com", frame
"MARA _air" (98:75481), 1920 x 32962, 17 sections. `build/` holds the build and diff scripts.

## How close

Diffed against Figma's own 1x renders: 0.224% of pixels off by more than 24 levels overall.
Every section is at or under 0.24% except 10 (2.5%: Figma resamples the pencil sketches at a
fractional position and softens them; the page shows the sharper node export). All 192 live
text lines break where Figma breaks them.

## Text

- Live: all 68 text nodes outside the phone screens, the whole 02 summary, the callouts, the
  "136px" / "61px" labels, the "benjamin button" heading, the bullet list, the flow labels and
  the giant outlined "4.0".
- Taken out of renders (painted over, set live on top): 07 drawer row labels, the 07
  Component Analysis list, the 11 components note. 04 and 16 are cropped so their callouts and
  flow labels fall outside the image; 10's sketches are exported alone.
- Renders: the hero, phone and desktop mockups, pencil sketches and highlight boxes, two SF
  Symbol glyphs, the warning glyph and the thumbs up/down emoji (alt text only).

## Fonts and adjustments

Roboto, Roboto Italic, Roboto Mono (variable), vendored in `site/fonts`. SF Pro and the emoji
font are not shipped. Measured adjustments, each commented in the CSS: letter spacing +0.002 to
+0.02 px per style (Figma sets these faces slightly wider); Roboto / Roboto Mono 22 px text 1 px
lower; fractional right padding on two negatively tracked paragraphs; fi/fl ligatures forced;
bullet position from the render; the four dividers in 05 and 08 one stroke width higher.

Not matched: Figma's linear burn is approximated with multiply; the "4.0" outside stroke is
centred in CSS.
