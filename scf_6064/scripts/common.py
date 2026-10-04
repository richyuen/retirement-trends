"""Shared loader and estimators for the SCF 60-64 withdrawal-decline analysis.

Reuses the definitions and SE method of scf/scripts/scf_analysis.py (imported read-only):
  RETQLIQ = IRAKH + THRIFT + FUTPEN + CURRPEN; PENACCTWD = IRA/Keogh + account-pension withdrawals (prior year)
  withdrawal flags wd_ira / wd_pen / wd_any from full_flags(); SEs = 999 bootstrap replicate weights
  (wt1b x mm) on implicate 1 + 1.2 x between-implicate variance.
Adds household characteristics from the summary extract (rscfpYYYY) and the full public file (pYYi6).
All dollars in 2022 dollars (summary-extract convention; IRA withdrawal items converted with the Fed's
CPILAG x CPIADJ as in scf/scripts/scf_rates.py).

The built analysis file is cached (parquet) outside the shared folder: $SCF6064_CACHE or
~/.cache/scf_6064 (delete it to rebuild).
"""
import os, sys
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
PROJ = HERE.parents[1]
sys.path.insert(0, str(PROJ / "scf" / "scripts"))
from scf_analysis import read, full_flags, load_rw, RAW, WD_WAVES  # noqa: E402

OUT = HERE.parent / "output"
OUT.mkdir(exist_ok=True)
CACHE = Path(os.environ.get("SCF6064_CACHE", Path.home() / ".cache" / "scf_6064"))
CACHE.mkdir(parents=True, exist_ok=True)

# same table as scf/scripts/scf_rates.py: (CPIADJ denominator, CPILAG) per wave, CPIBASE 2022 = 4376
CPI = {2004: (2785, 2770/2698), 2007: (3058, 3041/2957), 2010: (3204, 3198/3147), 2013: (3438, 3420/3369),
       2016: (3548, 3528/3483), 2019: (3775, 3758/3691), 2022: (4376, 4315/3992)}
BANDS = {"55-59": (55, 59), "60-64": (60, 64), "65-69": (65, 69)}

SUMV = ["y1", "yy1", "wgt", "age", "irakh", "thrift", "futpen", "currpen", "retqliq", "penacctwd", "lf", "occat1",
        "edcl", "married", "income", "norminc", "wageinc", "ssretinc", "dbplant", "dbplancj", "dcplancj",
        "networth", "hhsex", "racecl4", "kids"]
FULLV = ["y1", "x4100", "x4700", "x19", "x5301", "x5303", "x5304", "x5308", "x5309",
         "x6551", "x6559", "x6567", "x6552", "x6560", "x6568", "x6553", "x6561", "x6569",
         "x6554", "x6562", "x6570", "x6557", "x6565", "x6573"]


def _working(code):
    """Fed LF rule (bulletin.macro.txt): not working if X4100 in 50..80 or 97. For the spouse (X4700) also 0/199 = no spouse."""
    c = code.fillna(0)
    return ~(((c >= 50) & (c <= 80)) | (c == 97) | (c == 0) | (c == 199))


def build_year(year):
    s = read(RAW / f"rscfp{year}.dta", SUMV)
    s["imp"] = (s.y1 - s.yy1 * 10).astype(int)
    s = s[(s.age >= 55) & (s.age <= 69)].copy()
    f = full_flags(year)
    yy = str(year)[2:]
    x = read(RAW / f"p{yy}i6.dta", FULLV)
    s = s.merge(f, on="y1", how="left", validate="1:1").merge(x, on="y1", how="left", validate="1:1")
    s["year"] = year
    s["ref_year"] = year - 1
    den, lag = CPI[year]
    s["ira_wd"] = s.ira_amt_raw * lag * 4376 / den                          # IRA withdrawals, 2022$
    s["pen_wd"] = (s.penacctwd - s.ira_wd).clip(lower=0)                      # account-pension withdrawals, 2022$
    s["wd_any"] = s.wd_ira | s.wd_pen
    s["pen"] = s.thrift + s.futpen + s.currpen
    # IRA type balances (nominal survey-year $ in the full file; used only as shares of IRA balances)
    pos = lambda cols: s[cols].clip(lower=0).sum(axis=1)
    s["roth_nom"] = pos(["x6551", "x6559", "x6567"])
    s["rollover_nom"] = pos(["x6552", "x6560", "x6568"])
    s["ira_nom"] = pos(["x6551", "x6559", "x6567", "x6552", "x6560", "x6568", "x6553", "x6561", "x6569",
                        "x6554", "x6562", "x6570"])
    adj = np.where(s.ira_nom > 0, s.irakh / s.ira_nom.where(s.ira_nom > 0), 0)  # nominal -> 2022$ factor of the extract
    s["roth"] = s.roth_nom * adj
    s["rollover"] = s.rollover_nom * adj
    # work status (reference person / spouse-partner)
    s["r_work"] = s.lf == 1
    s["r_retired"] = s.x4100.isin([13, 50])           # retired (13 = worker + retired)
    s["marr"] = s.married == 1
    s["sp_work"] = s.marr & _working(s.x4700)
    s["any_work"] = s.r_work | s.sp_work
    s["no_work"] = ~s.any_work
    s["r_ss"] = s.x5303 == 1                          # R currently receives Social Security (any type)
    s["r_ss_ret"] = (s.x5303 == 1) & (s.x5304 == 1)   # ... retirement benefit
    s["hh_ss"] = s.x5301 == 1                         # R or spouse receives Social Security
    s["ba"] = s.edcl == 4
    s["db"] = s.dbplant == 1
    s["has_ira"] = s.irakh > 0
    s["has_thrift"] = s.thrift > 0                    # current-job DC account
    s["has_oldpen"] = (s.futpen + s.currpen) > 0      # DC from past jobs or now paying out
    s["holder"] = s.retqliq > 0
    s["acct_type"] = np.select([s.has_ira & ~(s.pen > 0), ~s.has_ira & (s.pen > 0), s.has_ira & (s.pen > 0)],
                               ["IRA only", "DC only", "IRA and DC"], "none")
    s["thrift_sh"] = np.where(s.holder, s.thrift / s.retqliq.where(s.holder), 0)
    return s


