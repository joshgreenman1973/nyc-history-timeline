#!/usr/bin/env python3
"""Merge era JSON part files into data.js. Decodes HTML entities, dedupes, sorts, validates."""
import json, glob, os, html, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ERAS = [
    "Lenapehoking & New Amsterdam (pre-1664)",
    "Colonial & Revolutionary (1664–1783)",
    "Empire City Rising (1784–1897)",
    "Greater New York (1898–1945)",
    "Modern Metropolis (1946–2000)",
    "21st Century (2001–present)",
]
ERA_ORDER = {e: i for i, e in enumerate(ERAS)}
CATS = {"Founding & Colonial","Politics & Government","Infrastructure & Building",
        "Immigration & People","Disaster & Crisis","Culture & Landmarks",
        "Civil Rights & Protest","Economy & Money"}

# Significance tiers — matched against lowercased titles.
# weight 1 = pivotal (largest), 3 = lesser (smallest), 2 = default.
MAJOR = [
    "lenape settle","lenape make","henry hudson","verrazzano","purchase","manhattan \"purchased",
    "new amsterdam granted","municipal government","english seize","becomes new york","flushing remonstrance",
    "first jewish","washington inaugurated","battle of long island","evacuation day","zenger",
    "commissioners' plan","lays out the grid","erie canal","croton aqueduct","great fire destroys",
    "central park","greensward","draft riots","brooklyn bridge","statue of liberty","ellis island opens",
    "tweed ring","consolidate","tenement house act","first subway","triangle shirtwaist","grand central",
    "woolworth","zoning","harlem renaissance","wall street crash","empire state building opens","chrysler building",
    "la guardia elected","la guardia became","world's fair opens","un chooses","jackie robinson",
    "landmarks preservation law","immigration reform","reopens the golden door","stonewall","world trade center",
    "hip-hop is born","drop dead","fiscal crisis","blackout that broke","dinkins is elected","crown heights",
    "9/11","september 11 attacks","attacks destroy","miracle on the hudson","high line","same-sex marriage",
    "occupy wall street","hurricane sandy","one world trade center opens","de blasio elected","covid-19",
    "george floyd","adams elected","congestion pricing tolls begin","mamdani elected","mamdani wins",
    "metropolitan opera house opens","new york philharmonic gives","chinese exclusion act",
    "great migration remakes harlem","saturday night live","cbgb opens","lincoln center opens",
    "first passenger elevator","first macy's thanksgiving",
]
MINOR = [
    "estêvão gomes","estevao gomes","adriaen block","new netherland company","dutch west india company is chartered",
    "charter of freedoms","van twiller","first school","jonas bronck","stadt herbergh","first ferry","nieuw haarlem",
    "peach war","castello plan","duke's laws","dutch retake","treaty of westminster","bolting act","charter of liberties",
    "dongan charter","montgomerie","trinity church receives","captain kidd","new-york gazette","mill street synagogue",
    "bowling green","new york society library","liberty pole","golden hill","new york tea party","kip's bay",
    "harlem heights","white plains","fort washington","prison ships","farewell at fraunces","bank of new york",
    "manumission society","african free school","buttonwood","manhattan company","new-york historical society",
    "fulton","savings bank","gas lamp","first railroad","panic of","barnum","astor place","crystal palace",
    "castle garden","cooper union","police riot","metropolitan police","paid fire","white wings","elevated rail",
    "rapid transit act","williamsburg bridge","longacre","general slocum","stanford white","singer building",
    "hudson-fulton","uprising of the 20,000","metropolitan life","new york public library's","armory show",
    "equitable building","black tom","birth control clinic","silent parade","malbone","wall street bombing",
    "cotton club","immigration act imposes","lindbergh","holland tunnel","museum of modern art","george washington bridge",
    "jimmy walker","rivera mural","triborough","lincoln tunnel","reform city charter","first regular us tv","laguardia airport",
    "queens-midtown","normandie","wartime dimout","levittown","idlewild","secretariat","puerto rican","containerization",
    "penn station","verrazzano-narrows","ocean hill","shirley chisholm","son of sam","studio 54","lennon",
    "goetz","tompkins square","central park jogger","yankees' dynasty","times square is reborn","diallo",
    "smoke-free","staten island ferry crash","freedom tower cornerstone","republican convention","transit strike",
    "trans fats","planyc","lehman","term limits","yankee stadium and citi","times square car bomb","9/11 memorial opens",
    "barclays","citi bike","stop-and-frisk","9/11 memorial museum","officers ambushed","pope francis","chelsea bombing",
    "second avenue subway","cornell tech","truck attack","amazon scraps","hudson yards","rent-law","hurricane ida",
    "migrant arrivals","adams indicted","containerization","cross bronx",
    "western union tower","city fetes the transatlantic","new york stock exchange opens its",
    "federal reserve bank of new york opens","air conditioning cools","silicon alley","fresh kills recovery",
    "omny brings","feast of san gennaro","tin pan alley","first tony awards","first new york film festival",
    "warhol's silver factory","def jam is founded","tenement museum founded","brighton beach","nuyorican poets cafe is born",
    "us open moves","current madison square garden","mets play their first",
]
def weight_for(title):
    t = title.lower()
    for k in MAJOR:
        if k in t: return 1
    for k in MINOR:
        if k in t: return 3
    return 2

