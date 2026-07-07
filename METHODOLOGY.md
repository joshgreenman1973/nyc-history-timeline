# New York, in Time — methodology & sources

An interactive, scroll-driven timeline of key moments in the history of New York City, from the Lenape homeland of Lenapehoking (c. 900 CE) through the start of Manhattan congestion pricing in 2025.

## What this is
A **curated** selection of 331 turning points — not a comprehensive chronicle. Events were chosen to span the full arc of the city across six eras:

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

## Fact-check passes (two independent rounds)
After assembly, every event in all six eras was audited by an independent fact-checking pass that re-verified dates, names, numbers and characterizations against reputable sources — then a **second, fully independent round** re-audited the whole corrected dataset from scratch.

**Round 1** corrections: the 1907 Ellis Island figure (~1 million processed at the station, not the ~1.28 million total US arrivals that year), the Queens–Midtown Tunnel builder (New York City Tunnel Authority, not Robert Moses's agency), the Cross Bronx Expressway completion year (1963), the 1741 conspiracy-trial arrest count and Fort George fire date (March 18), the Bank of New York's rank among early US banks, and the 2025 Mamdani turnout comparison (highest since 1969).

**Round 2** corrections: the 1798 yellow-fever toll as a share of population (~6%, not 4%), the 1892 cholera-scare quarantine (ordered under President Harrison, not Cleveland, who was not yet inaugurated), Congregation Shearith Israel's founding year (1654), the 2003 blackout figure (~50 million, per the cited DOE source), the 2004 RNC arrest count (more than 1,800, a convention record), the Occupy Wall Street opening-march size (~1,000), and the Federal Hall remodeling date (1788–89, distinct from the 1785 capital designation).

Across both rounds, four high-severity and several low-severity fixes were made; eras I, IV and V passed the second round with zero errors, and the vast majority of all claims verified clean.

A later thematic expansion added ~44 events (arts, music, theater, film, sports, immigration/neighborhoods, science and technology). Each was verified with reputable sources by its researcher at the time of addition; these newer entries have not yet been through the two adversarial rounds above.

## Significance sizing
Events are rendered at three visual weights so the eye can find the pivotal moments at a glance: **major** turning points (founding events, the 1898 consolidation, the Erie Canal, the Brooklyn Bridge, 9/11, and the like) appear largest and boldest; **notable** events at the default size; **lesser** events in a compact, quieter card. The tier of each event is assigned in `parts/merge.py` and is editorial, not a claim about historical importance in any absolute sense.

## Images
Most significant cards carry a representative image fetched from each subject's Wikipedia article via the Wikimedia pageimages API (`parts/fetch_images.py`, cached in `parts/images.json`). For historical events this is often a period engraving, painting or photograph; for still-standing landmarks it is a contemporary photo. Images are hotlinked from and hosted by Wikimedia Commons under their own licenses, credited in the corner of each card. Minor-tier events are intentionally imageless to keep them compact. About 297 of 331 events resolved an image; images render only on major and notable tiers.

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
