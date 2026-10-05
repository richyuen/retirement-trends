"""SCF 1989-2022: sources of income and composition of wealth for older households.

Unit: household (SCF "family"); age of the reference person at interview.
Groups: all households, 55-64, 65+, 65-74, 75+.
Income refers to the calendar year before the survey (SCF 2022 -> 2021), in 2022 dollars.

Inputs
  scf/raw/rscfpYYYY.dta        Fed summary extract (2022 dollars): WAGEINC, BUSSEFARMINC, INTDIVINC,
                               KGINC, SSRETINC, TRANSFOTHINC, PENACCTWD, balance-sheet variables
  scf/raw/pYYi6.dta, pYY_rw1   full public file + replicate weights, 2004-2022
  $SCF_OLD_DIR                 full public file + replicate weights, 1989-2001 (downloaded on first run
                               from federalreserve.gov/econres/files/: scf89s, scf92s, scf95s, scf98s,
                               scf01s and the matching *rw1s zips)

Splitting SSRETINC (codebook 2022 X5722; bulletin.macro.txt):
  SSRETINC = X5722 ("Social Security or other pensions, annuities, or other disability or retirement
  programs", prior year) + PENACCTWD (IRA and account-type pension withdrawals, 2004+ only).
  X5722 has no Social Security/pension split, so it is split per household in proportion to the
  *current* annualized amounts reported elsewhere in the interview:
    Social Security: X5306/X5307 (reference person), X5311/X5312 (spouse/partner)
    Pensions/annuities paying regular benefits: X5318/X5319, X5326/X5327, X5334/X5335, X5418/X5419,
      X5426/X5427, X5434/X5435 (grid #5-#6 through 2007), remaining plans X6804/X6805 (1998-2001)
      or X6958/X6959 (2004+). From 2001 the grid amounts exclude account-type plans (X6461=1);
      in 1989-1998 regular payments from account plans are in this grid too.
  Frequencies converted with the Fed's MCONV macro. If X5722 > 0 but both current amounts are 0,
  the amount is kept as "ss_pen_unallocated".
Account withdrawals (PENACCTWD) are a separate source from 2004. Before 2004 the SCF folded them
into X5724 (other income) or X5722, so for 1989-2001 they are inside "transfers/other" or
"pensions"; the 'comparable' definition (acctwd merged into other) is reported for all waves.

Estimates pool the 5 implicates (summary WGT is already divided by 5). SEs: 999 bootstrap replicate
weights (wt1bK x mmK) on implicate 1, plus (1 + 1/5) x between-implicate variance (same as
scf/scripts/scf_analysis.py).
Run: python3 spending/scf_income/scripts/scf_income_sources.py   (about 2-3 minutes)
"""
from pathlib import Path
import os, zipfile, urllib.request
import numpy as np, pandas as pd, pyreadstat

HERE = Path(__file__).resolve().parents[1]
PROJ = HERE.parents[1]
RAW = PROJ / "scf" / "raw"
OLD = Path(os.environ.get("SCF_OLD_DIR", "/tmp/scf_old"))
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

WAVES = [1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016, 2019, 2022]
OLD_FILES = {1989: ("scf89s", "scf89rw1s", "p89i6.dta", "p89_rw1.dta"),
             1992: ("scf92s", "scf92rw1s", "p92i4.dta", "p92_rw1.dta"),
             1995: ("scf95s", "scf95rw1s", "p95i6.dta", "p95_rw1.dta"),
             1998: ("scf98s", "scf98rw1s", "p98i6.dta", "p98_rw1.dta"),
             2001: ("scf01s", "scf2001rw1s", "p01i6.dta", "scf2001rw1s.dta")}

SUMV = ["y1", "yy1", "x1", "xx1", "wgt", "age", "income", "wageinc", "bussefarminc", "intdivinc", "kginc",
        "ssretinc", "transfothinc", "penacctwd", "networth", "asset", "fin", "nfin", "debt", "houses",
        "mrthel", "retqliq", "irakh", "thrift", "futpen", "currpen", "dbplant", "dbplancj", "dcplancj"]
SS = [("x5306", "x5307"), ("x5311", "x5312")]
PEN = [("x5318", "x5319"), ("x5326", "x5327"), ("x5334", "x5335"), ("x5418", "x5419"),
       ("x5426", "x5427"), ("x5434", "x5435"), ("x6804", "x6805"), ("x6958", "x6959")]
