# Fact-check, September 2026

An independent pass over all 396 cards then in `data.js` — every date, title, blurb and detail paragraph, plus a machine check of all 835 source links. This is the fourth review the dataset has had; the earlier three are described in `HANDOFF.md`. It found eleven substantive errors, two duplicate events, one structural ordering bug and forty dead links. All of those are fixed below except the dead links, which are fixed for nine cards and catalogued for the rest.

The dataset is now 394 events.

## Errors corrected

**The Frick Collection (Dec. 16, 1935).** Said the museum opened "six years after his widow's death." Adelaide Howard Childs Frick died in October 1931 — four years. Corrected.

**Ford Foundation headquarters.** Dated Dec. 1, 1968. The building opened in 1967 and was inaugurated Dec. 7 that year — the card's own cited source, fordfoundation.org, says 1967. Redated to December 1967.

**RCA Building, Rockefeller Center.** Dated Nov. 1, 1933. The first tenant moved in April 22, 1933; the formal opening was set for May 1 and slipped to mid-May amid the fight over Diego Rivera's lobby mural. Redated to May 1933, with the delay explained in the detail.

**The 1938 city charter.** Blurb said "voters approved" it in 1938. They approved it Nov. 3, 1936; the first Council under it was elected in 1937 and the charter took effect in 1938. Rewritten.

**Bank for Savings (1819).** The card was dated March 16, 1819 and headlined "the city's first savings bank opens," while its own detail said the bank was incorporated in March and opened in July. It opened July 3, 1819. Redated.

**New York City's first COVID-19 case.** Said Feb. 29, 2020. The case was confirmed and announced March 1, 2020, which is what the card's cited Wikipedia source says. Corrected.

**Singer Building demolition.** Claimed it "became the tallest building ever peacefully demolished" in 1968 — true until 270 Park Avenue, at 707 feet, came down in 2021. Updated to name the record's end.

**1798 yellow fever.** Said the epidemic killed "about 2,080 people, roughly six percent of the population." The six percent comes from the cited Museum of American Finance page, which puts the city's population that summer at about 35,000 — a figure that counts only those who had not fled. The 1800 federal census counted 60,515 residents, which would put the toll near three percent. The blurb no longer asserts a percentage, and the detail now shows both denominators.

**Vitascope at Koster & Bial's (April 23, 1896).** Called it "the first commercial projection of motion pictures for a paying American audience." The Latham brothers' Eidoloscope did that on lower Broadway on May 20, 1895, nearly a year earlier. Reframed as the screening that brought projected film into a major vaudeville house and turned it into mass entertainment, with the Eidoloscope noted in the detail.

**Flight 1549 (Jan. 15, 2009).** Detail said the ditching came "less than four minutes after takeoff." Takeoff was 3:25:51 p.m., the ditching 3:30:43 — about five minutes. Corrected.

**Ali-Frazier (March 8, 1971).** Detail said the bout "marked Ali's return three-and-a-half years after his license was revoked." Ali had already returned, against Jerry Quarry, in October 1970. Rewritten.

## Duplicates removed

**The English seizure of New Amsterdam, Sept. 8, 1664,** appeared twice — once at the end of the Dutch era and once at the start of the colonial era, in different words. Because the two cards sat in different eras the build's dedup pass never saw them as a pair. Merged into one card, with both sets of sources kept.

**The Metropolitan Opera House opening, Oct. 22, 1883,** appeared twice, and the two cards disagreed about the house: one said it seated more than 3,600, the other more than 3,000. It seated about 3,625. Merged into one card at the correct figure.

## Ordering bug

Seventy-eight cards displayed out of chronological order. `sortKey` was a bare year, so a year-only event always sorted after every dated event in the same year, and a handful of keys had been bumped by a year to force an order. The Cross Bronx Expressway, whose year an earlier pass corrected from 1960 to 1963, still carried a 1960 key and so appeared before events from 1961 and 1962.

`sortKey` is now `YYYYMMDD`, derived from the display date, with month and day zeroed when the date does not give them. `parts/merge.py` derives it the same way on rebuild, so agent-supplied keys can no longer scramble the order. `app.js` reads years off the new key where it needs them. Inversions are now zero.

## Dead source links

All 835 source, further-reading, primary-document and historian links were requested. Forty returned 404 and four failed outright. Nine cards had no working source at all, which defeats the premise stated on the page — that every card carries a link you can check yourself. Those nine now have live, verified replacements:

