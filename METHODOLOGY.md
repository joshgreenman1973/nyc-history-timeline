# New York, in Time — methodology & sources

An interactive, scroll-driven timeline of key moments in the history of New York City, from the Lenape homeland of Lenapehoking (c. 900 CE) through the start of Manhattan congestion pricing in 2025.

## What this is
A **curated** selection of 62 turning points — not a comprehensive chronicle. Events were chosen to span the full arc of the city across six eras:

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