FULLV = ["x5702", "x5716", "x5718", "x5720", "x5722", "x5724"] + [v for p in SS + PEN for v in p]


def mconv(f):
    """Fed bulletin.macro.txt MCONV: frequency code -> multiplier to a monthly amount."""
    f = np.asarray(f)
    return ((f == 2) * 52 / 12 + (f == 3) * 26 / 12 + (f == 4) + (f == 5) / 3 + (f == 6) / 12 + (f == 11) / 6
            + (f == 12) / 2 + (f == 31) * 2 + (f == 23) * 13 / 12 + (f == 24) * 52 / 72)


def read(path, cols):
    _, meta = pyreadstat.read_dta(str(path), metadataonly=True)
    names = {c.lower(): c for c in meta.column_names}
    df, _ = pyreadstat.read_dta(str(path), usecols=[names[c] for c in cols if c in names])
    df.columns = df.columns.str.lower()
    return df


def old_path(year, k):
    """Full file (k=2) or replicate file (k=3) for 1989-2001; download from the Fed if missing."""
    zips = OLD_FILES[year]
    p = OLD / zips[k]
    if not p.exists():
        OLD.mkdir(parents=True, exist_ok=True)
        z = OLD / f"{zips[k - 2]}.zip"
        urllib.request.urlretrieve(f"https://www.federalreserve.gov/econres/files/{zips[k - 2]}.zip", z)
        zipfile.ZipFile(z).extractall(OLD)
        z.unlink()
    return p


def paths(year):
    if year >= 2004:
        yy = str(year)[2:]
        return RAW / f"p{yy}i6.dta", RAW / f"p{yy}_rw1.dta"
    return old_path(year, 2), old_path(year, 3)


def load(year):
    s = read(RAW / f"rscfp{year}.dta", SUMV)
    if "y1" not in s:
        s = s.rename(columns={"x1": "y1", "xx1": "yy1"})
    fpath, _ = paths(year)
    f = read(fpath, ["y1", "x1"] + FULLV)
    if "y1" not in f:
        f = f.rename(columns={"x1": "y1"})
    f = f.reindex(columns=["y1"] + FULLV).fillna(0)
    s = s.merge(f, on="y1", how="left", validate="1:1")
    for c in ["penacctwd", "dbplant", "dbplancj", "dcplancj"]:
        if c not in s:
            s[c] = 0.0
    s = s.fillna({"penacctwd": 0})
    s["imp"] = (s.y1 - s.yy1 * 10).astype(int)
    # 2022-dollar factor for full-file X variables (summary WAGEINC = X5702 x CPI factor)
    m = s.x5702 > 0
    cpi = float(np.median(s.wageinc[m] / s.x5702[m]))
    ss_cur = sum(np.clip(s[a], 0, None) * mconv(s[b]) * 12 for a, b in SS)
    pen_cur = sum(np.clip(s[a], 0, None) * mconv(s[b]) * 12 for a, b in PEN)
    base = s.ssretinc - s.penacctwd  # = X5722 in 2022 dollars
    tot = ss_cur + pen_cur
    sh = np.where(tot > 0, ss_cur / tot.where(tot > 0, 1), np.nan)
    s["inc_wage"] = s.wageinc
    s["inc_bus"] = s.bussefarminc
    s["inc_intdiv"] = s.intdivinc
    s["inc_kg"] = s.kginc
    s["inc_ss"] = np.where(tot > 0, base * sh, 0)
    s["inc_pen"] = np.where(tot > 0, base * (1 - sh), 0)
    s["inc_sspen_unalloc"] = np.where(tot > 0, 0, base)
    s["inc_acctwd"] = s.penacctwd
    tr = (s.x5716 + s.x5718 + s.x5720).clip(lower=0) * cpi
    s["inc_transfers"] = np.minimum(tr, s.transfothinc.clip(lower=0))  # UI/workers comp, child support/alimony, TANF/SNAP/SSI
    s["inc_other_raw"] = s.transfothinc - s.inc_transfers
    # A few hundred public-file records (mostly 1989-1995) carry an "other income" (X5724) far above the
    # household's own reported total (X5729), e.g. 1992 cases with $1.7M other income and $11k-57k total.
    # Headline: cap positive other income at the household's total income minus its other components.
    rest = s[["inc_wage", "inc_bus", "inc_intdiv", "inc_kg", "inc_ss", "inc_pen", "inc_sspen_unalloc",
              "inc_acctwd", "inc_transfers"]].sum(axis=1)
    s["inc_other"] = np.where(s.inc_other_raw > 0, np.minimum(s.inc_other_raw, np.maximum(s.income - rest, 0)),
                              s.inc_other_raw)
    s["cur_ss"] = ss_cur * cpi
    s["cur_pen"] = pen_cur * cpi
    s["year"] = year
    s["cpi"] = cpi
    return s


