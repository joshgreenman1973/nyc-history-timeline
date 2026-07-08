# New York, in Time — methodology & sources

An interactive, scroll-driven timeline of key moments in the history of New York City, from the Lenape homeland of Lenapehoking (c. 900 CE) through the start of Manhattan congestion pricing in 2025.

## What this is
A **curated** selection of 396 turning points — not a comprehensive chronicle. Events were chosen to span the full arc of the city across six eras:

1. Lenapehoking & New Amsterdam (pre-1664)
2. Colonial & Revolutionary (1664–1783)
3. Empire City Rising (1784–1897)
4. Greater New York (1898–1945)
5. Modern Metropolis (1946–2000)
6. 21st Century (2001–present)

Events are tagged across eight themes: Founding & Colonial, Politics & Government, Infrastructure & Building, Immigration & People, Disaster & Crisis, Culture & Landmarks, Civil Rights & Protest, and Economy & Money.

## Sourcing
Every event carries a direct link to a reputable source, surfaced through web research and spot-checked. Priority was given to authoritative references:

- Government / archival: National Park Service, Library of Congress, U.S. House History, NYC Dept. of Records & Information Services, NYC Landmarks Preservation Commission, NYC Parks, Federal Reserve History, U.S. Dept. of Energy, National Weather Service
- Institutions / museums: Museum of the City of New York, New-York Historical Society, Central Park Conservancy, New York Transit Museum, Statue of Liberty–Ellis Island Foundation, Smithsonian NMAAHC, Cornell University ILR School, American Society of Civil Engineers, Historical Society of the New York Courts
- Encyclopedic: Britannica; Wikipedia (used where a well-established fact lacked a cleaner primary link — flagged for the reader via the visible source name)

The full source list, by year, is available in the in-page **"Sources & method"** panel.

## Fact-check passes (four independent rounds)
After assembly, every event in all six eras was audited by an independent fact-checking pass that re-verified dates, names, numbers and characterizations against reputable sources — then a **second, fully independent round** re-audited the whole corrected dataset from scratch.

