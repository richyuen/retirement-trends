"""One SIPP series, 1996-2024, for IRA + 401(k) accounts combined (person level, year-end holders 15+ with a combined
balance > 0), by age band. Same definitions in both eras:
  incidence_per100        withdrawers per 100 holders
  rate_all_holders_pct    sum of withdrawals in the year / sum of end-of-year balances (all holders)
  rate_below_p85_pct      the same, for holders below the 85th percentile of the combined balance among holders 60+
                          that year. Old-panel balances are topcoded (7-11% of holders 60+ have an account at the topcode,
                          holding about a third of reported balances), which inflates the full all-holder rate there;
                          every topcoded person is above the cut, so this variant is unaffected and comparable.
Old era (1996-2010): ../data/sipp_hist_persons.parquet (12-month window ending at the asset-module interview; year =
  the calendar year whose December falls inside the window). New era (2021-2024): ../../sipp/data/sipp_persons_dec.parquet
  (calendar year; 2020 is left out because SIPP 2021 asked only retired owners).
SEs: Fay BRR, 4/R * sum (theta_r - theta)^2 (R = 108 or 120 old panels, 240 new).
Writes ../output/sipp_combined_long.csv.
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "output")
BANDS = [("55-59", 55, 59), ("60-64", 60, 64), ("65-69", 65, 69), ("70-74", 70, 74), ("75-79", 75, 79),
         ("80+", 80, 200), ("60+", 60, 200), ("60-69", 60, 69), ("70+", 70, 200)]


def tab(era, year, age, w, R, wd, amt, bal, topc=None):
    """age, w, wd(0/1), amt, bal: arrays for holders; R: replicate weight matrix (n x R)."""
    cut = np.nan
    a60 = age >= 60
    o = np.argsort(bal[a60]); cw = np.cumsum(w[a60][o]) / w[a60].sum()
    cut = bal[a60][o][np.searchsorted(cw, 0.85)]
    below = bal < cut
    if topc is not None:
        assert not (topc & below).any(), (year, "topcoded case below the cut")
    rows = []
    nrep = R.shape[1]
    for name, lo, hi in BANDS:
        m = (age >= lo) & (age <= hi)
        mb = m & below
        def f(ww):
            return np.array([100 * (ww[m] * wd[m]).sum() / ww[m].sum(),
                             100 * (ww[m] * amt[m]).sum() / (ww[m] * bal[m]).sum(),
                             100 * (ww[mb] * amt[mb]).sum() / (ww[mb] * bal[mb]).sum()])
        est = f(w)
        rep = np.array([f(R[:, r]) for r in range(nrep)])
        se = np.sqrt(4 / nrep * ((rep - est) ** 2).sum(axis=0))
        for i, meas in enumerate(["incidence_per100", "rate_all_holders_pct", "rate_below_p85_pct"]):
            rows.append(dict(era=era, year=year, age_band=name, measure=meas, estimate=round(est[i], 3),
                             se=round(se[i], 3), n=int(m.sum()), p85_cut_usd=round(float(cut))))
    return rows


rows = []
# ---- old panels
D = pd.read_parquet(os.path.join(HERE, "..", "data", "sipp_hist_persons.parquet"))
D["bal"] = D[["TALRB", "TALKB", "TALTB"]].clip(lower=0).sum(axis=1)
D["dec_year"] = np.where((D.win_end % 12) == 11, D.win_end // 12, D.win_end // 12 - 1)
for (panel, wave), g in D.groupby(["panel", "wave"]):
    mx = g[["TALRB", "TALKB", "TALTB"]].max().to_numpy()
    h = g[(g.bal > 0) & g.months.eq(12)]
    reps = pd.read_parquet(f"/tmp/sipph/reps_{panel}_w{wave}.parquet")
    h = h.merge(reps, on=["SSUID", "EPPPNUM"], how="inner")
    rc = [c for c in reps.columns if c.startswith("R")]
    topc = (h[["TALRB", "TALKB", "TALTB"]].to_numpy() >= mx).any(axis=1)
    year = int(h.dec_year.mode()[0])
    rows += tab("1996-2008 panels", year, h.TAGE.to_numpy(), h.WPFINWGT.to_numpy() / 1e4, h[rc].to_numpy() / 1e4,
                (h.wd12 > 0).to_numpy(float), h.wd12.to_numpy(float), h.bal.to_numpy(float), topc)
    print("old", panel, wave, year, flush=True)

# ---- new files (same construction as sipp/scripts/tabulate.py: any = IRA/Keogh or 401k/403b/503b/TSP)
N = pd.read_parquet(os.path.join(HERE, "..", "..", "sipp", "data", "sipp_persons_dec.parquet"))
N = N[(N.ref_year >= 2021) & (N.WPFINWGT > 0) & (N.TAGE_EHC >= 15)].copy()
z = lambda c: N[c].fillna(0).clip(lower=0)
ira_own, dc_own = N.EOWN_IRAKEO.eq(1), N.EOWN_THR401.eq(1)
ira_bal, dc_bal = z("TIRAKEOVAL") * ira_own, z("TTHR401VAL") * dc_own
ira_wd, dc_wd = ira_own & N.EIRA_INC_YN.eq(1), dc_own & N.ETHR_INC_YN.eq(1)
N["bal"] = ira_bal + dc_bal
N["ye"] = (ira_own & (ira_bal > 0)) | (dc_own & (dc_bal > 0))
N["wd"] = (ira_wd | dc_wd).astype(float)
N["amt"] = np.where(ira_wd, z("TIRA_INC_AMT"), 0.0) + np.where(dc_wd, z("TTHR_INC_AMT"), 0.0)
for y, g in N[N.ye].groupby("ref_year"):
    rp = f"/tmp/sipp/reps/rw{y + 1}_dec.parquet"
    if not os.path.exists(rp):
        print("no replicate weights yet for", y); continue
    reps = pd.read_parquet(rp)
    h = g.merge(reps, on=["SSUID", "PNUM"], how="inner")
    rc = [f"REPWGT{i}" for i in range(1, 241)]
    rows += tab("2021-2025 files", int(y), h.TAGE_EHC.to_numpy(), h.WPFINWGT.to_numpy(), h[rc].to_numpy(float),
                h.wd.to_numpy(), h.amt.to_numpy(float), h.bal.to_numpy(float))
    print("new", y, len(g), len(h), flush=True)

L = pd.DataFrame(rows)
L.to_csv(os.path.join(OUT, "sipp_combined_long.csv"), index=False)
pd.set_option("display.width", 250)
for meas in ["incidence_per100", "rate_all_holders_pct", "rate_below_p85_pct"]:
    print(meas)
    print(L[L.measure == meas].pivot_table(index="age_band", columns="year", values="estimate").round(1).to_string())
print(L.groupby("year").p85_cut_usd.first().to_string())