def load_all():
    p = CACHE / "scf_5569.parquet"
    if p.exists():
        return pd.read_parquet(p)
    df = pd.concat([build_year(y) for y in WD_WAVES], ignore_index=True)
    for c in df.columns:
        if df[c].dtype == object and c != "acct_type":
            df[c] = df[c].astype(float)
    df.to_parquet(p)
    return df


def band(df, b):
    lo, hi = BANDS[b]
    return df[(df.age >= lo) & (df.age <= hi)]


_RW = {}


def rw(year):
    if year not in _RW:
        p = CACHE / f"rw{year}.npy"
        pi = CACHE / f"rw{year}_y1.npy"
        if p.exists():
            _RW[year] = pd.DataFrame(np.load(p), index=np.load(pi))
        else:
            r = load_rw(year)
            np.save(p, r.to_numpy(np.float64)); np.save(pi, r.index.to_numpy())
            _RW[year] = pd.DataFrame(r.to_numpy(np.float64), index=r.index.to_numpy())
    return _RW[year]


def rep_matrix(d):
    """999 replicate weights for the implicate-1 rows of d (may span several waves)."""
    i1 = d[d.imp == 1]
    parts = [rw(y).reindex(g.y1.values).to_numpy() for y, g in i1.groupby("year", sort=False)]
    order = np.concatenate([g.index.values for _, g in i1.groupby("year", sort=False)])
    W = np.vstack(parts)
    return i1.loc[order], np.nan_to_num(W)


def estimate(d, fn, se=True):
    """fn(frame) -> f(weights) -> scalar or 1-d array. Pooled point estimate over implicates (WGT already /5)
    and SE = sqrt(replicate var on implicate 1 + 1.2 x between-implicate var) -- as scf_analysis.estimate."""
    point = np.asarray(fn(d)(d.wgt.values), float)
    if not se:
        return point, np.full_like(point, np.nan)
    imps = np.array([fn(g)(g.wgt.values * 5) for _, g in d.groupby("imp")], float)
    i1, W = rep_matrix(d)
    f1 = fn(i1)
    reps = np.array([f1(W[:, k]) for k in range(W.shape[1])], float)
    if reps.ndim == 1:
        reps = reps[:, None]; imps = imps[:, None]
    ok = np.isfinite(reps).all(axis=1)
    var = np.var(reps[ok], axis=0, ddof=1) + 1.2 * np.var(imps, axis=0, ddof=1)
    return point, np.sqrt(var).reshape(point.shape)


# ---- simple statistics (fn(d) -> f(w)) ----
def mean_of(expr, cond="holder"):
    def prep(d):
        m = d.eval(cond).values.astype(bool); x = d.eval(expr).values.astype(float)[m]
        return lambda w: 100 * (x * w[m]).sum() / w[m].sum()
    return prep


def ratio(num, den, cond="holder", scale=100):
    def prep(d):
        m = d.eval(cond).values.astype(bool); a = d[num].values[m]; b = d[den].values[m]
        return lambda w: scale * (a * w[m]).sum() / (b * w[m]).sum()
    return prep


