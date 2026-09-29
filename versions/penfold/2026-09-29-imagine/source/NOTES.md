# Penfold, Imagine (2026-09-29)

The Color page (2026-09-29-color) with images. Color itself stays text only.

## Images

Exported whole from the Figma file `__Folio-study` and kept in CodeCatalog under `images/penfold/`.

| Image | Figma node | Where |
|---|---|---|
| `img/hero.webp` | 45:1144 | Hero, between the lede and the numbers, as on the live Cable page: full width, 600px tall, cropped to fit |
| `img/sketches-strip.webp` | 45:884 | Shipping, between the first paragraph and the day-by-day paragraph; the onboarding strip follows that paragraph |

## The onboarding row

Under the sketches: the first onboarding as one strip of 10 screens that fits the text column, no
sideways scroll. Each is the live CodeCatalog desktop screen in its longest state, shown whole (3 things
with all three sections open, the calculator with the whole plan, plans through to risks accepted, the
sign-up form filled). The strip has five columns, 166px each, laid out by hand from Cesar's own arrangement of the exported PNGs:
3 things, sign-up upper | savings path, calculator | plan selection | sign-up form, docs |
monthly payment, standing order, confirmation. Enter your email is not a screen of its own: its field is
added to the sign-up upper half, before the password. All columns are the height of the tallest
(sign-up form + docs); a column's spare height is shared between its frames, as room at the bottom of each. Built by `source/flow33.py`.

No bars or step numbers under the screens (removed by request).
A dot at the top right of each frame counts the pages, 1 to 9, in reading order (down each column, left to
right); the last page carries a tick instead of a 10. Step counts and colour dots were removed by request. The steps each screen covers, 01 to 33,
are kept in its `data-steps` attribute; the docs screen is four steps, one per doc.

Left out by request: the assumptions dialog and the "Hold on while we run some checks" screen.
The all-docs-accepted state is not in CodeCatalog and is not shown; to be revisited.
Montserrat and Roboto Mono are in `site/_vendor/` for these screens.

## Background

The page colours are the live Penfold page's, read from `Portfolio/penfold/index.html` on 2026-09-29:

| | Light | Dark |
|---|---|---|
| Background | #f2f5f7 | #101519 |
| Ink | #151515 | #eef0f2 |
| Body | #5b6470 | #b3b7bd |
| Muted | #98a0a8 | #7c8188 |
| Label ink | #6b737b | #8b9198 |
| Line | #e7e8ea | #2a2d33 |
| Accent | #6076DD | #6076DD |
| Accent, light end | #98a6e9 | #b7c1f0 |
 The sketches image is blended with multiply in light, so its white paper takes the page colour.

## Frame sizes in the strip

No frame is shorter than 900px of screen (126px on the page, a 4:3 frame), and every screen keeps at least
170px of its own space under its last element, so short screens still read as screens and the dot sits clear.

## Sketches, darker

`img/sketches-strip.webp` is the Figma export multiplied by itself three times (each pixel cubed), the same as
stacking three copies with multiply. The untouched export is in CodeCatalog, `images/penfold/sketches-strip/`.

In dark the sketches are inverted and blended with screen: white ink, and the paper takes the dark page colour.

## Module colours

The colour dots are off the frames (removed by request); each frame keeps its colour in `data-module`. The colours on the flow picture were picked at
random and read badly (yellow invisible, amber close to red), so they are replaced by this set. Reuse these for
the modular onboarding.

| Screens | Colour |
|---|---|
| 3 things, savings path | pink #D6409F |
| sign-up with email | orange #F76B15 |
| savings calculator | cyan #00A2C7 |
| plan selection | purple #8E4EC6 |
| sign-up form, document consent | indigo #3E63DD |
| monthly payment, standing order, confirmation | green #46A758 |

## Grid annotation

Annotations on the grid follow the live Cable page's design: a ring on the screen, a line out to a caption in the
left gutter (title and short text). First one: "Optimised for launch.", Cesar's title and content, tightened (2026-09-29). Earlier: "Unoptimized." Before that: "Speed over sequence." (the copy owns the trade-off and never blames the proof of concept). Before that: "Nobody would ask in this order." (earlier: "Unfamiliar sequence.", "Related questions, far apart.", "The order the code needed."), ringing the two screens that ask for personal
details (sign-up with email, sign-up form). A line leaves each ring: the one from the sign-up form runs under the
screens and shows only in the gaps between columns. A bracket in the gutter joins the two, with the caption at its middle.
Copy and ring targets are in `ANNOTATIONS` in `flow33.py`.

## Column 2

Savings path stays at its least height (4:3) and the calculator takes the column's spare height, so the gap between
them sits well above the annotation line that runs under the screens. The calculator's lower half was opened up in
CodeCatalog the same day, which also made it longer.
