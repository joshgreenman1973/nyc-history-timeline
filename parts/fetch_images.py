#!/usr/bin/env python3
"""Fetch a representative image per event from Wikimedia (pageimages API).
Caches results in parts/images.json keyed by normalized title so it is incremental
and stable across merges. merge.py attaches these to events.

Strategy per event: derive a Wikipedia page title from a wikipedia.org source URL if present,
else search Wikipedia by the event title; then pull a ~640px lead thumbnail via pageimages.
Skips events with no good image (cards render fine without one)."""
import json, os, re, time, urllib.parse, urllib.request, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "images.json")
UA = "NYCHistoryTimeline/1.0 (educational timeline; contact josh.greenman@gmail.com)"

def norm_title(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())

def api(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())

def title_from_sources(ev):
    for s in ev.get("sources", []):
        u = s.get("url", "")
        m = re.search(r'en\.wikipedia\.org/wiki/([^#?]+)', u)
        if m:
            return urllib.parse.unquote(m.group(1)).replace("_", " ")
    return None

def search_title(query):
    url = ("https://en.wikipedia.org/w/api.php?action=query&list=search&format=json"
           "&srlimit=1&srsearch=" + urllib.parse.quote(query))
    try:
        d = api(url)
        hits = d.get("query", {}).get("search", [])
        return hits[0]["title"] if hits else None
    except Exception:
        return None

def thumb_for_title(title, size=640):
    url = ("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages"
           "&piprop=thumbnail|name&pithumbsize=%d&titles=%s" % (size, urllib.parse.quote(title)))
    try:
        d = api(url)
        pages = d.get("query", {}).get("pages", {})
        for _, p in pages.items():
            th = p.get("thumbnail", {})
            if th.get("source"):
                return th["source"], p.get("title", title)
    except Exception:
        return None, None
    return None, None

def main():
    txt = open(os.path.join(ROOT, "data.js")).read()
    events = json.loads(txt[txt.index('['):txt.rindex(']')+1])
    cache = {}
    if os.path.exists(CACHE):
        cache = json.load(open(CACHE))

    fetched = 0; skipped = 0; had = 0
    for ev in events:
        key = norm_title(ev["title"])
        if key in cache:  # already resolved (incl. explicit nulls)
            had += 1
            continue
        # 1) try wikipedia source url title
        title = title_from_sources(ev)
        src, resolved = (thumb_for_title(title) if title else (None, None))
        # 2) fall back to search
        if not src:
            st = search_title(ev["title"] + " New York")
            if st:
                src, resolved = thumb_for_title(st)
        if src:
            cache[key] = {"src": src, "credit": resolved or title or ev["title"]}
            fetched += 1
        else:
            cache[key] = None  # cache the miss so we don't retry endlessly
            skipped += 1
        if (fetched + skipped) % 20 == 0:
            json.dump(cache, open(CACHE, "w"), ensure_ascii=False, indent=0)
            print(f"  ...{fetched} images, {skipped} misses so far")
        time.sleep(0.12)

    json.dump(cache, open(CACHE, "w"), ensure_ascii=False, indent=1)
    got = sum(1 for v in cache.values() if v)
    print(f"\nDone. cached-before={had} newly-fetched={fetched} misses={skipped}")
    print(f"images.json now holds {got} images across {len(cache)} events")

if __name__ == "__main__":
    main()
