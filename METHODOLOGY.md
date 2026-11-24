# New York, in Time — methodology and sources

An interactive, scroll-driven timeline of New York City history, from the Lenape homeland of Lenapehoking (c. 1000) through Zohran Mamdani's election as mayor in November 2025.

## What this is
A curated selection of 394 events, chosen to span the city's history across six eras:

1. Lenapehoking & New Amsterdam (pre-1664)
2. Colonial & Revolutionary (1664–1783)
3. Empire City Rising (1784–1897)
4. Greater New York (1898–1945)
5. Modern Metropolis (1946–2000)
6. 21st Century (2001–present)

Events are tagged with eight themes: Founding & Colonial, Politics & Government, Infrastructure & Building, Immigration & People, Disaster & Crisis, Culture & Landmarks, Civil Rights & Protest and Economy & Money.

## Sourcing
Every card carries one or two source links at the bottom. Since November 2026, key dates, figures and contested claims in the card text also link directly to the page that supports them: more than 500 inline links, on all but a handful of cards.

Sources were chosen in roughly this order:

- Government and archival: National Park Service, Library of Congress, the U.S. House and Senate historians, the New York City Department of Records and Information Services, the Landmarks Preservation Commission, New York City Parks, Federal Reserve History, the U.S. Department of Energy, the National Weather Service
- Institutions and museums: Museum of the City of New York, New-York Historical Society, Central Park Conservancy, New York Transit Museum, Statue of Liberty–Ellis Island Foundation, Smithsonian National Museum of African American History and Culture, Cornell University's School of Industrial and Labor Relations, American Society of Civil Engineers, Historical Society of the New York Courts
- Encyclopedic: Britannica; Wikipedia where a well-established fact lacked a better link, with the source named on the card

The full source list, by year, is in the page's "Sources & method" panel.

## Fact-checking
The dataset has had five review passes. The last two are written up in full in [FACT-CHECK.md](FACT-CHECK.md).

