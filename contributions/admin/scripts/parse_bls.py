"""Parse BLS ECEC series pages saved by fetch_bls.py into tidy CSVs.

Input: raw/bls/CMU*.html (https://data.bls.gov/timeseries/<id>)
Outputs: output/bls_ecec_retirement_quarterly.csv (long), output/bls_ecec_retirement_annual.csv (wide, March = Q1
  reference, plus 4-quarter averages)
Run: python3 -I scripts/parse_bls.py
"""
import re
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parents[1]
RAW, OUT = HERE / "raw" / "bls", HERE / "output"
OWN = {"1": "civilian", "2": "private industry", "3": "state and local government"}
COMP = {"010": "total_comp", "020": "wages", "030": "benefits", "180": "retirement", "190": "db", "200": "dc"}
rows = []
for p in sorted(RAW.glob("CMU*.html")):
    sid = p.stem
    t = next(x for x in pd.read_html(p) if "Estimate Value" in x.columns)
    t = t[t.Period.astype(str).str.match(r"Qtr\d")]
    for _, r in t.iterrows():
        v = pd.to_numeric(r["Estimate Value"], errors="coerce")
        rows.append(dict(series_id=sid, ownership=OWN[sid[3]], component=COMP[sid[4:7]],
                         measure={"D": "cost_per_hour_usd", "P": "pct_total_comp"}[sid[-1]],
                         year=int(r.Year), quarter=int(r.Period[-1]), value=v))
q = pd.DataFrame(rows)
q["source"] = "BLS ECEC, https://data.bls.gov/timeseries/" + q.series_id
q["note"] = ("Employer cost per hour worked / % of total compensation; Qtr1=March, Qtr2=June, Qtr3=Sept, Qtr4=Dec "
             "reference periods. NAICS-based series start 2004 Q1.")
q.to_csv(OUT / "bls_ecec_retirement_quarterly.csv", index=False)

wide = q.pivot_table(index=["ownership", "year", "quarter"], columns=["component", "measure"], values="value")
wide.columns = [f"{c}_{m}" for c, m in wide.columns]
wide = wide.reset_index()
wide["dc_share_of_retirement_cost_pct"] = 100 * wide.dc_cost_per_hour_usd / wide.retirement_cost_per_hour_usd
wide["dc_pct_of_wages"] = 100 * wide.dc_cost_per_hour_usd / wide.wages_cost_per_hour_usd
wide["db_pct_of_wages"] = 100 * wide.db_cost_per_hour_usd / wide.wages_cost_per_hour_usd
march = wide[wide.quarter == 1].drop(columns="quarter").assign(basis="March (Q1)")
avg = wide.groupby(["ownership", "year"]).mean(numeric_only=True).reset_index()
nq = wide.groupby(["ownership", "year"]).size().values
avg = avg[nq == 4].drop(columns="quarter").assign(basis="mean of 4 quarters")
ann = pd.concat([march, avg]).sort_values(["basis", "ownership", "year"])
ann["source"] = "BLS ECEC series CMU{1,2,3}{010,020,030,180,190,200}000000000{D,P} via data.bls.gov/timeseries"
ann["note"] = "dc/db pct_of_wages and dc share of retirement computed from $/hour; pct_total_comp as published (1 decimal)."
ann.round(3).to_csv(OUT / "bls_ecec_retirement_annual.csv", index=False)

m = march.set_index(["ownership", "year"])
cols = ["dc_pct_total_comp", "db_pct_total_comp", "dc_cost_per_hour_usd", "db_cost_per_hour_usd", "dc_pct_of_wages",
        "db_pct_of_wages", "dc_share_of_retirement_cost_pct"]
for o in ["private industry", "state and local government"]:
    print(o); print(m.loc[o].loc[[2004, 2008, 2012, 2016, 2020, 2024, 2025, 2026], cols].round(2).to_string())
