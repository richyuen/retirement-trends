"""Replicate and extend O. Divounguy, "Optimism or pressure? What the data says about why households are
saving less" (29 May 2026, orphedivounguy.com/savings-and-consumer-expectations/).

The article: monthly U. Michigan Index of Consumer Expectations (ICE) vs the BEA personal saving rate
(Table 2.6), Pearson correlation of LEVELS within six windows. Not split by income.

This script:
  1. Re-runs the six windows with the article-date vintage of the saving rate (ALFRED, 2026-05-29)
     and with the current vintage (FRED, downloaded 2026-10-27, after BEA's September 2026 annual update).
  2. Adds correlations of monthly and 12-month changes, which are less prone to spurious level correlation.
  3. Income cohorts (annual): Michigan ICE by income third vs
       a) BLS Consumer Expenditure Survey saving proxy by income quintile, 1984-2023:
          (income after taxes - total expenditures) / income after taxes
       b) SCF share of families whose spending was below income over the past year (SAVED), by income
          quartile, 12 waves 1992-2025 (SAVED is not in the 1989 summary extract).
Outputs: output/saving_expectations_windows.csv, saving_expectations_cohorts.csv,
         saving_expectations_cohort_panel_ce.csv, saving_expectations_cohort_panel_scf.csv
"""
import os, warnings
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RW = os.path.dirname(BASE)
RAW, OUT = os.path.join(BASE, "raw"), os.path.join(BASE, "output")
MONTHS = {m: i + 1 for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July",
                                          "August", "September", "October", "November", "December"])}


def pear(a, b):
    d = pd.concat([a, b], axis=1).dropna()
    if len(d) < 6: return np.nan, np.nan, len(d)
    r, p = stats.pearsonr(d.iloc[:, 0], d.iloc[:, 1]); return r, p, len(d)


# ---------- monthly series ----------
cc = pd.read_csv(os.path.join(RAW, "tbmiccice.csv"))
cc["date"] = pd.to_datetime(dict(year=cc.YYYY, month=cc.Month.map(MONTHS), day=1))
ice = cc.set_index("date")["ICE"].astype(float)
sv_now = pd.read_csv(os.path.join(RAW, "PSAVERT_vintage_2026-10-27.csv"), parse_dates=["observation_date"]).set_index("observation_date").iloc[:, 0]
sv_old = pd.read_csv(os.path.join(RAW, "PSAVERT_vintage_2026-05-29.csv"), parse_dates=["observation_date"]).set_index("observation_date").iloc[:, 0]

WINDOWS = [("Volcker era", "1981-01", "1985-12", -0.59), ("Tech boom", "1995-01", "2000-12", -0.55),
           ("Housing boom run-up", "2003-01", "2007-12", 0.48), ("GFC", "2006-01", "2010-12", -0.49),
           ("Pandemic + stimulus", "2019-01", "2021-12", -0.42), ("Today (article end)", "2023-01", "2026-04", 0.53),
           ("Today (extended)", "2023-01", "2026-08", np.nan), ("Full sample", "1978-01", "2026-08", np.nan)]
rows = []
for name, s, e, art in WINDOWS:
    rec = dict(window=name, start=s, end=e, article_r=art)
    for lab, sv in [("vintage_2026_05", sv_old), ("vintage_2026_10", sv_now)]:
        x, y = ice.loc[s:e], sv.loc[s:e]
        rec[f"r_levels_{lab}"], rec[f"p_levels_{lab}"], rec[f"n_{lab}"] = pear(x, y)
        rec[f"r_dmonth_{lab}"], rec[f"p_dmonth_{lab}"], _ = pear(ice.diff().loc[s:e], sv.diff().loc[s:e])
        rec[f"r_d12_{lab}"], rec[f"p_d12_{lab}"], _ = pear(ice.diff(12).loc[s:e], sv.diff(12).loc[s:e])
        rec[f"saving_rate_end_{lab}"] = sv.loc[:e].dropna().iloc[-1] if len(sv.loc[:e].dropna()) else np.nan
    rows.append(rec)
win = pd.DataFrame(rows)
win.to_csv(os.path.join(OUT, "saving_expectations_windows.csv"), index=False, float_format="%.3f")

# ---------- income cohorts ----------
ice_inc = {}
for g in ["bottom", "middle", "top"]:
    d = pd.read_excel(os.path.join(RAW, f"umich_components_income_{g}33.xls"), header=None).iloc[7:, [0, 1, 5]]
    d.columns = ["month", "year", "ice"]
    d = d.dropna(subset=["year", "ice"]); d["year"] = d.year.astype(int); d["ice"] = d.ice.astype(float)
    a = d.groupby("year").agg(ice=("ice", "mean"), m=("ice", "size")); ice_inc[g] = a[a.m == 12].ice
ice_inc = pd.DataFrame(ice_inc)
ice_inc["all"] = ice.groupby(ice.index.year).mean()