INC = ["inc_wage", "inc_bus", "inc_intdiv", "inc_kg", "inc_ss", "inc_pen", "inc_sspen_unalloc", "inc_acctwd",
       "inc_transfers", "inc_other"]


def design(d):
    """Per-household columns whose weighted totals define every statistic."""
    X = {"one": np.ones(len(d))}
    for c in INC:
        X[c] = d[c].values
        X["has_" + c] = (d[c].values > 0).astype(float)
    X["has_ss_or_pen_any"] = ((d.inc_ss + d.inc_pen + d.inc_sspen_unalloc) > 0).astype(float).values
    X["has_pen_or_acctwd"] = ((d.inc_pen + d.inc_acctwd) > 0).astype(float).values
    X["has_ss_cur"] = (d.cur_ss > 0).astype(float).values
    X["has_pen_cur"] = (d.cur_pen > 0).astype(float).values
    X["inc_other_raw"] = d.inc_other_raw.values
    X["inc_total"] = d[INC].sum(axis=1).values
    X["income_fed"] = d.income.values
    # SS reliance: share of household income (sum of components, floored at 0) from SS
    tot = np.maximum(d[INC].sum(axis=1).values, 0)
    ssh = np.where(tot > 0, d.inc_ss.values / np.where(tot > 0, tot, 1), 0)
    pos = tot > 0
    X["pos_income"] = pos.astype(float)
    safe = np.where(pos, tot, 1)
    hsrc = {"ss": d.inc_ss.values, "pen_plus_acctwd": (d.inc_pen + d.inc_acctwd).values,
            "wage": d.inc_wage.values,
            "capital": (d.inc_intdiv + d.inc_kg + d.inc_bus).values}
    for k, v in hsrc.items():  # each household's own share (clipped to 0-1), averaged over households
        X["hs_" + k] = np.where(pos, np.clip(v / safe, 0, 1), 0)
    X["ss_ge50"] = (ssh >= 0.5).astype(float)
    X["ss_ge90"] = (ssh >= 0.9).astype(float)
    # balance sheet
    pen = (d.thrift + d.futpen + d.currpen).values
    X["w_ret"] = d.retqliq.values
    X["w_homeeq"] = (d.houses - d.mrthel).values
    X["w_othfin"] = (d.fin - d.retqliq).values
    X["w_othnfin"] = (d.nfin - d.houses).values
    X["w_othdebt"] = -(d.debt - d.mrthel).values
    X["w_networth"] = d.networth.values
    X["w_asset"] = d.asset.values
    X["has_ret"] = (d.retqliq.values > 0).astype(float)
    X["has_ira"] = (d.irakh.values > 0).astype(float)
    X["has_dcacct"] = (pen > 0).astype(float)
    X["has_home"] = (d.houses.values > 0).astype(float)
    db_now = d.cur_pen.values > 0
    db_fut = d.dbplant.values == 1
    dbany = db_now | db_fut
    dc = d.retqliq.values > 0
    X["has_db_receiving"] = db_now.astype(float)
    X["has_db_future_or_cj"] = db_fut.astype(float)
    X["has_db_any"] = dbany.astype(float)
    X["db_only"] = (dbany & ~dc).astype(float)
    X["dc_only"] = (~dbany & dc).astype(float)
    X["db_and_dc"] = (dbany & dc).astype(float)
    X["neither"] = (~dbany & ~dc).astype(float)
    return pd.DataFrame(X)


