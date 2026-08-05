# Review deployment: visible 3 August variant

Date: 2026-08-03

## Result

- Review URL: `https://new.haven.digipomps.org/`
- Active review release: `/var/www/haven-public-review-releases/20260803T162639Z`
- Review docroot symlink: `/var/www/haven-public-review`
- Search indexing: blocked by `X-Robots-Tag: noindex, nofollow, noarchive`
- HAVEN app entry: `blocked`; no app, demo or install URL is published
- Production docroot: unchanged at `/var/www/haven-public-new-releases/20260801T095935Z`

The visible review variant now contains the Fable-adjudicated hero, the approved
ingress and counterweight, a five-step human control loop, a labelled democracy
hypothesis, the maturity boundary, three abstraction-level entries and the
professional audiences after the human story.

## Checksums

Local source, deployed release and downloaded live HTTPS bytes match:

| Asset | SHA-256 |
|---|---|
| `index.html` | `036c2684f96a24135b24e71acacbbbcef8b7c1300e5798e1c74f598e88ee4414` |
| `assets/site.css` | `5237dfc330d2f8850affb71bb7bcb904759e67957b0b6fce2b46b6bdd61b136b` |
| `assets/site.js` | `3318c99817c51e8c29d4917b5d37a72939a4d25d7b3a679c9acf3f7bab8077a6` |

Production `index.html` before and after review deployment:

`6c41f47fec6020f9e6d4531842a160dfc3b848de6a9f574cb5bedb0a29b29784`

## Verification

- app-entry release guard: passed, fail-closed, exactly two hero actions
- Python unit tests: 8/8 passed
- live and local Chromium: passed with JavaScript enabled and disabled
- accessibility tree: both hero actions have the expected names
- keyboard: primary hero action receives visible focus
- text size: 200%, no horizontal overflow
- mobile viewport: 390 × 844, no horizontal overflow
- live assets: CSS, logo, hero and control-loop images loaded with non-zero
  intrinsic dimensions
- live content: approved H1, control-loop sequence and labelled democracy
  hypothesis found in downloaded HTTPS source
- HTTPS response: 200; CSP, HSTS, nosniff, frame denial and noindex present

Live full-page artifact:

- `haven-review-live-20260803.png` (1280 × 11167)

## Files changed for this visible variant

- `Website/index.html`
- `Website/assets/site.css`
- `Website/assets/haven-human-agency-20260803.png` (lossless local master; not deployed)
- `Website/assets/haven-human-agency-20260803.webp`
- `Website/assets/haven-control-loop-20260803.png` (lossless local master; not deployed)
- `Website/assets/haven-control-loop-20260803.webp`
- `Website/artikler/digital-uavhengighet/index.html`
- `Website/artikler/mennesket-forst/index.html`
- `Website/artikler/demokrati-trenger-mer/index.html`
- `Website/artikler/index.html`
- `Website/sitemap.xml`
- `Website/tools/verify_app_entry.py`
- `Website/tests/app_entry_browser_smoke.js`
- `Website/DEPLOYMENT_STATUS.md`
- this deployment report and the live screenshot above

## Image generation record

Style reference:

`Website/assets/haven-human-workshop.webp`

### Human-agency hero

Generated original:

`/Users/kjetil/.codex/generated_images/019f655e-eb0a-78d3-9763-122dae6cb533/exec-7952d924-1a00-4c1a-a7a2-4b92b9bb67aa.png`

Published derivative:

`Website/assets/haven-human-agency-20260803.webp`

Final prompt:

> Create a new horizontal editorial illustration for the HAVEN information website, using the referenced image only as a visual style reference. Purpose: first-screen hero for a Norwegian public-interest technology project about individual digital independence built together. Scene and action: four ordinary adults of varied age and appearance gather around a wooden table. One person is clearly the decision-maker. A paper request card arrives from a simple service at the edge of the scene; the request initially has several broad permission marks. The person calmly chooses and physically places a smaller, narrower permission card into an open path. Only one muted colored line continues from the person toward the service. A small receipt card visibly returns to the person. Two other people collaborate supportively without taking control away. Show human agency, deliberate choice, cooperation, action, and the ability to inspect the result. Visual language: warm Scandinavian editorial paper collage, subtle grain and handmade paper fibers, delicate ink drawing, off-white background, muted forest green, clay orange, ochre, charcoal, dusty blue. Include two open curved arc motifs inspired by HAVEN’s logo, never closed into a circle. Keep the composition calm, trustworthy, human and grounded, not futuristic. Preserve generous clear space around the figures and avoid visual clutter. Landscape 3:2. Do not include any text, letters, logos, watermarks, robots, humanoid AI, shields, padlocks, glowing screens, crypto symbols, corporate stock-photo styling, closed circles, or global score metaphors.

### Human control loop

Generated original:

`/Users/kjetil/.codex/generated_images/019f655e-eb0a-78d3-9763-122dae6cb533/exec-f31ddf0b-33bd-4a6d-9533-61eea06de865.png`

Published derivative:

`Website/assets/haven-control-loop-20260803.webp`

Final prompt:

> Create a second horizontal editorial illustration for the same HAVEN website, matching the referenced warm Scandinavian paper-collage style and recurring people. Purpose: accompany an HTML explanation of a five-step control loop. The image itself must contain no text. Composition: a clear left-to-right sequence of five connected but open mini-scenes on one continuous handmade-paper landscape: 1) an ordinary person receives a request card from a simple service; 2) the person examines a small purpose card, with a trusted helper nearby but not controlling the choice; 3) the person deliberately removes several broad permission tokens and keeps one narrower token; 4) a restrained tool/agent representation performs exactly one mundane action through a single colored path; 5) a receipt card returns to the same person, who can lift or disconnect the remaining permission token for future use. Make the same person visibly present and in control throughout, while community support, safe boundaries, and accountable institutions are suggested through other human figures and simple desk objects. Use open curved HAVEN arc motifs to frame but never enclose people. Show choice, collaboration, action, inspection, and withdrawal. Make each stage visually distinct enough that HTML labels can sit below it. Visual language: tactile off-white paper, subtle grain, ink drawing, muted forest green, clay orange, ochre, charcoal and dusty blue. Calm, public-interest, human, practical, non-futuristic. Landscape 3:2 with balanced spacing. Do not include any text, letters, numbers, logos, watermarks, robots, humanoid AI, shields, padlocks, glowing screens, crypto imagery, global person scores, closed circles, surveillance imagery, or corporate stock-photo styling.

## Remaining boundaries and non-blocking backlog

- No canonical public HAVEN app origin is documented. The app/install CTA remains
  correctly blocked; this did not block the information-site review release.
- The integrated identity journey is not ready for public pilot. The site says so.
- The review recommendation for a separate article comparing two ecosystem
  governance models is not required to understand this coherent variant and
  remains P1 editorial backlog.
- P2 work on converting the whole article index into explicit reading paths is
  not part of this release.
