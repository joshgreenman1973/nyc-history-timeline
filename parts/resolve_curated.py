#!/usr/bin/env python3
"""Apply curator decisions (curate_*.json) to images.json.
- action "keep":   leave the existing image
- action "skip":   remove the image (better none than a wrong one)
- action "replace":resolve the given Commons File: to a ~720px thumbnail URL and use it
Then merge.py attaches the (now curated) images."""
import json, glob, os, re, urllib.parse, urllib.request, time

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(HERE, "images.json")
UA = "NYCHistoryTimeline/1.0 (educational; josh.greenman@gmail.com)"

def nt(s): return re.sub(r'[^a-z0-9]', '', s.lower())

def api(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode())

def commons_thumb(filetitle, width=760):
    if not filetitle.lower().startswith("file:"):
        filetitle = "File:" + filetitle
    url = ("https://commons.wikimedia.org/w/api.php?action=query&format=json"
           "&prop=imageinfo&iiprop=url&iiurlwidth=%d&titles=%s" % (width, urllib.parse.quote(filetitle)))
    try:
        d = api(url)
        pages = d.get("query", {}).get("pages", {})
        for _, p in pages.items():
            if "missing" in p: return None
            ii = p.get("imageinfo", [])
            if ii and ii[0].get("thumburl"):
                return ii[0]["thumburl"]
    except Exception as e:
        print("  ! api error", filetitle, e)
    return None

def credit_from(filetitle):
    s = re.sub(r'^File:', '', filetitle)
    s = re.sub(r'\.(jpg|jpeg|png|gif|tif|tiff|svg)$', '', s, flags=re.I)
    s = s.replace('_', ' ').strip()
    return (s[:44] + '…') if len(s) > 45 else s

def main():
    images = json.load(open(IMAGES)) if os.path.exists(IMAGES) else {}
    files = sorted(glob.glob(os.path.join(HERE, "curate_*.json")))
    kept = replaced = skipped = failed = 0
    for f in files:
        try: arr = json.load(open(f))
        except Exception as e:
            print("bad", f, e); continue
        for x in arr:
            key = nt(x.get("title", ""))
            action = (x.get("action") or "").lower()
            if action == "keep":
                kept += 1
            elif action == "skip":
                images[key] = None; skipped += 1
            elif action == "replace" and x.get("commonsFile"):
                thumb = commons_thumb(x["commonsFile"])
                if thumb:
                    images[key] = {"src": thumb, "credit": credit_from(x["commonsFile"])}
                    replaced += 1
                else:
                    failed += 1
                    print("  fail resolve:", x.get("title"), x.get("commonsFile"))
                time.sleep(0.1)
    json.dump(images, open(IMAGES, "w"), ensure_ascii=False, indent=1)
    got = sum(1 for v in images.values() if v)
    print(f"kept={kept} replaced={replaced} skipped={skipped} failed={failed}")
    print(f"images.json now: {got} images across {len(images)} events")

if __name__ == "__main__":
    main()