def stats(T):
    """T: DataFrame of weighted totals (rows = weight vectors). Returns dict of statistic series."""
    out = {}
    den = T[INC].sum(axis=1)
    den_xkg = den - T.inc_kg
    for c in INC:
        k = c[4:]
        out[f"share_agg_{k}"] = 100 * T[c] / den
        if c != "inc_kg":
            out[f"share_agg_xkg_{k}"] = 100 * T[c] / den_xkg
        out[f"pct_with_{k}"] = 100 * T["has_" + c] / T.one
    out["share_agg_other_raw_uncapped"] = 100 * T.inc_other_raw / (den - T.inc_other + T.inc_other_raw)
    out["share_agg_ss_raw_uncapped_other"] = 100 * T.inc_ss / (den - T.inc_other + T.inc_other_raw)
    out["share_agg_ss_plus_pen_plus_unalloc"] = 100 * (T.inc_ss + T.inc_pen + T.inc_sspen_unalloc) / den
    out["share_agg_pen_plus_acctwd"] = 100 * (T.inc_pen + T.inc_acctwd) / den
    out["share_agg_xkg_pen_plus_acctwd"] = 100 * (T.inc_pen + T.inc_acctwd) / den_xkg
    out["share_agg_comparable_other_plus_acctwd"] = 100 * (T.inc_other + T.inc_transfers + T.inc_acctwd) / den
    out["pct_with_ss_or_pen_any"] = 100 * T.has_ss_or_pen_any / T.one
    out["pct_with_pen_or_acctwd"] = 100 * T.has_pen_or_acctwd / T.one
    out["pct_receiving_ss_now"] = 100 * T.has_ss_cur / T.one
    out["pct_receiving_pension_now"] = 100 * T.has_pen_cur / T.one
    out["pct_ss_ge50pct_of_income"] = 100 * T.ss_ge50 / T.one
    out["pct_ss_ge90pct_of_income"] = 100 * T.ss_ge90 / T.one
    for k in ["ss", "pen_plus_acctwd", "wage", "capital"]:
        out[f"mean_hh_share_{k}"] = 100 * T["hs_" + k] / T.pos_income
    out["mean_income_2022usd"] = T.inc_total / T.one
    nw = T.w_networth
    for c in ["w_ret", "w_homeeq", "w_othfin", "w_othnfin", "w_othdebt"]:
        out[f"pct_networth_{c[2:]}"] = 100 * T[c] / nw
    out["pct_assets_ret"] = 100 * T.w_ret / T.w_asset
    for c in ["has_ret", "has_ira", "has_dcacct", "has_home", "has_db_receiving", "has_db_future_or_cj",
              "has_db_any", "db_only", "dc_only", "db_and_dc", "neither"]:
        out[f"pct_{c}"] = 100 * T[c] / T.one
    out["mean_networth_2022usd"] = nw / T.one
    return out


def load_rw(year):
    _, rpath = paths(year)
    cols = ["y1", "x1"] + [f"wt1b{k}" for k in range(1, 1000)] + [f"mm{k}" for k in range(1, 1000)]
    r = read(rpath, cols)
    if "y1" not in r:
        r = r.rename(columns={"x1": "y1"})
    r = r.set_index("y1")
    W = np.column_stack([np.nan_to_num(r[f"wt1b{k}"].to_numpy(float) * r[f"mm{k}"].to_numpy(float))
                         for k in range(1, 1000)])
    return pd.DataFrame(W, index=r.index)


GROUPS = {"all": (0, 200), "55-64": (55, 64), "65+": (65, 200), "65-74": (65, 74), "75+": (75, 200)}


def run():
    rows = []
    for year in WAVES:
        df = load(year)
        rw = load_rw(year)
        print(year, "cpi factor", round(df.cpi.iloc[0], 3), flush=True)
        for g, (lo, hi) in GROUPS.items():
            d = df[(df.age >= lo) & (df.age <= hi)]
            X = design(d)
            point = stats(pd.DataFrame([d.wgt.values @ X.values], columns=X.columns))
            imps = [stats(pd.DataFrame([(gi.wgt.values * 5) @ design(gi).values], columns=X.columns))
                    for _, gi in d.groupby("imp")]
            d1 = d[d.imp == 1]
            W = rw.reindex(d1.y1.values).fillna(0).to_numpy()
            reps = stats(pd.DataFrame(W.T @ design(d1).values, columns=X.columns))
            n = int((d.imp == 1).sum())
            for k, v in point.items():
                est = float(np.asarray(v)[0])
                iv = np.var([float(np.asarray(i[k])[0]) for i in imps], ddof=1)
                rv = np.asarray(reps[k], float)
                rv = rv[np.isfinite(rv)]
                se = float(np.sqrt(np.var(rv, ddof=1) + 1.2 * iv)) if len(rv) > 1 else np.nan
                rows.append(dict(survey_year=year, income_year=year - 1, group=g, stat=k, estimate=est,
                                 se=se, n_cases=n))
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "scf_income_long.csv", index=False, float_format="%.4f")
    return res


if __name__ == "__main__":
    run()
