"""Income cohorts: Michigan sentiment by income tercile vs contributions by income group.

Sentiment: U. Michigan ICS for the bottom, middle and top third of family income
  (data.sca.isr.umich.edu demographic tables, Table 1a; monthly Dec 1979 - Sep 2026; raw/umich_ics_income_*.xls).
Contributions by income:
  1. IRS SOI W-2 elective deferrals by size of wages, 2008-2020, regrouped into approximate wage-earner terciles
     (the bin that straddles a tercile boundary is split pro rata by earners).
  2. SCF families contributing to a current-job DC plan, and employee DC contributions as % of wages,
     by family income quartile, 12 waves 1989-2022 (Q1 paired with bottom-third sentiment, Q2-Q3 with middle, Q4 with top).
  3. Saver's Credit returns as % of all returns, 2002-2023 (a low-income marker), paired with bottom-third sentiment.
Tests: correlation of year-to-year (or wave-to-wave) changes per group, and pooled panel regressions with
period fixed effects, which ask whether groups whose sentiment fell more also cut contributions more.
Outputs: output/cohort_panel_w2.csv, cohort_panel_scf.csv, cohort_sentiment_annual.csv, cohort_tests.csv
"""
import os, warnings
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RW = os.path.dirname(BASE)
RAW, OUT = os.path.join(BASE, "raw"), os.path.join(BASE, "output")
CDIR = os.path.join(RW, "contributions")
MONTHS = {m: i + 1 for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July",
                                          "August", "September", "October", "November", "December"])}

# ---- sentiment by income tercile, annual averages ----
sent = {}
for g in ["bottom", "middle", "top"]:
    d = pd.read_excel(os.path.join(RAW, f"umich_ics_income_{g}33.xls"), header=None).iloc[5:, :4]
    d.columns = ["month", "year", "ics", "cases"]
    d = d.dropna(subset=["year", "ics"])
    d["year"] = d.year.astype(int); d["ics"] = d.ics.astype(float)
    a = d.groupby("year").agg(ics=("ics", "mean"), months=("ics", "size"))
    sent[g] = a[a.months == 12].ics
sent = pd.DataFrame(sent)
sent["all"] = pd.read_csv(os.path.join(OUT, "annual_panel.csv"), index_col="year").ics
sent["gap_top_minus_bottom"] = sent.top - sent.bottom
sent.to_csv(os.path.join(OUT, "cohort_sentiment_annual.csv"), float_format="%.2f")


def lower_bound(label):
    s = label.replace("$", "").replace(",", "")
    return float(s.split(" ")[0])


# ---- 1. W-2 deferrals by approximate wage tercile ----
w = pd.read_csv(os.path.join(CDIR, "irs/output/w2_deferrals_by_wage_size.csv"))
w = w[w.wage_size != "All"].copy()
w["lb"] = w.wage_size.map(lower_bound)
rows = []
for yr, g in w.groupby("year"):
    g = g.sort_values("lb")
    tot = g.wage_earners.sum()
    cum0 = g.wage_earners.cumsum().shift(fill_value=0) / tot
    cum1 = g.wage_earners.cumsum() / tot
    for name, lo, hi in [("bottom", 0, 1 / 3), ("middle", 1 / 3, 2 / 3), ("top", 2 / 3, 1)]:
        share = ((np.minimum(cum1, hi) - np.maximum(cum0, lo)).clip(lower=0) / (cum1 - cum0))
        agg = {c: (g[c] * share).sum() for c in ["wage_earners", "wages_box1_k", "deferrers", "deferrals_k"]}
        rows.append(dict(year=yr, group=name, **agg,
                         pct_earners_deferring=100 * agg["deferrers"] / agg["wage_earners"],
                         deferrals_pct_wages=100 * agg["deferrals_k"] / agg["wages_box1_k"]))
w2 = pd.DataFrame(rows)
w2["ics_group"] = [sent.loc[y, g] for y, g in zip(w2.year, w2.group)]
w2.to_csv(os.path.join(OUT, "cohort_panel_w2.csv"), index=False, float_format="%.4f")

# ---- 2. SCF by income quartile ----
s = pd.read_csv(os.path.join(CDIR, "scf/output/scf_contrib_long.csv"))
s = s[s.group.str.match(r"^income quartile \d$")]
s = s[s.measure.isin(["pct_families_contributing_dc_current_job", "agg_dc_employee_pct_of_current_wages",
                      "pct_takeup_families_with_dc_plan"])]
