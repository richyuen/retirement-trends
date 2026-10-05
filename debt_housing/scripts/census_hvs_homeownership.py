"""Census CPS/HVS homeownership rates by age of householder.
Inputs (raw/): hvs_histtab12.xlsx (annual households and owners by age, 1982-2025),
hvs_histtab19.xlsx (quarterly homeownership rates by age, 1994Q1-2026Q2), both from
https://www.census.gov/housing/hvs/data/histtabs.html
Rate = owner households / all households x 100 (Table 12). 1993 and 2002 appear twice
(old and revised population controls, 'r' columns); the revised value is kept.
2025 annual covers 11 months (no October 2025 collection).
Output: output/hvs_homeownership_by_age_annual.csv, hvs_homeownership_by_age_quarterly.csv
"""
from pathlib import Path
import re
import pandas as pd, openpyxl

HERE = Path(__file__).resolve().parents[1]
RAW, OUT = HERE / "raw", HERE / "output"

rows = [[c for c in r] for r in openpyxl.load_workbook(RAW / "hvs_histtab12.xlsx", read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True)]
recs, years = {}, None
for r in rows:
    if r[0] == "Age of Householder":
        years = [str(c) for c in r[1:] if c is not None]
        continue
    if years is None or r[0] is None or not isinstance(r[1], (int, float)):
        continue
    label = re.sub(r"[.…]+", " ", str(r[0])).strip()
    vals = [c for c in r[1:] if c is not None]
    for i, y in enumerate(years):
        if 2 * i + 1 < len(vals):
            recs.setdefault(y, {})[label] = vals[2 * i + 1] / vals[2 * i] * 100
df = pd.DataFrame(recs).T
df.index.name = "year_label"
# keep revised columns for 1993/2002, drop the unrevised duplicate
df["year"] = df.index.str.extract(r"^(\d{4})", expand=False).astype(int)
df["revised"] = df.index.str.contains("r")
df = df.sort_values(["year", "revised"]).groupby("year").last()
keep = {"United States, total": "all", "55 to 64 years": "55-64", "65 to 69 years": "65-69", "70 to 74 years": "70-74",
        "75 years and over": "75+", "65 years and over": "65+", "Less than 35 years": "<35"}
ann = df[[k for k in keep]].rename(columns=keep)
ann.round(1).to_csv(OUT / "hvs_homeownership_by_age_annual.csv")
print("HVS annual homeownership rate (%) by age of householder:")
print(ann.loc[[1982, 1990, 2000, 2004, 2010, 2016, 2019, 2022, 2024, 2025]].round(1).to_string())

# quarterly Table 19
rows = [[c for c in r if c is not None] for r in openpyxl.load_workbook(RAW / "hvs_histtab19.xlsx", read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True)]
q, yr = [], None
for r in rows:
    if len(r) == 1 and isinstance(r[0], int):
        yr = r[0]
    elif yr and len(r) == 7 and isinstance(r[1], (int, float)):
        qn = {"1st": 1, "2nd": 2, "3rd": 3, "4th": 4}[str(r[0])[:3]]
        q.append([yr, qn] + list(r[1:]))
qt = pd.DataFrame(q, columns=["year", "q", "all", "<35", "35-44", "45-54", "55-64", "65+"])
qt.to_csv(OUT / "hvs_homeownership_by_age_quarterly.csv", index=False)
print("Quarterly 65+ (Table 19): min", qt.loc[qt["65+"].idxmin(), ["year", "q", "65+"]].tolist(),
      "max", qt.loc[qt["65+"].idxmax(), ["year", "q", "65+"]].tolist(), "latest", qt.iloc[-1][["year", "q", "65+", "all"]].tolist())

# share of all households headed by someone 60+ / 65+ (context for the NY Fed debt shares)
tot, years = {}, None
for r in openpyxl.load_workbook(RAW / "hvs_histtab12.xlsx", read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True):
    if r[0] == "Age of Householder":
        years = [str(c) for c in r[1:] if c is not None]
        continue
    if years and r[0] and isinstance(r[1], (int, float)):
        lab = re.sub(r"[.…]+", " ", str(r[0])).strip()
        vals = [c for c in r[1:] if c is not None]
        for i, y in enumerate(years):
            tot.setdefault(int(y[:4]), {})[lab] = vals[2 * i]  # revised column (later) overwrites
hh = pd.DataFrame(tot).T.sort_index()
sh = pd.DataFrame({"pct_households_head_60plus": 100 * (hh["60 to 64 years"] + hh["65 years and over"]) / hh["United States, total"],
                   "pct_households_head_65plus": 100 * hh["65 years and over"] / hh["United States, total"]})
sh.index.name = "year"
sh.round(2).to_csv(OUT / "hvs_share_households_head_60plus.csv")
print("Share of households with head 60+ / 65+ (%):", sh.loc[[1999, 2008, 2019, 2025]].round(1).to_dict("index"))
