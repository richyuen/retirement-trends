"""Two small public tables.

1. BLS National Compensation Survey (NCS) plan provisions, private industry, all workers.
   raw/bls_nb_data_annuity_provisions.tsv and raw/bls_nb_series_annuity_provisions.tsv are the rows of
   https://download.bls.gov/pub/time.series/nb/nb.data.1.AllData and nb.series for the series below
   (filtered with grep; full files are 45MB/25MB and not kept). Values are % of participants in that
   plan type whose plan has the provision (a plan can offer several distribution methods, so they add
   to more than 100).
2. CPS ASEC: % of people receiving annuity income, by age. Read-only from the cps/ thread's output
   (../cps/output/asec_retirement_income_by_age.csv; measure `pct_annuity` = RET_SC 6 legacy, ANN_YN=1 updated).
Run: python3 annuities/scripts/bls_cps_tables.py
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
d = pd.read_csv(ROOT / "raw" / "bls_nb_data_annuity_provisions.tsv", sep="\t")
d.columns = d.columns.str.strip()
d["series_id"] = d.series_id.str.strip()
s = pd.read_csv(ROOT / "raw" / "bls_nb_series_annuity_provisions.tsv", sep="\t")
s.columns = s.columns.str.strip()
s["series_id"] = s.series_id.str.strip()
lab = {"887": "DB (traditional): full lump sum available", "888": "DB (traditional): any lump sum available",
       "889": "DB (traditional): lump sum not available", "896": "DB (traditional): partial lump sum + reduced annuity",
       "925": "DB (traditional): lump sum not determinable",
       "R08": "DC deferred profit-sharing: annuity available", "R23": "DC money purchase: annuity available",
       "S14": "DC savings & thrift (401(k)-type): annuity available", "S15": "DC savings & thrift: installments available",
       "S16": "DC savings & thrift: lump sum available", "S17": "DC savings & thrift: other method",
       "S18": "DC savings & thrift: method not determinable"}
d = d.merge(s[["series_id", "provision_code"]], on="series_id")
d["provision_code"] = d.provision_code.astype(str).str.strip()
d["provision"] = d.provision_code.map(lab)
t = d.pivot_table(index=["series_id", "provision"], columns="year", values="value").reset_index()
t.to_csv(ROOT / "output" / "bls_ncs_payout_provisions_private.csv", index=False)
print("BLS NCS, private industry, % of plan participants with provision:")
print(t.drop(columns="series_id").to_string(index=False))

c = pd.read_csv(ROOT.parent / "cps" / "output" / "asec_retirement_income_by_age.csv")
keep = c[c.age.isin(["55-59", "60-64", "65-69", "70-74", "75-79", "80+", "65+"])]
w = keep.pivot_table(index=["asec_year", "income_year", "file", "system"], columns="age", values="pct_annuity").reset_index()
w.to_csv(ROOT / "output" / "cps_pct_receiving_annuity_income.csv", index=False)
print("\nCPS ASEC, % of persons receiving annuity income (updated system 2017R+; legacy before):")
print(w[["asec_year", "file", "60-64", "65+", "75-79", "80+"]].to_string(index=False))