# Redundant additions to drop (normalized titles) — near-dups of events already present.
SKIP_TITLES = {
    "zengeracquittedanearlypressfreedomvictory",   # dup of existing Zenger acquittal
    "immigrationactof1924emptiesellisisland",        # dup of "Immigration Act imposes national quotas"
    "nuyoricanpoetscafeopensinloisaida",             # dup of "Nuyorican Poets Cafe is born"
    "astorplaceriotoverrivalshakespeareans",         # dup of "The Astor Place Riot turns deadly"
}

def clean(s):
    if not isinstance(s, str): return s
    # decode HTML entities (&amp; etc.) to real characters
    return html.unescape(s)

def norm_title(t):
    return re.sub(r'[^a-z0-9]', '', clean(t).lower())

def main():
    events = []
    # optional image cache (from fetch_images.py), keyed by normalized title
    IMAGES = {}
    imgpath = os.path.join(HERE, "images.json")
    if os.path.exists(imgpath):
        try: IMAGES = json.load(open(imgpath))
        except Exception: IMAGES = {}
    # optional historian's-lens notes from hist_*.json (arrays of {title,who,work,take,url})
    HIST = {}
    for hf in sorted(glob.glob(os.path.join(HERE, "hist_*.json"))):
        try:
            for h in json.load(open(hf)):
                HIST[re.sub(r'[^a-z0-9]', '', h.get("title","").lower())] = {
                    k: h[k] for k in ("who","work","take","url") if k in h}
        except Exception: pass
    # optional verified primary/original sources from primary_*.json
    PRIMARY = {}
    for pf in sorted(glob.glob(os.path.join(HERE, "primary_*.json"))):
        try:
            for x in json.load(open(pf)):
                p = x.get("primary")
                if p and p.get("url"):
                    PRIMARY[re.sub(r'[^a-z0-9]', '', x.get("title","").lower())] = {
                        "name": p.get("name",""), "url": p["url"]}
        except Exception: pass
    # optional historical-fiction ties from fiction_*.json (grouped by event title)
    FICTION = {}
    for ff in sorted(glob.glob(os.path.join(HERE, "fiction_*.json"))):
        try:
            for x in json.load(open(ff)):
                k = re.sub(r'[^a-z0-9]', '', x.get("title","").lower())
                FICTION.setdefault(k, []).append({kk: x[kk] for kk in ("work","kind","year","by","note","url") if kk in x})
        except Exception: pass
    # optional "further reading" nonfiction from reading_*.json (grouped by event title)
    READING = {}
    for rf in sorted(glob.glob(os.path.join(HERE, "reading_*.json"))):
        try:
            for x in json.load(open(rf)):
                k = re.sub(r'[^a-z0-9]', '', x.get("title","").lower())
                READING.setdefault(k, []).append({kk: x[kk] for kk in ("book","author","year","note","url") if kk in x})
        except Exception: pass
    files = sorted(glob.glob(os.path.join(HERE, "era*.json")))
    if not files:
        print("No part files found in", HERE); sys.exit(1)
    for f in files:
        with open(f) as fh:
            try:
                arr = json.load(fh)
            except Exception as e:
                print(f"!! {os.path.basename(f)}: JSON error {e}"); sys.exit(1)
        print(f"  {os.path.basename(f)}: {len(arr)} events")
        for e in arr:
            events.append(e)

    # clean strings + validate
    seen = {}
    out = []
    used_images = set()
    warnings = []
    for e in events:
        for k in ("title","blurb","detail","date","category","era","source"):
            if k in e and isinstance(e[k], str): e[k] = clean(e[k])
        if "sources" in e and isinstance(e["sources"], list):
            for s in e["sources"]:
                if isinstance(s, dict):
                    if "name" in s: s["name"] = clean(s["name"])
        # normalize era/category
        if e.get("era") not in ERA_ORDER:
            warnings.append(f"bad era: {e.get('era')} :: {e.get('title')}")
        if e.get("category") not in CATS:
            warnings.append(f"bad category: {e.get('category')} :: {e.get('title')}")
        # must have a source
        has_src = (e.get("sources") and len(e["sources"])>0 and e["sources"][0].get("url")) or e.get("sourceUrl")
        if not has_src:
            warnings.append(f"NO SOURCE: {e.get('title')}")
        # sanitize implausible sortKeys (e.g. 19691) -> derive year from the date
        sk = e.get("sortKey")
        if not isinstance(sk, int) or sk < -2000 or sk > 2100:
            m = re.search(r'\d{3,4}', str(e.get("date","")))
            e["sortKey"] = int(m.group()) if m else 0
        # drop known redundant additions
        if norm_title(e.get("title","")) in SKIP_TITLES:
            continue
        # assign significance weight
        e["weight"] = weight_for(e.get("title",""))
        # attach cached image if available
        img = IMAGES.get(norm_title(e.get("title","")))
        if img and img.get("src") and img["src"] not in used_images:
            e["image"] = img["src"]
            e["imageCredit"] = img.get("credit","")
            used_images.add(img["src"])
        h = HIST.get(norm_title(e.get("title","")))
        if h:
            e["historian"] = {kk: clean(vv) for kk, vv in h.items()}
        p = PRIMARY.get(norm_title(e.get("title","")))
        if p:
            e["primary"] = {"name": clean(p["name"]), "url": p["url"]}
        fic = FICTION.get(norm_title(e.get("title","")))
        if fic:
            e["fiction"] = [{kk: clean(vv) if isinstance(vv, str) else vv for kk, vv in w.items()} for w in fic]
        rd = READING.get(norm_title(e.get("title","")))
        if rd:
            hw = norm_title(e.get("historian", {}).get("work", "")) if e.get("historian") else ""
            def _dup(b):
                nb = norm_title(b.get("book", ""))
                return bool(nb and hw and (nb in hw or hw[:len(nb)] == nb))
            rd = [b for b in rd if not _dup(b)]
            if rd:
                e["reading"] = [{kk: clean(vv) if isinstance(vv, str) else vv for kk, vv in b.items()} for b in rd]
        # dedupe by normalized title
        key = norm_title(e.get("title",""))
        if key in seen:
            continue
        seen[key] = True
        out.append(e)

    # sort by era order, then sortKey, then date
    def sk(e):
        return (ERA_ORDER.get(e.get("era"), 99), e.get("sortKey", 0))
    out.sort(key=sk)

    # write data.js
    header = ("/* New York, in Time — verified event dataset (expanded)\n"
              "   {n} turning points across six eras, each with a source link.\n"
              "   Auto-assembled from per-era research; see METHODOLOGY.md. */\n"
              "window.NYC_EVENTS = ").format(n=len(out))
    body = json.dumps(out, ensure_ascii=False, indent=0)
    # compact: one object per line
    with open(os.path.join(ROOT, "data.js"), "w") as fh:
        fh.write(header)
        fh.write("[\n")
        for i, e in enumerate(out):
            fh.write(json.dumps(e, ensure_ascii=False))
            fh.write(",\n" if i < len(out)-1 else "\n")
        fh.write("];\n")

    print(f"\nWrote {len(out)} events to data.js (from {len(events)} raw, {len(events)-len(out)} dupes removed)")
    # per-era counts
    from collections import Counter
    c = Counter(e.get("era") for e in out)
    for era in ERAS:
        print(f"  {c.get(era,0):>3}  {era}")
    if warnings:
        print("\nWARNINGS:")
        for w in warnings[:40]: print("  -", w)

if __name__ == "__main__":
    main()
