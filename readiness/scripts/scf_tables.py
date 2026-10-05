"""Wide tables from output/scf_readiness_long.csv. Run after scf_readiness.py.
python3 readiness/scripts/scf_tables.py"""
from pathlib import Path
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "output"
r = pd.read_csv(OUT / "scf_readiness_long.csv")
LAB = {"race1": "white_nh", "race2": "black_nh", "race3": "hispanic", "race4": "other_multi",
       "incq1": "inc_q1", "incq2": "inc_q2", "incq3": "inc_q3", "incq4": "inc_q4", "all": "all"}


def wide(d, col):
    est = d.pivot(index="survey_year", columns=col, values="estimate")
    se = d.pivot(index="survey_year", columns=col, values="se").add_suffix("_se")
    cols = list(est.columns)
    return est.join(se)[[c for k in cols for c in (k, f"{k}_se")]].round(3)


cov = r[r.block == "coverage"]
for stat, name in [("pct_any_ret_acct", "c1_pct_any_ret_acct_by_age"), ("pct_db_plan", "c2_pct_db_plan_by_age"),
                   ("pct_acct_or_db", "c3_pct_acct_or_db_by_age"), ("pct_dc_current_job", "c4_pct_dc_current_job_by_age")]:
    wide(cov[(cov.group == "all") & (cov.stat == stat)], "age").to_csv(OUT / f"{name}.csv")
for age in ["25-64", "55-64"]:
    for stat in ["pct_any_ret_acct", "pct_acct_or_db"]:
        d = cov[(cov.age == age) & (cov.stat == stat) & (cov.group != "all")].copy()
        d["group"] = d.group.map(LAB)
        for kind in ["race", "inc"]:
            dd = d[d.group.str.startswith("inc") == (kind == "inc")]
            if dd.empty:
                continue
            t = wide(dd, "group")
            n = dd.pivot(index="survey_year", columns="group", values="n_records").add_prefix("n_hh_").round(0)
            t.join(n).to_csv(OUT / f"c5_{stat}_{age.replace('-', '')}_by_{kind}.csv")
near = r[r.block == "near"].copy()
near["group"] = near.group.map(LAB)
for stat in near.stat.unique():
    wide(near[near.stat == stat], "group").to_csv(OUT / f"n_{stat}_5564.csv")

c3 = cov[(cov.group == "all") & (cov.stat == "pct_acct_or_db")].pivot(index="survey_year", columns="age", values="estimate")
print("Any retirement account or DB plan, % of households:\n", c3[["25-64", "55-64"]].round(1).T.to_string())
nh = near[near.group == "all"].pivot(index="survey_year", columns="stat", values="estimate")
print("55-64 median account/income ratio (all hh, holders):\n", nh[["median_ratio_all", "median_ratio_holders"]].round(2).T.to_string())
