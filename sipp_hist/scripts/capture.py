"""SIPP aggregate IRA and 401(k)-type balances (all ages, weighted) against ICI's US retirement market totals
(Table 1: IRAs; DC plans), to see how completely each SIPP era measures balances.
ICI: irs/raw/ici/ret_26_q2_data.xls (The US Retirement Market, Second Quarter 2026), Table 1, year-end (Q4) values.
Writes ../output/sipp_balance_capture_vs_ici.csv.
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
t = pd.read_excel(os.path.join(ROOT, "irs/raw/ici/ret_26_q2_data.xls"), sheet_name="Table 1", header=None)
t = t.iloc[5:, [0, 1, 3]].dropna(subset=[1]); t.columns = ["period", "ira", "dc"]
t["period"] = t.period.astype(str).str.strip()
ye = {}
for _, r in t.iterrows():
    p = r.period
    if p.isdigit(): ye[int(p)] = (float(r.ira), float(r.dc))
    elif p.endswith(":Q4"): ye[int(p[:4])] = (float(r.ira), float(r.dc))
rows = []
D = pd.read_parquet(os.path.join(HERE, "..", "data", "sipp_hist_persons.parquet"))
for (p, w), g in D.groupby(["panel", "wave"]):
    W = g.WPFINWGT / 1e4
    endyr = int(np.median(g.win_end.dropna()) // 12)
    ira = (W * (g.TALRB + g.TALKB).clip(lower=0)).sum() / 1e9; dc = (W * g.TALTB.clip(lower=0)).sum() / 1e9
    rows.append(dict(source=f"SIPP {p} panel wave {w}", balance_year=endyr, sipp_ira_bn=round(ira), sipp_dc_bn=round(dc),
                     ici_ira_bn=ye[endyr][0], ici_dc_bn=ye[endyr][1]))
N = pd.read_parquet(os.path.join(ROOT, "sipp", "data", "sipp_persons_dec.parquet"))
for y, g in N[N.ref_year >= 2017].groupby("ref_year"):
    W = g.WPFINWGT
    ira = (W * g.TIRAKEOVAL.fillna(0).clip(lower=0) * g.EOWN_IRAKEO.eq(1)).sum() / 1e9
    dc = (W * g.TTHR401VAL.fillna(0).clip(lower=0) * g.EOWN_THR401.eq(1)).sum() / 1e9
    rows.append(dict(source=f"SIPP {y + 1}", balance_year=int(y), sipp_ira_bn=round(ira), sipp_dc_bn=round(dc),
                     ici_ira_bn=ye[int(y)][0], ici_dc_bn=ye[int(y)][1]))
R = pd.DataFrame(rows)
R["ira_capture_pct"] = (100 * R.sipp_ira_bn / R.ici_ira_bn).round(0)
R["dc_capture_pct"] = (100 * R.sipp_dc_bn / R.ici_dc_bn).round(0)
R.to_csv(os.path.join(HERE, "..", "output", "sipp_balance_capture_vs_ici.csv"), index=False)
print(R.to_string())
