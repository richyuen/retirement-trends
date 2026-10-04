"""Starter: weighted 60+ retirement-account tables from SCF summary extract and IPUMS-CPS ASEC.
Run in VS Code / Databricks. Variable names are from memory of the SCF summary extract; verify in the codebook."""
import pandas as pd, numpy as np
from pathlib import Path
RAW = Path(__file__).parent / "raw"

def wmean(x, w): return np.average(x, weights=w)
def wshare(mask, w): return (w[mask].sum() / w.sum()) if w.sum() else np.nan

# ---------- SCF 2022 summary extract (rscfp2022.dta) ----------
scf = pd.read_stata(RAW / "scf" / "rscfp2022.dta")
scf.columns = scf.columns.str.lower()
scf = scf[scf.age >= 60].copy()
scf["ira"]   = scf["irakh"]      # IRA/Keogh balance
scf["dc"]    = scf["thrift"]     # current-job DC (thrift) accounts
scf["has_ira"] = scf.ira > 0
scf["bandage"] = pd.cut(scf.age, [59, 64, 69, 74, 79, 120], labels=["60-64","65-69","70-74","75-79","80+"])
tab = (scf.groupby("bandage", observed=True)
         .apply(lambda g: pd.Series({
             "pct_hh_with_IRA": 100*wshare(g.has_ira.values, g.wgt.values),
             "median_IRA_if_any": np.nan if not g.has_ira.any() else
                 g.loc[g.has_ira].sort_values("ira").pipe(lambda d: d.ira[d.wgt.cumsum() >= d.wgt.sum()/2].iloc[0]),
             "hh_millions": g.wgt.sum()/1e6})))
print(tab.round(1))
# TODO: add full-SCF withdrawal items (regular withdrawals, reason, amount) from the codebook; merge on y1; compare with IRS SOI incidence in ../data/irs_derived.json

# ---------- IPUMS-CPS ASEC ----------
cps_path = next((RAW / "cps").glob("*.csv*"), None)
if cps_path:
    cps = pd.read_csv(cps_path)
    cps.columns = cps.columns.str.lower()
    cps = cps[cps.age >= 60]
    ret = "incretir"   # check codebook; handle NIU codes (99999999) and the 2014/2019 breaks
    cps["has_ret_inc"] = (cps[ret] > 0) & (cps[ret] < 99999990)
    out = (cps.assign(bandage=pd.cut(cps.age,[59,64,69,74,79,120],labels=["60-64","65-69","70-74","75-79","80+"]))
              .groupby(["year","bandage"], observed=True)
              .apply(lambda g: 100*wshare(g.has_ret_inc.values, g.asecwt.values)).unstack())
    print(out.round(1))
else:
    print("Place an IPUMS-CPS extract in microdata/raw/cps/")
