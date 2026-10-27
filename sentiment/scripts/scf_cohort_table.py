"""One table: SCF contributions by family income quartile vs Michigan sentiment, every wave 1989-2025.

Rows: one per SCF wave and income quartile (13 waves x 4 = 52 rows).
SCF measures (estimate and replicate-weight SE, from contributions/scf/output/scf_contrib_long.csv):
  - pct_families_contributing_dc: families where the head or spouse makes employee contributions to a
    current-job DC plan, % of all families in the quartile
  - pct_takeup_families_with_dc: of families with a current-job DC plan, % contributing
  - employee_dc_pct_wages: annualized current employee DC contributions / annualized current main-job pay
  - employer_dc_pct_wages: same for employer contributions
  DC items are current at the interview (survey year); quartiles use prior-year family income.
Sentiment: University of Michigan ICS, calendar-year average of the survey year, for the income third
  matched to the quartile (Q1 -> bottom third, Q2 and Q3 -> middle, Q4 -> top), plus all respondents.
Output: output/scf_cohort_contrib_vs_sentiment.csv
"""
import os
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RW = os.path.dirname(BASE)
OUT = os.path.join(BASE, "output")

s = pd.read_csv(os.path.join(RW, "contributions/scf/output/scf_contrib_long.csv"))
s = s[s.group.str.match(r"^income quartile \d$")]
keep = {"pct_families_contributing_dc_current_job": "pct_families_contributing_dc",
        "pct_takeup_families_with_dc_plan": "pct_takeup_families_with_dc",
        "agg_dc_employee_pct_of_current_wages": "employee_dc_pct_wages",
        "agg_dc_employer_pct_of_current_wages": "employer_dc_pct_wages"}
s = s[s.measure.isin(keep)].assign(measure=lambda d: d.measure.map(keep))
s["quartile"] = s.group.str[-1].astype(int)
est = s.pivot_table(index=["year", "quartile"], columns="measure", values="estimate")
se = s.pivot_table(index=["year", "quartile"], columns="measure", values="se").add_suffix("_se")
n = s[s.measure == "pct_families_contributing_dc"].set_index(["year", "quartile"])["n"].rename("n_families")
t = est.join(se).join(n).reset_index()

sent = pd.read_csv(os.path.join(OUT, "cohort_sentiment_annual.csv"), index_col="year")
qmap = {1: "bottom", 2: "middle", 3: "middle", 4: "top"}
t["sentiment_group"] = t.quartile.map(qmap) + " third"
t["ics_own_group"] = [sent.loc[y, g] for y, g in zip(t.year, t.quartile.map(qmap))]
t["ics_all"] = t.year.map(sent["all"])
t["ics_bottom_third"] = t.year.map(sent["bottom"])
t["ics_middle_third"] = t.year.map(sent["middle"])
t["ics_top_third"] = t.year.map(sent["top"])

cols = ["year", "quartile", "n_families",
        "pct_families_contributing_dc", "pct_families_contributing_dc_se",
        "pct_takeup_families_with_dc", "pct_takeup_families_with_dc_se",
        "employee_dc_pct_wages", "employee_dc_pct_wages_se",
        "employer_dc_pct_wages", "employer_dc_pct_wages_se",
        "sentiment_group", "ics_own_group", "ics_all", "ics_bottom_third", "ics_middle_third", "ics_top_third"]
t = t[cols].sort_values(["year", "quartile"])
t.to_csv(os.path.join(OUT, "scf_cohort_contrib_vs_sentiment.csv"), index=False, float_format="%.2f")
print(t.to_string(index=False))