# a) CE saving proxy by quintile
ce = pd.read_csv(os.path.join(RAW, "bls_ce_income_quintiles_long.csv"))
ce["q"] = ce.series.str[-3:-1].astype(int) - 1          # LB0101M = all, 0102M = Q1 ... 0106M = Q5
ce["var"] = np.where(ce.series.str.contains("INCAFTTX"), "inc", "exp")
ce = ce.pivot_table(index=["year", "q"], columns="var", values="value").reset_index()
ce["saving_pct_aftertax_income"] = 100 * (ce.inc - ce.exp) / ce.inc
ce = ce.dropna(subset=["saving_pct_aftertax_income"])
qmap5 = {0: "all", 1: "bottom", 2: "bottom", 3: "middle", 4: "top", 5: "top"}
ce["sentiment_group"] = ce.q.map(qmap5)
ce["ice_group"] = [ice_inc.loc[y, g] if y in ice_inc.index else np.nan for y, g in zip(ce.year, ce.sentiment_group)]
ce.to_csv(os.path.join(OUT, "saving_expectations_cohort_panel_ce.csv"), index=False, float_format="%.3f")

# b) SCF SAVED by income quartile
scf_rows = []
for yr in [1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016, 2019, 2022, 2025]:
    f = os.path.join(RW, "scf/raw", f"rscfp{yr}.dta")
    if not os.path.exists(f): continue
    d = pd.read_stata(f, columns=["wgt", "income", "saved"])
    d.columns = [c.lower() for c in d.columns]
    d = d[["wgt", "income", "saved"]].dropna()
    # weighted income quartiles within the wave (all 5 implicates, weights already divided by 5)
    o = d.sort_values("income"); cw = o.wgt.cumsum() / o.wgt.sum()
    o["quartile"] = np.minimum(4, np.floor(cw * 4 - 1e-12).astype(int) + 1)
    for q, g in o.groupby("quartile"):
        scf_rows.append(dict(year=yr, quartile=q, pct_spending_below_income=100 * np.average(g.saved, weights=g.wgt)))
    scf_rows.append(dict(year=yr, quartile=0, pct_spending_below_income=100 * np.average(d.saved, weights=d.wgt)))
scf = pd.DataFrame(scf_rows)
qmap4 = {0: "all", 1: "bottom", 2: "middle", 3: "middle", 4: "top"}
scf["sentiment_group"] = scf.quartile.map(qmap4)
scf["ice_group"] = [ice_inc.loc[y, g] for y, g in zip(scf.year, scf.sentiment_group)]
scf.to_csv(os.path.join(OUT, "saving_expectations_cohort_panel_scf.csv"), index=False, float_format="%.3f")

res = []
for src, df, gcol, ycol in [("BLS CE", ce, "q", "saving_pct_aftertax_income"), ("SCF", scf, "quartile", "pct_spending_below_income")]:
    for g, gd in df.groupby(gcol):
        gd = gd.sort_values("year").set_index("year")
        consec = gd.index.to_series().diff()
        step = 1 if src == "BLS CE" else 3
        dy, dx = gd[ycol].diff(), gd.ice_group.diff()
        dy[consec != step] = np.nan
        r, p, n = pear(gd[ycol], gd.ice_group); res.append(dict(source=src, group=g, sentiment=gd.sentiment_group.iloc[0], kind="levels", r=r, p=p, n=n))
        r, p, n = pear(dy, dx); res.append(dict(source=src, group=g, sentiment=gd.sentiment_group.iloc[0], kind="changes", r=r, p=p, n=n))
    pan = df[df[gcol] != 0].sort_values([gcol, "year"]).copy()
    pan["dy"] = pan.groupby(gcol)[ycol].diff(); pan["dx"] = pan.groupby(gcol).ice_group.diff()
    pp = pan.dropna(subset=["dy", "dx"])
    fit = smf.ols("dy ~ dx + C(year)", data=pp).fit(cov_type="HC1")
    rng = np.random.default_rng(0); b0 = abs(fit.params["dx"]); hits = 0
    for _ in range(5000):
        qq = pp.copy(); qq["dx"] = qq.groupby("year").dx.transform(lambda v: rng.permutation(v.values))
        hits += abs(smf.ols("dy ~ dx + C(year)", data=qq).fit().params["dx"]) >= b0
    res.append(dict(source=src, group="pooled, year fixed effects", sentiment="own income group", kind="panel coef per 10 ICE pts",
                    r=10 * fit.params["dx"], p=fit.pvalues["dx"], n=int(fit.nobs), perm_p=hits / 5000))
coh = pd.DataFrame(res)
coh.to_csv(os.path.join(OUT, "saving_expectations_cohorts.csv"), index=False, float_format="%.3f")

pd.set_option("display.width", 250)
print(win[["window", "start", "end", "article_r", "r_levels_vintage_2026_05", "r_levels_vintage_2026_10", "n_vintage_2026_10",
           "r_dmonth_vintage_2026_10", "p_dmonth_vintage_2026_10", "r_d12_vintage_2026_10", "p_d12_vintage_2026_10",
           "saving_rate_end_vintage_2026_05", "saving_rate_end_vintage_2026_10"]].round(2).to_string())
print(coh.round(3).to_string())
print(ce[ce.year.isin([1984, 2000, 2008, 2023])].round(1).to_string())
print(scf.pivot(index="year", columns="quartile", values="pct_spending_below_income").round(1))
print(ice_inc.loc[[2019, 2022, 2025]].round(1))
