# Raw retrieval cache (not committed)

During the run, 68 topics were fetched from the ServiceNow docs khub API and cleaned
into `/tmp/kilo/snc_pages/`. They are intentionally **not** committed here:

- they are large (~350 KB) and re-fetchable;
- the authoritative, stable artifact is `../topics.json`, which records the exact map
  ID, content ID, and API URL for every topic;
- committing ServiceNow documentation text would duplicate vendor content.

Reproduce with:

```bash
python3 - <<'PY'
import json, urllib.request
for row in json.load(open("../topics.json")):
    html = urllib.request.urlopen(urllib.request.Request(
        row["api_url"], headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read()
    open(row["key"] + ".html", "wb").write(html)
PY
```
