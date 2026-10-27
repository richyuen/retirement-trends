"""Build annual and quarterly datasets: consumer sentiment vs retirement contributions.

Inputs (all on disk):
  sentiment/raw/tbmics.csv      U. Michigan Index of Consumer Sentiment, monthly (sca.isr.umich.edu/files/tbmics.csv)
  sentiment/raw/tbqics.csv      same, quarterly from 1960 (files/tbqics.csv)
  sentiment/raw/tbmiccice.csv   current-conditions (ICC) and expectations (ICE) components, monthly
  sentiment/raw/UNRATE.csv      BLS unemployment rate via FRED (control variable)
  sentiment/raw/nipa_q_extract.csv  BEA NipaDataQ.txt extract (B040RC, A034RC, A132RC, A072RC)
  contributions/... existing annual contribution series (see README there)

Outputs: sentiment/output/annual_panel.csv, quarterly_panel.csv
"""
import pandas as pd, numpy as np, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RW = os.path.dirname(BASE)
RAW = os.path.join(BASE, "raw")
OUT = os.path.join(BASE, "output")
C = os.path.join(RW, "contributions")

MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}

# ---------- sentiment ----------
m = pd.read_csv(os.path.join(RAW, "tbmics.csv"))
m["date"] = pd.to_datetime(dict(year=m.YYYY, month=m.Month.map(MONTHS), day=1))
m = m.set_index("date")["ICS_ALL"].astype(float)
cc = pd.read_csv(os.path.join(RAW, "tbmiccice.csv"))
cc["date"] = pd.to_datetime(dict(year=cc.YYYY, month=cc.Month.map(MONTHS), day=1))
cc = cc.set_index("date")[["ICC", "ICE"]].astype(float)
q = pd.read_csv(os.path.join(RAW, "tbqics.csv"))
qmap = {"Jan.-Mar.": 1, "Apr.-Jun.": 2, "Jul.-Sep.": 3, "Oct.-Dec.": 4}
q["period"] = q.YYYY.astype(str) + "Q" + q.QUARTER.map(qmap).astype(str)
q = q.set_index("period")["ICS_ALL"].astype(float)

# Monthly survey is continuous from Jan 1978. Before that the survey was quarterly
# (tbqics, 1960+). Annual average: monthly mean from 1978, quarterly mean 1960-1977.
mm = m[m.index >= "1978-01-01"]
ann_m = mm.groupby(mm.index.year).agg(["mean", "count"])
ann_m = ann_m[ann_m["count"] == 12]["mean"]
qq = q.copy(); qq.index = qq.index.str[:4].astype(int)
ann_q = qq.groupby(level=0).agg(["mean", "count"])
ann_q = ann_q[ann_q["count"] == 4]["mean"]
ics_ann = pd.concat([ann_q[ann_q.index < 1978], ann_m]).rename("ics")
ccm = cc[cc.index >= "1978-01-01"]
comp_ann = ccm.groupby(ccm.index.year).mean()
comp_ann = comp_ann[ccm.groupby(ccm.index.year).size() == 12]
comp_ann.columns = ["ics_current", "ics_expect"]

# Quarterly sentiment from monthly (1978+), quarterly survey before
mq = mm.groupby(mm.index.to_period("Q")).agg(["mean", "count"])
mq = mq[mq["count"] == 3]["mean"]; mq.index = mq.index.astype(str)
ics_q = pd.concat([q[q.index < "1978Q1"], mq]).rename("ics")

# ---------- unemployment control ----------
u = pd.read_csv(os.path.join(RAW, "UNRATE.csv"), parse_dates=["observation_date"]).set_index("observation_date")["UNRATE"]
u_ann = u.groupby(u.index.year).agg(["mean", "count"])
u_ann = u_ann[u_ann["count"] >= 10]["mean"].rename("unrate")  # 2025: Oct missing (federal shutdown)
u_q = u.groupby(u.index.to_period("Q")).agg(["mean", "count"]); u_q = u_q[u_q["count"] >= 2]["mean"]
u_q.index = u_q.index.astype(str); u_q = u_q.rename("unrate")

# ---------- annual contribution series (% of wages, % of people) ----------
bea = pd.read_csv(os.path.join(C, "admin/output/bea_nipa_pension_contrib.csv")).set_index("year")
dol = pd.read_csv(os.path.join(C, "admin/output/dol_dc_contrib_by_source.csv")).set_index("year")
e13 = pd.read_csv(os.path.join(C, "admin/output/dol_e13_contributions_by_type.csv")).set_index("year")
ira = pd.read_csv(os.path.join(C, "irs/output/ira_contributions_by_type.csv"))
ira = ira[ira.ira_type == "All IRA types"].set_index("year")
f1040 = pd.read_csv(os.path.join(C, "irs/output/f1040_ira_keogh_deduction_long.csv")).set_index("year")
w2 = pd.read_csv(os.path.join(C, "irs/output/w2_deferrals_totals.csv")).set_index("year")

ann = pd.DataFrame({
    "bea_dc_employee_pct_wages": bea["dc_household_contrib_all_sectors_pct_total_wages"],
    "bea_dc_employer_pct_priv_wages": bea["priv_dc_employer_pct_priv_wages"],
    "bea_all_employer_pension_pct_priv_wages": bea["priv_pension_employer_pct_priv_wages"],
    "f5500_dc_participant_pct_priv_wages": dol["dc_participant_pct_private_wages"],
    "f5500_dc_employer_pct_priv_wages": dol["dc_employer_pct_private_wages"],
    "f5500_dc_total_incl_rollovers_pct_priv_wages": e13["dc_contrib_pct_private_wages"],
    "irs_ira_contrib_pct_wages": ira["contrib_pct_f1040_wages"],
    "irs_pct_taxpayers_contrib_ira": ira["pct_all_taxpayers_contributing"],
    "f1040_pct_returns_ira_deduction": f1040["pct_returns_ira_ded"],
    "w2_deferrals_pct_wages": w2["deferrals_pct_all_box1_wages"],
    "w2_pct_earners_deferring": w2["pct_wage_earners_deferring"],
})
ann = ann.join(ics_ann, how="outer").join(comp_ann, how="outer").join(u_ann, how="outer")
ann.index.name = "year"
ann = ann[(ann.index >= 1960) & (ann.index <= 2025)]
ann.to_csv(os.path.join(OUT, "annual_panel.csv"), float_format="%.4f")

# ---------- quarterly NIPA ----------
nq = pd.read_csv(os.path.join(RAW, "nipa_q_extract.csv"), header=None, names=["code", "period", "value"])
nq["value"] = nq.value.astype(str).str.replace(",", "").astype(float)
nq = nq.pivot(index="period", columns="code", values="value")
qp = pd.DataFrame({
    "nipa_emp_pension_insurance_pct_wages": 100 * nq["B040RC"] / nq["A034RC"],
    "personal_saving_rate": nq["A072RC"],
}).join(ics_q, how="outer").join(u_q, how="outer")
qp.index.name = "quarter"
qp = qp[(qp.index >= "1960Q1")]
qp.to_csv(os.path.join(OUT, "quarterly_panel.csv"), float_format="%.4f")
print(ann.tail(8).T.to_string()); print(qp.tail(4).T)