- Trinity Church spire (1846) — Trinity Wall Street history
- First New Year's Eve ball (1907) — Times Square Alliance ball history
- First US zoning resolution (1916) — NYC Department of City Planning
- Black Tom explosion (1916) — FBI famous cases, Wikipedia
- Lincoln Tunnel first tube (1937) — Port Authority, Baruch NYCdata
- Normandie fire (1942) — Naval History and Heritage Command
- Wartime dimout (1942) — Gothamist
- V-J Day (1945) — National WWII Museum
- Hart-Celler Act (1965) — US House historian, LBJ Library

Thirty-one cards still carry one dead link alongside a working one. The heaviest cluster is the New Netherland Institute, which restructured its site and broke six links (Hudson, Block, the West India Company, the Schaghen letter, the Charter of Freedoms, Kieft). The rest are scattered: nps.gov Verrazzano and Plaza Hotel pages, the Collegiate School timeline, Bronx County Historical Society on Jonas Bronck, loc.gov's Haven to Home exhibit, nyphil.org history, AMNH archives, neh.gov on Riis and on Papp, un.org headquarters, Baseball Hall of Fame on the 1955 and 1996 World Series, PBS on Robert Moses, nyc.gov on the landmarks law, NYSED on Ocean Hill-Brownsville, panynj.gov on the World Trade Center, MCNY on Studio 54 and the 1977 blackout, ojp.gov on CompStat, history.com on One World Trade Center, and four publisher pages for books in the further-reading layer.

A further 204 links returned 403 and 12 returned 202. Those are bot blocks, not dead pages — Britannica, loc.gov, Mount Vernon, Gilder Lehrman and Oxford University Press all refuse scripted requests but load normally in a browser. Spot checks confirmed this. They were not touched.

## Checked and correct

Everything else held up. Worth recording, because these are the claims most likely to be wrong and they are not:

- The 1990s immigration card's "45 percent of adults foreign born by 2000" is verbatim from the cited New York Fed research, as is the 1.2 million figure.
- Fresh Kills: "roughly 1.4 million tons" over a ten-month operation matches the Sanitation Department's own account exactly.
- Recent additions are right, including the Studio Museum's purpose-built home opening in November 2025 and the Breuer building's 2025 landmark designation.
- The 1907 Ellis Island peak (about 1 million, 11,747 in a day), the 1990 murder record (2,245), the 1798-1849 epidemic tolls, the Draft Riots, the Triangle fire, the 1918 flu, Sandy's $19 billion, the 9/11 tolls, Mamdani's 56 percent primary and turnout claims all check out.
- Every era assignment is inside its era's date range.

## Claims left standing with a note

These are contestable rather than wrong, and are flagged here rather than changed:

- **The Nuyorican Poets Cafe, "Oct. 31, 1973."** The founding in Miguel Algarín's apartment is well documented; a precise day is not. The card's confidence label should probably be medium.
- **Collegiate School, c. 1628.** The card already says the year is contested among 1628, 1633 and 1638, and attributes the 1628 claim to the school. That is the honest way to handle it.
- **MTV "launches from New York," Aug. 1, 1981.** The company and its studios were in New York; the launch feed originated in Fort Lee, New Jersey.
- **The RCA Building's "70 stories."** Sources split between 66 and 70 depending on whether the setback floors are counted. The observation deck is billed as the 70th floor. Left as is.
- **Benny Goodman, "the first time a big band headlined the classical hall."** Carefully worded already; James Reese Europe and W.C. Handy had played Carnegie Hall earlier, but not as a swing band headlining.
- **The 1795 and 1803 yellow fever death tolls (about 730 and about 700).** Both figures are right, but the cited Baruch NYCdata page contains no death figures at all and dates the era's peaks to 1795, 1799 and 1803. The numbers need a source that actually carries them.

## Method

Every card's date, title and blurb was read in full, and every detail sentence containing a number was extracted and reviewed separately. Claims that could not be settled from the record were verified against primary or institutional sources — the Museum of American Finance, the Ford Foundation, Wikipedia's sourced articles, the New York Fed, DSNY, the National WWII Museum, the US House historian's office, CTBUH. Link health was checked by requesting all 835 URLs with a browser user agent and a 25-second timeout.
