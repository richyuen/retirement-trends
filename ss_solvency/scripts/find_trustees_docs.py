"""Walk govinfo's CDOC (Congressional Documents) browse tree and list every
House/Senate document whose title is an OASDI, HI or SMI Trustees Report.

Output: raw/govinfo_trustees_index.csv (packageid, title, publishdate, pdf/html size).
govinfo's browse service needs no API key (the api.govinfo.gov search needs one).
"""
import csv, json, os, sys, time, urllib.parse, urllib.request

BASE = "https://www.govinfo.gov/wssearch/rb/cdoc"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "raw", "govinfo_trustees_index.csv")
KEYS = ("OLD-AGE AND SURVIVORS", "HOSPITAL INSURANCE", "SUPPLEMENTARY MEDICAL")


def get(path):
    url = BASE + "/" + urllib.parse.quote(path) + "?fetchChildrenOnly=1"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as e:  # transient
            time.sleep(2)
    print("FAILED", url, file=sys.stderr)
    return {"childNodes": []}


def main():
    top = json.load(urllib.request.urlopen(BASE + "?fetchChildrenOnly=0", timeout=60))
    rows = []
    for cong in top["childNodes"]:
        cpath = cong["nodeValue"]["browsePathAlias"]
        for cls in get(cpath)["childNodes"]:
            if cls["nodeValue"]["value"] not in ("HDOC", "SDOC"):
                continue
            for rng in get(cls["nodeValue"]["browsePathAlias"])["childNodes"]:
                nv = rng["nodeValue"]
                docs = get(nv["browsePathAlias"])["childNodes"] if nv.get("browsePathAlias") else []
                for d in docs:
                    v = d["nodeValue"]
                    t = (v.get("title") or "").upper()
                    if any(k in t for k in KEYS) and "TRUST" in t:
                        rows.append({k: v.get(k, "") for k in
                                     ("packageid", "title", "publishdate", "pdfsize", "htmlsize")})
        print(cong["nodeValue"]["displayValue"], "-> running total", len(rows))
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"{len(rows)} trustees-report documents -> {OUT}")


if __name__ == "__main__":
    main()
