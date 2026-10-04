"""Weighted tables of retirement-income receipt by age from asec_persons_50plus.parquet.
Output: ../output/asec_retirement_income_by_age.csv (long) and a printed wide summary."""
from pathlib import Path
import numpy as np, pandas as pd
D = Path(__file__).resolve().parent.parent
a = pd.read_parquet(D / "data" / "asec_persons_50plus.parquet")
BANDS = [(50,54),(55,59),(60,64),(65,69),(70,74),(75,79),(80,99),(60,99),(65,99),(73,99)]
def wmedian(x, w):
    o = np.argsort(x); x, w = np.asarray(x)[o], np.asarray(w)[o]; c = np.cumsum(w)
    return float(x[np.searchsorted(c, c[-1] / 2)]) if len(x) else np.nan
rows = []
for (yr, f, sysm), g in a.groupby(["asec_year", "file", "system"]):
    for lo, hi in BANDS:
        b = g[g.age.between(lo, hi)]; w = b.wt
        r = dict(asec_year=yr, income_year=yr - 1, file=f, system=sysm,
                 age=f"{lo}-{hi}" if hi < 99 else f"{lo}+", n=len(b), pop_m=w.sum() / 1e6)
        for v in ["any_ret", "acct_wd", "db_pension", "annuity", "ss_recip"]:
            r[f"pct_{v}"] = 100 * w[b[v]].sum() / w.sum()
        r["acct_wd_m"] = w[b.acct_wd].sum() / 1e6
        rc = b[b.acct_wd & (b.acct_wd_val > 0)]
        r["acct_wd_median_amt"] = wmedian(rc.acct_wd_val, rc.wt)
        r["acct_wd_total_bn"] = (b.acct_wd_val * w).sum() / 1e9
        rows.append(r)
t = pd.DataFrame(rows)
t.to_csv(D / "output" / "asec_retirement_income_by_age.csv", index=False, float_format="%.2f")
if __name__ == "__main__":
    pd.set_option("display.width", 250)
    for v in ["pct_acct_wd", "pct_any_ret", "pct_db_pension"]:
        print("\n", v); print(t.pivot_table(index=["asec_year", "file"], columns="age", values=v).round(1))
