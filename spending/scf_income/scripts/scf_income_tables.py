"""Wide tables from output/scf_income_long.csv. Columns are SCF survey years (income refers to the prior
calendar year); each estimate column is followed by its standard error (<year>_se).
Run after scf_income_sources.py: python3 spending/scf_income/scripts/scf_income_tables.py
"""
from pathlib import Path
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "output"
r = pd.read_csv(OUT / "scf_income_long.csv")
GROUPS = ["65+", "55-64", "65-74", "75+", "all"]

SRC = ["wage", "bus", "intdiv", "kg", "ss", "pen", "acctwd", "pen_plus_acctwd", "sspen_unalloc", "transfers", "other"]
TABLES = {
    "t1_share_of_aggregate_income": [f"share_agg_{k}" for k in SRC] + ["share_agg_other_raw_uncapped",
                                                                      "share_agg_comparable_other_plus_acctwd"],
    "t2_share_of_aggregate_income_excl_capital_gains": [f"share_agg_xkg_{k}" for k in SRC if k != "kg"],
    "t3_pct_households_with_income_from": [f"pct_with_{k}" for k in SRC if k not in ("pen_plus_acctwd",)]
    + ["pct_with_pen_or_acctwd", "pct_receiving_ss_now", "pct_receiving_pension_now"],
    "t4_typical_household_shares_and_ss_reliance": ["mean_hh_share_ss", "mean_hh_share_pen_plus_acctwd",
                                                    "mean_hh_share_wage", "mean_hh_share_capital",
                                                    "pct_ss_ge50pct_of_income", "pct_ss_ge90pct_of_income",
                                                    "mean_income_2022usd"],
    "t5_networth_composition": ["pct_networth_ret", "pct_networth_homeeq", "pct_networth_othfin",
                                "pct_networth_othnfin", "pct_networth_othdebt", "pct_assets_ret",
                                "mean_networth_2022usd"],
    "t6_db_vs_dc_coverage": ["pct_has_db_receiving", "pct_has_db_future_or_cj", "pct_has_db_any", "pct_has_ret",
                             "pct_has_ira", "pct_has_dcacct", "pct_db_only", "pct_dc_only", "pct_db_and_dc",
                             "pct_neither", "pct_has_home"],
}

for name, stats in TABLES.items():
    d = r[r.stat.isin(stats) & r.group.isin(GROUPS)].copy()
    d["group"] = pd.Categorical(d.group, GROUPS)
    d["stat"] = pd.Categorical(d.stat, stats)
    est = d.pivot_table(index=["group", "stat"], columns="survey_year", values="estimate", observed=True)
    se = d.pivot_table(index=["group", "stat"], columns="survey_year", values="se", observed=True)
    cols = []
    for y in est.columns:
        cols += [(str(y), est[y]), (f"{y}_se", se[y])]
    w = pd.DataFrame(dict(cols), index=est.index).round(2)
    w.to_csv(OUT / f"{name}.csv")
    print(name, w.shape)
