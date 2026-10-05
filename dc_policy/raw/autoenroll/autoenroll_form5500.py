"""Share of private DC / 401(k) plans reporting automatic enrollment (Form 5500 pension feature code 2S),
by filing (plan) year and by plan effective year. Source: DOL EBSA Form 5500 'Latest' datasets
https://www.askebsa.dol.gov/FOIA%20Files/<YEAR>/Latest/F_5500_<YEAR>_Latest.zip and F_5500_SF_<YEAR>_Latest.zip
Usage: python3 autoenroll_form5500.py <dir with unzipped csvs> <out csv>
Notes: dedupe by EIN+PN keeping latest DATE_RECEIVED; DC = any pension code starting with '2';
401k = code 2J; AE = code 2S; participants = participants with account balances (EOY).
"""
import sys, pandas as pd, numpy as np
d, out = sys.argv[1], sys.argv[2]
YEARS = [2010, 2015, 2019, 2023, 2024, 2025]
rows = []
for y in YEARS:
    m = pd.read_csv(f"{d}/f_5500_{y}_latest.csv", dtype=str, low_memory=False,
                    usecols=["SPONS_DFE_EIN","SPONS_DFE_PN","PLAN_EFF_DATE","TYPE_PENSION_BNFT_CODE","PARTCP_ACCOUNT_BAL_CNT","TOT_ACTIVE_PARTCP_CNT","DATE_RECEIVED","TYPE_PLAN_ENTITY_CD"])
    m = m[m.TYPE_PLAN_ENTITY_CD.isin(["1","2","3"])]
    m = m.rename(columns={"SPONS_DFE_EIN":"ein","SPONS_DFE_PN":"pn","PLAN_EFF_DATE":"eff","TYPE_PENSION_BNFT_CODE":"codes","PARTCP_ACCOUNT_BAL_CNT":"acct","TOT_ACTIVE_PARTCP_CNT":"active","DATE_RECEIVED":"rcv"})
    m["form"] = "5500"
    s = pd.read_csv(f"{d}/f_5500_sf_{y}_latest.csv", dtype=str, low_memory=False,
                    usecols=lambda c: c in ["SF_SPONS_EIN","SF_PLAN_NUM","SF_PLAN_EFF_DATE","SF_TYPE_PENSION_BNFT_CODE","SF_PARTCP_ACCOUNT_BAL_CNT","SF_TOT_ACT_PARTCP_EOY_CNT","DATE_RECEIVED"])
    s = s.rename(columns={"SF_SPONS_EIN":"ein","SF_PLAN_NUM":"pn","SF_PLAN_EFF_DATE":"eff","SF_TYPE_PENSION_BNFT_CODE":"codes","SF_PARTCP_ACCOUNT_BAL_CNT":"acct","SF_TOT_ACT_PARTCP_EOY_CNT":"active","DATE_RECEIVED":"rcv"})
    s["form"] = "SF"
    a = pd.concat([m, s], ignore_index=True)
    a["codes"] = a.codes.fillna("").str.upper()
    a = a[a.codes.str.contains(r"(?:^|[^0-9])2[A-Z]", regex=True) | a.codes.str.startswith("2")]
    a = a.sort_values("rcv").drop_duplicates(["ein","pn"], keep="last")
    a["acct"] = pd.to_numeric(a.acct, errors="coerce").fillna(0)
    a["k401"] = a.codes.str.contains("2J")
    a["ae"] = a.codes.str.contains("2S")
    a["effyr"] = pd.to_datetime(a.eff, errors="coerce").dt.year
    def add(label, sub):
        n = len(sub); p = sub.acct.sum()
        rows.append(dict(filing_year=y, group=label, n_plans=n,
                         pct_plans_AE=round(100*sub.ae.mean(),1) if n else np.nan,
                         participants_acct=int(p),
                         pct_participants_in_AE_plans=round(100*sub.loc[sub.ae,"acct"].sum()/p,1) if p else np.nan))
    add("all DC plans", a)
    k = a[a.k401]
    add("401(k) plans", k)
    add("401(k) plans, 11+ acct-bal participants", k[k.acct > 10])
    add("401(k) plans, <100 acct-bal participants", k[k.acct < 100])
    add("401(k) plans, 100+ acct-bal participants", k[k.acct >= 100])
    for lo, hi, lab in [(0, y-4, f"eff<= {y-4}"), (y-3, y-2, f"eff {y-3}-{y-2}"), (y-1, y, f"eff {y-1}-{y}")]:
        g = k[(k.effyr >= lo) & (k.effyr <= hi)]
        add(f"401(k) plans {lab}", g)
        add(f"401(k) plans {lab}, 11+ acct-bal participants", g[g.acct > 10])
    for ey in range(y-3, y+1):
        g = k[(k.effyr == ey)]
        add(f"401(k) plans eff {ey}", g)
        add(f"401(k) plans eff {ey}, 11+ acct-bal participants", g[g.acct > 10])
    print(y, "done", flush=True)
r = pd.DataFrame(rows); r.to_csv(out, index=False); print(r.to_string())
