"""Fetch BLS ECEC (CM) series and CPI-U from data.bls.gov "timeseries" pages.

download.bls.gov/pub/time.series/cm/ returns 403 from this environment and the BLS public API
(api.bls.gov) reported its daily request threshold exhausted, so this script saves the public
HTML series-report pages (https://data.bls.gov/timeseries/<SERIES_ID>) under raw/bls/ and
parse_bls.py extracts the data table from them.

Series (ECEC, https://www.bls.gov/ncs/ect/ ; ids as in cm.series):
  CMU{owner}{component}000000000{type}
    owner     1 civilian, 2 private industry, 3 state and local government
    component 010 total compensation, 020 wages and salaries, 030 total benefits,
              180 retirement and savings, 190 defined benefit, 200 defined contribution
    type      D cost per hour worked ($), P percent of total compensation
  CUUR0000SA0  CPI-U, U.S. city average, all items, NSA (annual averages requested)
Run: python3 -I scripts/fetch_bls.py   (from contributions/admin/)
"""
import os, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
RAW = HERE / "raw" / "bls"
RAW.mkdir(parents=True, exist_ok=True)
contact = os.environ.get("BLS_CONTACT_EMAIL", "")
UA = "Mozilla/5.0" + (f" (contact: {contact})" if contact else "")

series = [f"CMU{o}{c}000000000{t}" for o in "123" for c in ("010", "020", "030", "180", "190", "200") for t in "DP"]
jobs = [(s, 2004, 2026, False) for s in series] + [("CUUR0000SA0", 1975, 2026, True)]
for sid, y0, y1, ann in jobs:
    out = RAW / f"{sid}.html"
    if out.exists() and out.stat().st_size > 20000:
        continue
    url = (f"https://data.bls.gov/timeseries/{sid}?from_year={y0}&to_year={y1}&output_view=data"
           f"&include_graphs=false" + ("&annual_averages=true" if ann else ""))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        out.write_bytes(r.read())
    print("saved", sid, out.stat().st_size)
    time.sleep(1.5)
print("done:", len(jobs), "series pages in", RAW)
