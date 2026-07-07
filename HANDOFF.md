# New York, in Time — handoff

An interactive, scroll-driven timeline of New York City history. This document is the single starting point for anyone (human or agent) picking the project up.

## Live
- **Site:** https://joshgreenman1973.github.io/nyc-history-timeline/
- **Repo:** `joshgreenman1973/nyc-history-timeline` (public), branch `main`, GitHub Pages from `/` root
- **Local dir:** `/Users/joshgreenman/Experiments/nyc-history-timeline`
- **Local preview:** launch config `nyc-history-timeline` on port 8555 (`python3 -m http.server 8555`)

## What it is
A curated selection of **331 turning points** in the city's history, from the Lenape homeland of Lenapehoking (c. 1000) to Mamdani's election (Nov 2025), across 6 eras and 8 themes. It is deliberately not comprehensive — it favors legibility over completeness.

Each event card has: a big serif year, an emoji, title, one-to-two-sentence blurb, a "Read more" expansion with a deeper paragraph, one-to-two source links, a period image (on major/notable cards), and — for ~66 events — a **"Historian's lens"** summarizing a named scholar's argument about that moment.

## Files
- `index.html` — structure, all CSS, the sources/method modal
- `app.js` — the whole engine (render, scroll choreography, filters, tools, modal)
- `data.js` — the built dataset: `window.NYC_EVENTS = [ … ]` (do not hand-edit; it is generated)
- `parts/` — the sources of truth and the build pipeline:
  - `era1.json … era6.json` — core events by era (the canonical, fact-checked set)
  - `era7_arts.json`, `era7_sports.json`, `era7_sci.json` — thematic additions
  - `hist_1.json … hist_4.json` — historian's-lens notes, keyed by exact event title
  - `primary_1.json … primary_6.json` — verified primary/original sources (and any corrections found), keyed by title
  - `reading_1.json … reading_3.json` — "further reading" acclaimed-history recommendations, keyed by title
  - `fiction_1.json` — "in fiction" ties (film/TV/novel/musical/play), keyed by title
  - `images.json` — cached Wikimedia image per event (from `fetch_images.py`)
  - `merge.py` — **the build**: globs `era*.json`, decodes HTML entities, drops `SKIP_TITLES` dups, dedupes by normalized title, sanitizes implausible sortKeys, assigns significance `weight`, attaches images + historian + primary + reading + fiction (reading is deduped against the historian book), sorts by (era order, sortKey), writes `data.js`. Loaders are keyed by lowercased-alphanumeric title, so a new note attaches by matching the event title exactly.
  - `fetch_images.py` — fetches a Wikimedia pageimages lead per event into `images.json` (incremental, cached; ~0.12s/call, needs network)
- `METHODOLOGY.md` — public-facing methodology (sourcing, fact-check rounds, images, significance, caveats)

## Build / rebuild
```
cd nyc-history-timeline
python3 parts/fetch_images.py    # only when events changed; incremental, caches misses
python3 parts/merge.py           # rebuilds data.js from all parts
```
Then commit and push (see Deploy). `merge.py` prints per-era counts and warnings (bad era/category/missing source). Zero warnings expected.

## Deploy
```
gh auth switch --hostname github.com --user joshgreenman1973   # IMPORTANT: active account flips to vitalcity-nyc on its own; always re-assert
git add -A && git commit -m "…"
git push origin main
```
Pages redeploys in ~1–3 min. Confirm with `curl -s https://joshgreenman1973.github.io/nyc-history-timeline/data.js | grep -c '"sortKey"'`.

## Data model (one event)
```json
{
  "date": "May 24, 1883",           // display date; "YYYY" or "c. YYYY" allowed
  "sortKey": 1883,                   // integer year for ordering (bump within a year to sequence)
  "title": "…",                      // <=64 chars, sentence case; the JOIN KEY for images/historian/etc.
  "blurb": "…",                       // 1–2 sentence summary (no serial comma)
  "detail": "…",                      // deeper paragraph, shown on Read more
  "category": "Infrastructure & Building",   // one of 8 (real ampersand)
  "era": "Empire City Rising (1784–1897)",   // one of 6 (real ampersand + en-dash)
  "sources": [{"name":"…","url":"…"}],       // 1–2 reputable sources
  "confidence": "high" | "medium",
  "icon": "🌉",
  "weight": 1|2|3,                    // significance (set by merge.py): 1 major, 3 minor
  "image": "https://upload.wikimedia.org/…",  // attached by merge from images.json
  "imageCredit": "…",
  "historian": {"who":"…","work":"…","take":"…","url":"…"},  // ~66 events
  "primary": {"name":"…","url":"…"},                          // ~41 events: verified original document
  "reading": [{"book":"…","author":"…","year":2004,"note":"…","url":"…"}],  // ~37 events
  "fiction": [{"work":"…","kind":"Film","year":2002,"by":"…","note":"…","url":"…"}]  // ~16 events
}
```
Everything after `confidence` is attached by the build, not authored in the era files. Titles must match exactly across `era*.json`, `hist_*.json`, and `images.json` (matching is by lowercased alphanumerics).

## Features (in app.js)
- Scroll-driven glowing spine + traveling "comet"; era-tinted background that shifts per era; IntersectionObserver reveals
- Significance tiers: weight 1 large/bold with a bigger node + larger image; weight 3 compact and imageless
- Sticky controls: era jump-pills, theme chips, keyword search with live "X of 331" count
- Search tools: **On this day** (month/day), **Jump to year**, **🎲 Surprise me** (random spotlight + expand)
- Guided **▶ tour** (auto-scroll), **Read more** card expansion, **Sources & method** modal listing every source

## Provenance & fact-checking
- Core 287 events researched by 6 per-era agents, then **two independent adversarial fact-check rounds** (4 high-severity + several low-severity fixes applied; eras I/IV/V passed round 2 clean).
- +44 thematic events added later (arts, sports, immigration, sci/tech), individually sourced.
- ~66 historian's-lens notes (Shorto, Lepore, Harris, Anbinder, Rosenzweig & Blackmar, Bernstein, Ackerman, McCullough, von Drehle, Ngai, Caro, Wallace, Phillips-Fein, Chang, Zimring, Freeman, Duberman, and more), each independently verified for correct attribution.
- Images: Wikimedia pageimages lead per subject (297/331), sepia archival treatment, credited; only on major/notable tiers.

## Known limitations / next steps
- A handful of auto-fetched images are approximate (e.g. explorer Verrazzano resolves to the bridge). A curated image pass would tighten these.
- 34 events have no Wikimedia image (render text-only).
- The ~44 thematic additions and the historian notes were verified at authoring time; they have had fewer adversarial rounds than the core 287.
- Primary/original-source linking is in progress: replacing/augmenting tertiary sources (Wikipedia/Britannica) with verified primary documents (digitized newspapers, statutes, charters, government records) where they exist.
- No analytics, no build step beyond the two Python scripts, no external runtime dependencies (fonts via Google Fonts, images hotlinked from Wikimedia).

## Gotchas
- **GitHub account flips to vitalcity-nyc** between pushes — always `gh auth switch` to joshgreenman1973 first.
- **app.js sorts by (eraIndex, sortKey)**, not sortKey alone — bumped same-year sortKeys would otherwise interleave eras.
- **The screenshot preview tool cannot composite the ~95k-px page** — verify via `elementFromPoint`, computed styles, or by temporarily collapsing the DOM (`display:none` on other events) before capturing.
- Research subagents tend to spawn their own sub-agents and return prose; instruct "do NOT spawn sub-agents; output ONLY JSON" and have them Write results to files to keep the main context lean.