scf = s.pivot_table(index=["year", "group"], columns="measure", values="estimate").reset_index()
scf["quartile"] = scf.group.str[-1].astype(int)
qmap = {1: "bottom", 2: "middle", 3: "middle", 4: "top"}
scf["tercile_for_sentiment"] = scf.quartile.map(qmap)
# SCF 1989 interviews ran mid-1989; sentiment-by-income starts 1980, so all waves are covered
scf["ics_group"] = [sent.loc[y, g] for y, g in zip(scf.year, scf.tercile_for_sentiment)]
scf["ics_all"] = scf.year.map(sent["all"])
scf.to_csv(os.path.join(OUT, "cohort_panel_scf.csv"), index=False, float_format="%.4f")

# ---- 3. Saver's Credit ----
sc = pd.read_csv(os.path.join(CDIR, "irs/output/f1040_savers_credit.csv")).set_index("year")["pct_returns"]


def corr(a, b):
    d = pd.concat([a, b], axis=1).dropna()
    if len(d) < 5: return np.nan, np.nan, len(d)
    r, p = stats.pearsonr(d.iloc[:, 0], d.iloc[:, 1]); return r, p, len(d)


tests = []


def add(source, measure, group, sentiment, r, p, n, kind, note=""):
    tests.append(dict(source=source, measure=measure, group=group, sentiment=sentiment, kind=kind,
                      r_or_coef=r, p=p, n=n, note=note))


# per-group change correlations, own-tercile sentiment and headline sentiment
for src, df, period, measures in [("IRS W-2", w2, "year", ["pct_earners_deferring", "deferrals_pct_wages"]),
                                  ("SCF", scf.rename(columns={"group": "g0"}).assign(group=lambda x: "Q" + x.quartile.astype(str)), "year",
                                   ["pct_families_contributing_dc_current_job", "agg_dc_employee_pct_of_current_wages"])]:
    for g, gd in df.groupby("group"):
        gd = gd.sort_values(period).set_index(period)
        for m in measures:
            dy = gd[m].diff()
            r, p, n = corr(dy, gd.ics_group.diff()); add(src, m, g, "own income group", r, p, n, "corr of changes")
            r, p, n = corr(dy, gd.index.to_series().map(sent["all"]).diff()); add(src, m, g, "all respondents", r, p, n, "corr of changes")
            r, p, n = corr(gd[m], gd.ics_group); add(src, m, g, "own income group", r, p, n, "corr of levels")
    # pooled panel in changes with period fixed effects: within a period, do groups with bigger sentiment drops cut more?
    pan = df.sort_values(["group", period]).copy()
    for m in measures:
        pan["dy"] = pan.groupby("group")[m].diff(); pan["dx"] = pan.groupby("group").ics_group.diff()
        pp = pan.dropna(subset=["dy", "dx"])
        fit = smf.ols("dy ~ dx + C(%s)" % period, data=pp).fit(cov_type="cluster", cov_kwds={"groups": pp["group"]}) \
            if pp.group.nunique() > 3 else smf.ols("dy ~ dx + C(%s)" % period, data=pp).fit(cov_type="HC1")
        add(src, m, "pooled, period fixed effects", "own income group", 10 * fit.params["dx"], fit.pvalues["dx"], int(fit.nobs),
            "panel coef per 10 pts", "change in measure per 10-point relative sentiment change")

# Saver's Credit vs bottom-third sentiment
r, p, n = corr(sc.diff(), sent.bottom.diff()); add("IRS Saver's Credit", "pct_returns_claiming", "low income", "bottom third", r, p, n, "corr of changes")
r, p, n = corr(sc.diff(), sent["all"].diff()); add("IRS Saver's Credit", "pct_returns_claiming", "low income", "all respondents", r, p, n, "corr of changes")

# aggregate series vs each tercile's sentiment (does the sentiment of the people holding most dollars fit better?)
ann = pd.read_csv(os.path.join(OUT, "annual_panel.csv"), index_col="year")
for col, s0, e0 in [("bea_dc_employee_pct_wages", 1984, 2025), ("bea_dc_employer_pct_priv_wages", 1984, 2025),
                    ("irs_pct_taxpayers_contrib_ira", 2000, 2021), ("f5500_dc_participant_pct_priv_wages", 1999, 2023)]:
    y = ann.loc[s0:e0, col]
    if col.startswith("irs_"):
        y = y.copy(); dyv = y.diff(); dyv[2004] = np.nan
    else:
        dyv = y.diff()
    for g in ["bottom", "middle", "top", "gap_top_minus_bottom"]:
        r, p, n = corr(dyv, sent.loc[s0:e0, g].diff()); add("aggregate", col, "all", g, r, p, n, "corr of changes")

t = pd.DataFrame(tests)
t.to_csv(os.path.join(OUT, "cohort_tests.csv"), index=False, float_format="%.4f")
pd.set_option("display.width", 220)
print(sent.loc[[1980, 1990, 2000, 2008, 2019, 2022, 2025]].round(1))
print(w2[w2.year.isin([2008, 2014, 2020])].round(2).to_string())
print(t.round(3).to_string())
