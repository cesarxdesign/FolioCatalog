# Starcount, Figma: the "Audiences _air" frame

Built 2026-09-24 with figma2code from Figma Z9p4dGIT13UAJSSESrOAd5 "-cxd.com", frame
"Audiences _air" (94:129652), 1920 wide, 14 sections. `build/` holds the build and diff scripts.

## How close

Diffed against Figma's scale-1 renders: 0.107% of pixels off by more than 24 levels overall;
every section at or under 0.31%. What remains is glyph edges. All 81 live text blocks (268
lines) sit within 0.3 px of Figma and wrap to the same number of lines.

## Text

- Live: titles, body copy, the annotation callouts in 08, 10 and 12, the 04 labels, the 11
  "Original" / "Re-balanced" labels and captions, the 07 wishlist box (CSS).
- Taken out of renders (painted out with what Figma has underneath, set live on top): the
  plates for 04, 06, 08, 09, 10, 11, 12 and 14; in 08 the blurred map backdrop is exported alone.
- Renders: the hero (its Starcount / Audiences logo is a vector shape), partner logos, product
  screens, the 11 heatmaps, all of 13 (product UI), the SF Symbol glyph in 09.

## Fonts and adjustments

Roboto, Roboto Italic, Roboto Mono, Roboto Mono Italic, IBM Plex Mono Medium (all OFL/Apache,
vendored). Measured adjustments: Roboto Mono tracking +0.0095 px (Chrome sets it narrower),
smaller corrections for Roboto Light 32 and Bold 69; 22 px Roboto / Roboto Mono 1 px lower;
fi/fl ligatures forced; bullet positions from the render; the faked "st" of "1st" sized from
the render. Not matched: the "CRM upload" strikethrough is 1 px where Figma draws ~1.1; in 08
the backdrop behind the annotations lacks the mockup shadow (a few levels).
