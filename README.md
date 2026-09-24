# FolioCatalog

Every version of a folio page, kept whole: shipped ones, replaced ones, and ones that never
left Claude. Each version is the complete page as code in this repo (HTML, CSS, fonts,
images), with no link out to where it came from. Open any `site/…/index.html` and it
works, offline, forever.

Live at **https://cesar-foliocatalog.vercel.app**: its own Vercel project, separate from the
folio and its staging, open to anyone with the link, no sign-in. Every push to `main`
redeploys it within a minute, and the URL stays the same if the repo goes private.

`index.html` is the viewer. One header line: **Project**, **Version**, **Compare** (1 to 6
pages side by side) and, when the screen is too narrow for all of them, **‹ ›** to step
through, and a light/dark switch that sets every page shown that has both themes (the
Figma page has one look). Panes are never narrower than 360px; the page never
scrolls sideways. Each page is drawn at the width it was designed for and scaled into its
pane. Compare shows the chosen version and the ones after it. In a pane, text selects and the
page scrolls, but nothing navigates: the viewer takes the address off every link and swallows
clicks on anything clickable. The stored pages themselves are untouched, so a version taken
out of `versions/` works in full. A view can be linked:
`index.html#cable/2026-09-21/3/0` (project / version / how many / first one shown).

    python3 -m http.server 4174 --directory ~/Claude/FolioCatalog      to run it locally

Serve it rather than opening the file: fonts do not load from `file://`.

## Before trusting it

    python3 tools/check.py

Exit 0 means every page stands on its own: nothing it loads comes from outside its own
version folder (no http, no CDN, no Google Fonts, no claude.ai, no Figma), every file it
loads exists, and every file is committed in git. Links a reader clicks (LinkedIn, the other
case studies) are the only things pointing out, and a page renders without them.
Tested against a deliberately broken clone: it caught a deleted image, an outside font, an
outside `srcset` image, an outside `@import` and a missing file. On 2026-09-24 every page was
also opened from a fresh `git clone` in Chrome: all images, fonts and stylesheets loaded, no
request left localhost.

## Cable

| id | what | shipped | left the folio |
|---|---|---|---|
| `2024-07-06` | Figma: the Figma "Cable _air" frame, built as one page | never | |
| `2026-07-08` | Lite: the August page | 6 Aug 2026 18:04 | 21 Sep 2026 21:23 |
| `2026-09-21` | Rebuild, the third column on the staging compare page | 21 Sep 2026 21:23 | 23 Sep 2026 23:12 |
| `2026-09-22-noir` | Noir, text only (Claude Design); dark mode added here | never, made 22 Sep 09:31 | |
| `2026-09-23-color` | Color, Noir with images (Claude Design) | never, made 23 Sep 17:30 | |
| `2026-09-23-shipped` | Shipped: the Crazy canvas (made 23 Sep 22:19) built into the site | 23 Sep 2026 23:12 | live |

## Penfold

| id | what | shipped | left the folio |
|---|---|---|---|
| `2020` | Sqsp: the 2020 live page on the Squarespace site, rebuilt from screenshots (notes in `source/NOTES.md`) | 2020, date not on record | |
| `2024-07-15` | Figma: the Figma "penfold _air" frame, built as one page | never | |
| `2026-07-30` | Lite: the live page, as of 24 Sep 2026 | 30 Jul 2026 14:54 | live |

## Confirmo, Mara, Starcount

| project | id | what | shipped | left the folio |
|---|---|---|---|---|
| confirmo | `2026-07-29` | Lite: the live page, as of 24 Sep 2026 | 29 Jul 2026 01:51 | live |
| mara | `2020-07-20` | Figma: the Figma "MARA _air" frame, built as one page | never | |
| mara | `2020-07-23` | Sqsp: the 2020 live page on the Squarespace site, rebuilt from screenshots (notes in `source/NOTES.md`) | 2020, date not on record | |
| mara | `2026-07-29` | Lite: the live page, as of 24 Sep 2026 | 29 Jul 2026 01:51 | live |
| starcount | `2020-07-01` | Observatory: the 2020 Observatory case study on the Squarespace site, rebuilt from screenshots (notes in `source/NOTES.md`) | 2020, date not on record | |
| starcount | `2020-07-02` | Audiences: the 2020 Audiences case study on the Squarespace site, rebuilt from screenshots (notes in `source/NOTES.md`) | 2020, date not on record | |
| starcount | `2026-07-29` | Lite: the live page, as of 24 Sep 2026 | 29 Jul 2026 01:51 | live |

## DONE

| id | what | shipped | left the folio |
|---|---|---|---|
| `2020-07-20` | Sqsp: the 2020 live page on the Squarespace site, rebuilt from screenshots (notes in `source/NOTES.md`) | 2020, date not on record | |
| `2024-06-28` | Figma: the Figma frame "06 Done _folio", built as one page | never | |
| `2024-07-23` | Done2: the Figma frame "06 Done2 _air", built as one page | never | |
| `2026-08-03` | Lite: the page as it was when taken off | 3 Aug 2026 18:49 | 21 Sep 2026 14:47 |

Times are UK time. Shipped times are the git push to `main` (Vercel deploys within
seconds) where it is on record; the August Cable page's is the oldest production deploy
Vercel still lists; the other Lite pages' are the commit that first put them live. Made times
are the canvas's creation time on claude.ai.

The Crazy canvas itself, desktop and mobile, is kept in git history rather than the list, since
Shipped is the same page: `git show a4abbf9:versions/cable/2026-09-23-crazy/meta.json`, or
`git worktree add ../crazy a4abbf9` for the whole folder.

## Adding a version

From Portfolio's git history (store a page **before** its replacement is committed, or
name the ref it was live at):

    python3 tools/from_portfolio.py cable --ref 78b4426 --id 2026-09-23-shipped --name Shipped \
        --shipped 2026-09-23T23:12:11+01:00 [--until …] [--note …]

From a single self-contained HTML file:

    python3 tools/from_file.py cable path/to/page.html --id 2024-07-06 --width 1920

From a Claude Design canvas: download its `project/*.dc.html`, `canvas.json` and every
`/_blob/` image first (the Artifact tool's read action), then:

    python3 tools/from_design.py cable --id … --name … --canvas <artifact url> --made … \
        --boards Main.dc.html Main-2.dc.html --blobs <image folder> --vals '{"theme":"dark"}'

`--vals` fills the `{{holes}}` renderVals computes from the artboard's settings; plain
string values are read from the script.

Then `python3 tools/build.py` to put it in the viewer.

## What a stored version is

    versions/<project>/<id>/
      meta.json    name, width, shipped / until / made times, where it came from, note
      site/        the whole page. Portfolio versions keep the folio's layout
                   (site/cable/index.html beside site/case-shared.css)
      source/      Claude Design only: the artboard files and canvas.json, unchanged

Changed on the way in, and nothing else:
- root-absolute paths (`/cable/fonts/x`) are made relative
- links to other pages (home, other case studies, CV) point at the live folio
- Google Fonts and any other external file a page loads are downloaded into `site/_vendor/`
- the PostHog script is removed, and every page is `noindex`
- Claude Design artboards are flattened to plain HTML with their settings applied

Two edits, by request, both 2026-09-24: Noir got a dark mode (its light look is unchanged),
and the Figma page's Cable dates were corrected to Jul 2020 - Oct 2022, as in the CV.

`catalog.json` and `index.html` are built by `tools/build.py` from the meta files. Never
hand-edit them.

## Layout

    code     tools/
    derived  versions/                     copies, never edited after they are stored
    out      catalog.json, index.html      built