**Round 1** corrections: the 1907 Ellis Island figure (~1 million processed at the station, not the ~1.28 million total US arrivals that year), the Queens–Midtown Tunnel builder (New York City Tunnel Authority, not Robert Moses's agency), the Cross Bronx Expressway completion year (1963), the 1741 conspiracy-trial arrest count and Fort George fire date (March 18), the Bank of New York's rank among early US banks, and the 2025 Mamdani turnout comparison (highest since 1969).

**Round 2** corrections: the 1798 yellow-fever toll as a share of population (~6%, not 4%), the 1892 cholera-scare quarantine (ordered under President Harrison, not Cleveland, who was not yet inaugurated), Congregation Shearith Israel's founding year (1654), the 2003 blackout figure (~50 million, per the cited DOE source), the 2004 RNC arrest count (more than 1,800, a convention record), the Occupy Wall Street opening-march size (~1,000), and the Federal Hall remodeling date (1788–89, distinct from the 1785 capital designation).

Across both rounds, four high-severity and several low-severity fixes were made; eras I, IV and V passed the second round with zero errors, and the vast majority of all claims verified clean.

A later thematic expansion added ~44 events (arts, music, theater, film, sports, immigration/neighborhoods, science and technology). Each was verified with reputable sources by its researcher at the time of addition.

**Round 3** re-checked events against **primary/original sources** (see below) — verifying claims against the actual documents rather than encyclopedias. It surfaced **zero factual corrections**, independently confirming the dataset's accuracy.

**Round 4** was a fresh five-agent adversarial audit of all 331 events, with extra scrutiny on the thematic additions. Eras I–IV passed with zero errors; the only fix on the live site was one date (the New Amsterdam Theatre's Disney reopening, corrected to the November 1997 Lion King premiere).

## Layers of depth
Beyond the core facts, many cards carry additional layers, each independently verified:

- **Primary source** (41 events): a link to the actual original document, fetched and confirmed to support the claim — e.g. Robert Juet's 1609 journal of the Half Moon voyage, the Dutch West India Company charter at Yale's Avalon Project, the Schaghen letter at the NY State Library, Governor Hunter's own 1712 report on the slave revolt, the printed 1701 Captain Kidd trial record, the original 1916 Zoning Resolution, and the eyewitness United Press dispatch on the Triangle fire.
- **Historian's lens** (66 events): a named scholar, their work, and a faithful summary of the argument they made about that moment — e.g. Russell Shorto, Jill Lepore, Leslie Harris, Tyler Anbinder, Rosenzweig & Blackmar, Iver Bernstein, David McCullough, David von Drehle, Mae Ngai, Robert Caro, Kim Phillips-Fein, Jeff Chang, Franklin Zimring and Martin Duberman. Every attribution passed two independent verification passes.
- **Further reading** (37 events): an acclaimed narrative history to read next (Pulitzer/Bancroft winners and standard works), deduplicated so a card never lists the same book as both its lens and its reading pick.
- **In fiction** (16 events): notable films, TV, novels, musicals and plays set in the event or period — Gangs of New York, Hamilton, The Age of Innocence, Ragtime, The Great Gatsby, West Side Story, Summer of Sam, Angels in America, Rent, The Deuce, Motherless Brooklyn and more.

The reading and fiction attributions were also independently fact-checked (real works, correct authors/creators/years, correct topic).

## Significance sizing
Events are rendered at three visual weights so the eye can find the pivotal moments at a glance: **major** turning points (founding events, the 1898 consolidation, the Erie Canal, the Brooklyn Bridge, 9/11, and the like) appear largest and boldest; **notable** events at the default size; **lesser** events in a compact, quieter card. The tier of each event is assigned in `parts/merge.py` and is editorial, not a claim about historical importance in any absolute sense.

## Images
Significant cards carry a **genuine period image** — a painting, engraving, map or photograph made in or near the event's own era. Images were first fetched from each subject's Wikipedia article (`parts/fetch_images.py`), then **picture-edited by a curation pass** (`parts/resolve_curated.py` applying `parts/curate_*.json`) that reviewed every pre-1945 image against the Wikimedia Commons API and replaced anachronistic modern photos with verified period art — the 1664 Duke's Plan for the English takeover, a Currier & Ives lithograph for the Brooklyn Bridge, Edward Moran's 1886 painting for the Statue of Liberty dedication, Library of Congress / NARA photographs for the early 20th century, and so on. Where no period image exists on Commons, the card deliberately shows **none** rather than a wrong one. Images are de-duplicated so no picture appears on two cards, rendered as halftone, credited in the corner, and hosted by Wikimedia Commons under their own licenses. ~291 of 396 events carry an image; they render only on major and notable tiers.

## Confidence & caveats
- Each event is marked **high** or **medium** confidence. Medium-confidence items are shown with an **"≈ approximate"** badge and a `c.` date. These include the deep-pre-colonial Lenape settlement (a span, not a single date), the 1626 Manhattan "purchase" (no surviving deed; the 60-guilder figure is traditional), and the 1990 murder peak (dependent on definition/source).
- Where a date is traditionally given but debated by historians, the traditional date is used and noted.
- A few composite entries pair two closely-linked events of the same year (e.g. 1939 World's Fair + LaGuardia; 1965 Landmarks Law + federal immigration reform).
- Descriptions aim to state facts without editorializing. Many worthy moments were omitted to keep the story legible.

## How it's built
- Pure static site: `index.html` (structure + styles), `app.js` (engine), `data.js` (the verified dataset). No build step, no external data calls.
- Fonts: Fraunces (display) + Archivo (body/narrow) via Google Fonts.
- Interactions: scroll-driven spine fill + traveling "comet," IntersectionObserver reveals, era-tinted background that shifts as you pass each era, era jump-pills, theme filters, keyword search, a guided auto-scroll "tour," and a sources modal. Fully responsive (alternating two-column on desktop, single spine on mobile).

## Data schema (`data.js`)
Each event: `year`, `date`, `sortKey`, `title`, `blurb`, `category`, `era`, `source`, `sourceUrl`, `confidence` (`high`/`medium`), `icon`.
