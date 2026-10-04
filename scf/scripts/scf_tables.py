"""Wide tables from scf/output/scf_estimates_long.csv, plus SCF vs IRS SOI incidence comparison.
Run after scf_analysis.py: python3 scf/scripts/scf_tables.py"""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
r = pd.read_csv(OUT / "scf_estimates_long.csv")
BANDS = ["60+", "60-64", "65-69", "70-74", "75-79", "80+"]
TABLES = {
    "t1_withdrawal_incidence_holders": "wd_any_per100_holders",
    "t2_ira_withdrawal_incidence": "wd_ira_per100_ira_holders",
    "t3_pension_acct_withdrawal_incidence": "wd_pen_per100_pen_holders",
    "t4_withdrawers_pct_all_households": "wd_any_pct_all_hh",
    "t5_dollar_withdrawal_rate": "wd_dollar_rate_pct",
    "t6_median_withdrawal_2022usd": "median_wd_if_any",
    "t7_aggregate_withdrawals_bn_2022usd": "aggregate_wd_bn",
    "t8_pct_with_retirement_account": "pct_with_any_ret_acct",
    "t9_pct_with_ira": "pct_with_ira",
    "t10_median_ret_acct_if_any_2022usd": "median_ret_acct_if_any",
    "t11_aggregate_ret_acct_bn_2022usd": "aggregate_ret_acct_bn",
    "t12_households_millions": "hh_millions",
}
for name, stat in TABLES.items():
    d = r[r.stat == stat]
    est = d.pivot(index="survey_year", columns="age_band", values="estimate")[BANDS]
    se = d.pivot(index="survey_year", columns="age_band", values="se")[BANDS].add_suffix("_se")
    t = est.join(se)[[c for b in BANDS for c in (b, b + "_se")]]
    t.insert(0, "ref_year", t.index - 1)
    t.round(2).to_csv(OUT / f"{name}.csv")

# SCF (household, any IRA/Keogh holder, age of reference person at interview) vs IRS SOI
# (individual IRA owners, age at end of tax year), same reference year.
irs = json.load(open(ROOT.parent / "data" / "irs_derived.json"))["inc"]
order = ["u60", "60-64", "65-69", "70-74", "75-79", "80+", "60-69", "70+", "all"]
rows = []
for sy in sorted(r[r.stat == "wd_ira_per100_ira_holders"].survey_year.unique()):
    ry = str(sy - 1)
    for b in ["60-64", "65-69", "70-74", "75-79", "80+"]:
        s = r[(r.stat == "wd_ira_per100_ira_holders") & (r.survey_year == sy) & (r.age_band == b)].iloc[0]
        rows.append(dict(ref_year=int(ry), age_band=b, scf_ira_incidence=round(s.estimate, 1), scf_se=round(s.se, 1),
                         irs_ira_incidence=irs[ry][order.index(b)] if ry in irs else None))
pd.DataFrame(rows).to_csv(OUT / "t13_scf_vs_irs_ira_incidence.csv", index=False)
print("tables written to", OUT)
