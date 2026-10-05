"""Annuity reserves at U.S. life insurers, Federal Reserve Financial Accounts (Z.1), 1985-2025.

Input: raw/z1_csv_files_2026-09-10.zip (https://www.federalreserve.gov/releases/z1/current/z1_csv_files.zip,
release of 2026-09-10, data through 2026Q2). Series (millions of $):
  FL543150005  Life insurance companies; pension entitlements (= "Annuity reserves held by life insurance
               companies, excluding unallocated contracts held by pension funds", L.116 footnote 2,
               raw/z1_L116_2026-03-19.htm). Individual and allocated group annuities, deferred and payout,
               incl. variable-annuity separate-account values and annuities held inside IRAs.
  FU543150005  same, net transactions (not seasonally adjusted; quarters summed to calendar years)
  LM543131503  Life insurance companies; IRAs (IRA assets held as annuities at life insurers), market value
  LM893131573  All sectors; IRAs (total IRA assets)
  FL154090005  Households and nonprofits; total financial assets
  FL893150005  All sectors; pension entitlements (all DB/DC/annuity claims)
Year-end = Q4. Run: python3 annuities/scripts/z1_annuity_reserves.py
"""
from pathlib import Path
import io, zipfile
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
Z = zipfile.ZipFile(ROOT / "raw" / "z1_csv_files_2026-09-10.zip")


def table(name):
    d = pd.read_csv(io.BytesIO(Z.read(f"csv/{name}.csv")))
    d = d.loc[:, ~d.columns.duplicated()]
    return d.set_index("date").apply(pd.to_numeric, errors="coerce")


lv = table("F6_2_s").join(table("S1M_s")[["FL154090005.Q"]])
fl = table("F6_2_t_tu")[["FU543150005.Q"]]
fl["year"] = fl.index.str[:4].astype(int)
fl_ann = fl[fl.index.str[:4].astype(int) <= 2025].groupby("year")["FU543150005.Q"].agg(["sum", "count"])
q4 = lv[lv.index.str.endswith("Q4")].copy()
q4.index = q4.index.str[:4].astype(int)
q4 = q4.loc[1985:2025]
out = pd.DataFrame({
    "annuity_reserves_bn": q4["FL543150005.Q"] / 1e3,
    "ira_at_life_insurers_bn": q4["LM543131503.Q"] / 1e3,
    "ira_total_bn": q4["LM893131573.Q"] / 1e3,
    "hh_fin_assets_bn": q4["FL154090005.Q"] / 1e3,
    "all_pension_entitlements_bn": q4["FL893150005.Q"] / 1e3,
})
out["annuity_reserves_pct_hh_fin_assets"] = 100 * out.annuity_reserves_bn / out.hh_fin_assets_bn
out["annuity_reserves_pct_all_pension_entitlements"] = 100 * out.annuity_reserves_bn / out.all_pension_entitlements_bn
out["ira_annuity_pct_of_ira_assets"] = 100 * out.ira_at_life_insurers_bn / out.ira_total_bn
f = fl_ann[fl_ann["count"] == 4]["sum"] / 1e3
out["annuity_reserves_net_flow_bn"] = f
out["net_flow_pct_of_prior_yr_reserves"] = 100 * out.annuity_reserves_net_flow_bn / out.annuity_reserves_bn.shift(1)
out.index.name = "year"
out = out.round(2)
out.to_csv(ROOT / "output" / "z1_annuity_reserves.csv")
print(out.loc[[1985, 1990, 1995, 2000, 2005, 2007, 2010, 2015, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
              ["annuity_reserves_bn", "annuity_reserves_pct_hh_fin_assets", "annuity_reserves_pct_all_pension_entitlements",
               "ira_annuity_pct_of_ira_assets", "annuity_reserves_net_flow_bn", "net_flow_pct_of_prior_yr_reserves"]].to_string())