def wmedian(x, w):
    o = np.argsort(x); x, w = x[o], w[o]; c = np.cumsum(w)
    return x[np.searchsorted(c, c[-1] / 2)] if len(x) else np.nan


def median_of(var, cond="holder"):
    def prep(d):
        m = d.eval(cond).values.astype(bool); x = d[var].values[m]
        return lambda w: wmedian(x, w[m])
    return prep


def popn(cond):
    def prep(d):
        m = d.eval(cond).values.astype(bool)
        return lambda w: w[m].sum() / 1e6
    return prep


# ---- vectorised statistics: f(w) accepts w of shape (n,) or (n, R) ----
def _vec(f):
    f.vec = True
    return f


def vshare(num, den="holder"):
    def prep(d):
        dm = d.eval(den).values.astype(float); nm = dm * d.eval(num).values.astype(float)
        return _vec(lambda w: 100 * (nm @ w) / (dm @ w))
    return prep


def vratio(num, den, cond="holder", scale=100):
    def prep(d):
        m = d.eval(cond).values.astype(float); a = d.eval(num).values.astype(float) * m
        b = d.eval(den).values.astype(float) * m
        return _vec(lambda w: scale * (a @ w) / (b @ w))
    return prep


def vmean(expr, cond="holder", scale=1.0):
    def prep(d):
        m = d.eval(cond).values.astype(float); x = d.eval(expr).values.astype(float) * m
        return _vec(lambda w: scale * (x @ w) / (m @ w))
    return prep


def vpop(cond="holder"):
    def prep(d):
        m = d.eval(cond).values.astype(float)
        return _vec(lambda w: (m @ w) / 1e6)
    return prep


def estimate_v(d, fn):
    """Like estimate() but evaluates all 999 replicates at once when the statistic is vectorised."""
    point = np.asarray(fn(d)(d.wgt.values), float)
    imps = np.array([fn(g)(g.wgt.values * 5) for _, g in d.groupby("imp")], float)
    i1, W = rep_matrix(d)
    f1 = fn(i1)
    if getattr(f1, "vec", False):
        reps = np.asarray(f1(W), float).T
    else:
        reps = np.array([f1(W[:, k]) for k in range(W.shape[1])], float)
    if reps.ndim == 1:
        reps = reps[:, None]; imps = imps.reshape(len(imps), -1)
    ok = np.isfinite(reps).all(axis=1)
    var = np.var(reps[ok], axis=0, ddof=1) + 1.2 * np.var(imps, axis=0, ddof=1)
    return point, np.sqrt(var).reshape(point.shape)


PERIODS = {"2003/06": [2004, 2007], "2018/21": [2019, 2022]}


def groups_by_wave(d):
    """(label, frame) per wave plus pooled early/late periods."""
    out = [(str(y - 1), g) for y, g in d.groupby("year")]
    out += [(k, d[d.year.isin(v)]) for k, v in PERIODS.items()]
    return out


BAL_BINS = [0, 25e3, 100e3, 250e3, 500e3, 1e6, np.inf]
INC_BINS = [-np.inf, 30e3, 60e3, 100e3, 200e3, np.inf]


def add_derived(d, bandname):
    d = d.copy()
    d["income_x"] = d.income - d.penacctwd                       # income net of the withdrawals it includes
    d["hh_rate"] = np.where(d.holder, np.minimum(d.penacctwd / d.retqliq.where(d.holder), 1.0), 0) * 100
    d["wd5"] = d.hh_rate >= 5                                    # withdrew >= 5% of balance
    d["wd10"] = d.hh_rate >= 10                                  # withdrew >= 10% of balance
    d["female"] = d.hhsex == 2
    d["has_roth"] = d.roth > 0
    d["ira_only"] = d.acct_type == "IRA only"
    d["dc_only"] = d.acct_type == "DC only"
    d["ira_dc"] = d.acct_type == "IRA and DC"
    d["bal_bin"] = pd.cut(d.retqliq, BAL_BINS, right=False, labels=False)
    d["inc_bin"] = pd.cut(d.income_x, INC_BINS, right=False, labels=False)
    d["tsh_bin"] = np.select([d.thrift_sh <= 0, d.thrift_sh <= .5], [0, 1], 2)
    # top-3 withdrawing households (weighted withdrawal dollars, all implicates) per wave within this band
    d["top3"] = False
    h = d[d.holder & (d.penacctwd > 0)]
    s = (h.penacctwd * h.wgt).groupby([h.year, h.yy1]).sum()
    top = s.groupby(level=0, group_keys=False).nlargest(3).index
    d.loc[pd.MultiIndex.from_arrays([d.year, d.yy1]).isin(top), "top3"] = True
    d["band"] = bandname
    return d
