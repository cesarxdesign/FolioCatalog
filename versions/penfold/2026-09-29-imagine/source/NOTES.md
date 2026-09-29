# Penfold, Imagine (2026-09-29)

The Color page (2026-09-29-color) with images. Color itself stays text only.

## Images

Exported whole from the Figma file `__Folio-study` and kept in CodeCatalog under `images/penfold/`.

| Image | Figma node | Where |
|---|---|---|
| `img/hero.webp` | 45:1144 | Hero, between the lede and the numbers, as on the live Cable page: full width, 600px tall, cropped to fit |
| `img/sketches-strip.webp` | 45:884 | Shipping, between the first paragraph and the day-by-day paragraph; the onboarding strip follows that paragraph |

## The onboarding row

Under the sketches: the first onboarding as one strip of its 11 screens that fits the text column, no
sideways scroll. Each is the live CodeCatalog desktop screen in its longest state, shown whole (3 things
with all three sections open, the calculator with the whole plan, plans through to risks accepted, the
sign-up form filled). The strip has five columns, 166px each. Screens are stacked in sequence, split so the tallest
column is as short as it can be: 3 things + email + sign-up upper | savings path + calculator + monthly payment |
plan selection | docs + sign-up form | standing order + confirmation. Frames stretch to fill their column.
Built by `source/flow33.py`.

No bars or step numbers under the screens (removed by request). A dot at the bottom right of each frame gives the
running total of steps up to and including that screen, in two digits: 06, 07, 08, 09, 16, 18, 23, 27, 31, 32, 33. The steps each screen covers, 01 to 33,
are kept in its `data-steps` attribute; the docs screen is four steps, one per doc.

Left out by request: the assumptions dialog and the "Hold on while we run some checks" screen.
The all-docs-accepted state is not in CodeCatalog and is not shown; to be revisited.
Montserrat and Roboto Mono are in `site/_vendor/` for these screens.

## Background

The light page background is white (#FFFFFF), not Color's #f2f5f7. Dark is unchanged.

## Frame sizes in the strip

No frame is shorter than 900px of screen (126px on the page, a 4:3 frame), and every screen keeps at least
170px of its own space under its last element, so short screens still read as screens and the dot sits clear.