Round 1, at assembly, re-verified every date, name, number and characterization. It corrected the 1907 Ellis Island figure (about 1 million processed at the station, against about 1.28 million total US arrivals that year), the builder of the Queens–Midtown Tunnel (the New York City Tunnel Authority, not Robert Moses's agency), the Cross Bronx Expressway's completion year (1963), the 1741 conspiracy-trial arrest count, the Fort George fire date (March 18), the Bank of New York's rank among early US banks and the 2025 turnout comparison.

Round 2 re-audited the corrected dataset from scratch. It corrected the 1892 cholera quarantine (ordered under President Harrison; Cleveland was not yet inaugurated), Congregation Shearith Israel's founding year (1654), the 2003 blackout's reach (about 50 million people, per the Department of Energy), the 2004 Republican National Convention arrest count (more than 1,800), the size of the first Occupy Wall Street march (about 1,000) and the dates of Federal Hall's remodeling (1788–89). It also set the 1798 yellow fever toll at about 6 percent of the population; the September 2026 pass later withdrew that percentage because the denominator was uncertain.

Round 3 checked claims against primary documents where they exist and found no errors.

Round 4 re-audited the then-331 events. Its one fix was the date of the New Amsterdam Theatre's reopening, corrected to the November 1997 premiere of "The Lion King."

The September 2026 pass re-read every card, tested all 835 source links and corrected 11 errors, two duplicate events and a sorting bug.

The November 2026 pass checked every card against outside sources again, corrected 81 errors on 76 cards, replaced hijacked and dead links, rewrote copy that read as machine-written and added the inline links. Six of its corrections were claims that events had overtaken, such as the end of MetroCard sales and the start of Second Avenue Subway Phase 2 construction. Questions it could not settle are listed in [fact-check-flags-2026-11.md](fact-check-flags-2026-11.md).

## Layers
Many cards carry more under "Read more":

- Primary source (41 events): the original document, checked to confirm it supports the claim. Examples include Robert Juet's 1609 journal of the Half Moon voyage, the Dutch West India Company charter at Yale's Avalon Project, the Schaghen letter at the New York State Library, Gov. Robert Hunter's 1712 report on the slave revolt, the printed 1701 Captain Kidd trial record, the 1916 Zoning Resolution and the United Press dispatch on the Triangle fire.
- Historian's lens (66 events): a named scholar, the work and a summary of the scholar's argument about that moment. Scholars include Russell Shorto, Jill Lepore, Leslie Harris, Tyler Anbinder, Roy Rosenzweig and Elizabeth Blackmar, Iver Bernstein, David McCullough, David von Drehle, Mae Ngai, Robert Caro, Kim Phillips-Fein, Jeff Chang, Franklin Zimring and Martin Duberman.
- Further reading (37 events): a narrative history to read next, never the same book as the card's historian's lens.
- In fiction (16 events): films, TV, novels, musicals and plays set in the event or period, including Gangs of New York, Hamilton, The Age of Innocence, Ragtime, The Great Gatsby, West Side Story, Summer of Sam, Angels in America, Rent, The Deuce and Motherless Brooklyn.

Authors, creators and years in the reading and fiction layers were checked in the review passes.

## Card sizes
Cards come in three sizes. The largest go to major events (the founding, the 1898 consolidation, the Erie Canal, the Brooklyn Bridge, 9/11); most cards are medium; minor events get a compact card. The size is an editorial judgment, set in `parts/merge.py`.

## Images
Cards in the two larger sizes carry a period image: a painting, engraving, map or photograph made in or near the event's own era. Images were first fetched from each subject's Wikipedia article (`parts/fetch_images.py`). A curation pass (`parts/resolve_curated.py`, applying `parts/curate_*.json`) then checked every pre-1945 image against Wikimedia Commons and replaced modern photos with period art: the 1664 Duke's Plan for the English takeover, a Currier & Ives lithograph for the Brooklyn Bridge, Edward Moran's 1886 painting for the Statue of Liberty dedication, and Library of Congress and National Archives photographs for the early 20th century. Where Commons has no period image, the card has none. No image appears on two cards. Images are rendered as halftone, credited in the corner and hosted by Wikimedia Commons under their own licenses. About 291 of the 394 events carry one.

## Confidence and caveats
- Each event is marked high or medium confidence. Medium-confidence events show an "≈ approximate" badge and a "c." date. They include Lenape settlement (a span, not a date), the 1626 "purchase" of Manhattan (no deed survives; the 60-guilder figure is traditional) and the 1990 murder peak (counts vary by definition and source).
- Where historians debate a traditional date, the card uses the traditional date and says so.
- A few cards pair two linked events from the same year, such as the 1939 World's Fair and LaGuardia Airport.
- Descriptions state facts without editorializing. Many events were left out to keep the timeline readable.

## How it's built
- Static site: `index.html` (structure and styles), `app.js` (rendering and interaction) and `data.js` (the dataset). No external data calls.
- `data.js` is the source of truth. The `parts/` build files are out of date: the September and November 2026 fact-checks edited `data.js` directly, so running `parts/merge.py` would undo their corrections.
- Fonts: Bodoni Moda, Source Serif 4 and Archivo Narrow, from Google Fonts.
- Interaction: a scroll-driven spine, era-tinted backgrounds, era jump buttons, theme filters, keyword search, "On this day," a guided auto-scroll tour and a sources panel. The layout alternates two columns on desktop and collapses to one on mobile.

## Data schema (`data.js`)
Each event has `date`, `sortKey` (YYYYMMDD, zeros for unknown month or day), `title`, `blurb`, `detail`, `category`, `era`, `sources` (a list of name and URL), `confidence`, `icon` and `weight`, and optionally `image`, `imageCredit`, `historian`, `primary`, `reading` and `fiction`. Text fields may contain inline links written as `[words](https://url)`; `app.js` renders them as links.
