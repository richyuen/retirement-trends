"""Tabulate combined IRA/Keogh/401(k) withdrawal incidence and all-holder rates by age, SIPP 1996-2008 panels.

Holders: persons 15+ with IRA + Keogh + 401k/403b/thrift balance > 0 at the end of the 12-month
window (asset module), observed in all 12 core months. Withdrawer: any month with TPPNDIST > 0.
Incidence = withdrawers per 100 holders. All-holder rate = sum of 12-month withdrawals / sum of
end-of-window balances. SEs: Fay's BRR, variance = 4/R * sum (theta_r - theta)^2.
Writes ../output/sipp_hist_long.csv and ../output/sipp_hist_windows.csv.
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
D = pd.read_parquet(os.path.join(HERE, "..", "data", "sipp_hist_persons.parquet"))
OUT = os.path.join(HERE, "..", "output"); os.makedirs(OUT, exist_ok=True)

BANDS = [("55-59", 55, 59), ("60-64", 60, 64), ("65-69", 65, 69), ("70-74", 70, 74), ("75-79", 75, 79),
         ("80+", 80, 200), ("60+", 60, 200), ("60-69", 60, 69), ("70+", 70, 200), ("65+", 65, 200)]

D["bal"] = D[["TALRB", "TALKB", "TALTB"]].clip(lower=0).sum(axis=1)
D["full"] = D.months.eq(12)
# window label: the calendar year of the one December inside the 12-month window
D["dec_year"] = np.where((D.win_end % 12) == 11, D.win_end // 12, D.win_end // 12 - 1)
D["mid_year"] = (D.win_start + D.win_end) / 2 / 12

win = []
rows = []
for (panel, wave), g in D.groupby(["panel", "wave"]):
    hold = g[(g.bal > 0)]
    attr = 1 - hold.full.mean()
    h = hold[hold.full].copy()
    reps = pd.read_parquet(f"/tmp/sipph/reps_{panel}_w{wave}.parquet")
    rcols = [c for c in reps.columns if c.startswith("R")]
    h = h.merge(reps, on=["SSUID", "EPPPNUM"], how="left")
    miss = h[rcols[0]].isna().mean()
    h = h[h[rcols[0]].notna()]
    dy = h.dec_year.value_counts(normalize=True)
    label = int(dy.idxmax())
    win.append(dict(panel=panel, wave=wave, year=label, dec_year_share=round(dy.max(), 3),
                    win_first=f"{int(h.win_start.min()//12)}-{int(h.win_start.min()%12)+1:02d}",
                    win_last=f"{int(h.win_end.max()//12)}-{int(h.win_end.max()%12)+1:02d}",
                    mid_year=round(h.mid_year.mean(), 2), holders_dropped_incomplete_pct=round(100 * attr, 1),
                    holders_no_repwgt_pct=round(100 * miss, 2), n_holders=len(h)))
    W = h.WPFINWGT.to_numpy() / 1e4  # 4 implied decimals
    R = h[rcols].to_numpy() / 1e4
    wdr = (h.wd12 > 0).to_numpy(float)
    wd = h.wd12.to_numpy(float); bal = h.bal.to_numpy(float)
    nrep = len(rcols)
    for name, lo, hi in BANDS:
        m = ((h.TAGE >= lo) & (h.TAGE <= hi)).to_numpy()
        if m.sum() == 0:
            continue
        def stats(w):
            return (100 * (w[m] * wdr[m]).sum() / w[m].sum(), 100 * (w[m] * wd[m]).sum() / (w[m] * bal[m]).sum(),
                    w[m].sum() / 1e6)
        est = stats(W)
        rep = np.array([stats(R[:, r]) for r in range(nrep)])
        se = np.sqrt(4 / nrep * ((rep - np.array(est)) ** 2).sum(axis=0))
        for i, meas in enumerate(["incidence_per100", "rate_all_holders_pct", "holders_millions"]):
            rows.append(dict(panel=panel, wave=wave, year=label, age_band=name, measure=meas,
                             estimate=round(est[i], 3), se=round(se[i], 3), n=int(m.sum())))

pd.DataFrame(win).to_csv(os.path.join(OUT, "sipp_hist_windows.csv"), index=False)
L = pd.DataFrame(rows)
L.to_csv(os.path.join(OUT, "sipp_hist_long.csv"), index=False)
print(pd.DataFrame(win).to_string())
pd.set_option("display.width", 250)
for meas in ["incidence_per100", "rate_all_holders_pct"]:
    print(meas)
    print(L[L.measure == meas].pivot_table(index="age_band", columns="year", values="estimate").round(2).to_string())
    print(L[L.measure == meas].pivot_table(index="age_band", columns="year", values="se").round(2).to_string())
