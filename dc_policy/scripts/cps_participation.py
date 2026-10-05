"""Employer retirement-plan offer and participation, CPS ASEC public-use files (www2.census.gov only; no IPUMS).

Usage:
  python3 cps_participation.py extract  [RAW_DIR]   # download, extract universe + replicate weights, cache, delete raw
  python3 cps_participation.py tabulate [RAW_DIR]   # national series + state auto-IRA check -> ../output/*.csv
  python3 cps_participation.py all      [RAW_DIR]   # both (default RAW_DIR=/tmp/cpspart/raw)
Needs pandas, pyarrow. Cache: RAW_DIR/../cache/{asec}_{file}.parquet (persons) and *_rep.parquet (161 weights).

Variables (verified in each year's data dictionary, techdocs/cpsmarYY.pdf; positions are 1-based start/width):
  PENPLAN  "Other than social security did the employer or union that ... worked for in 20.. have a pension or
           other type of retirement plan for any of the employees?" (universe WRK_CK=1; 1 yes 2 no)
           [the task brief called this PENATVTY; in the ASEC PENATVTY is country of birth]
  PENINCL  "Was ... included in that plan?" (universe PENPLAN=1)
  LJCW     class of worker, longest job last year (1 private, 2-4 government, 5-6 self-employed, 7 unpaid)
  NOEMP    employer size, all locations (1 <10; 2 10-24 [2001-2010] / 10-49 [2011+]; 3 25-99 / 50-99;
           4 100-499; 5 500-999; 6 1000+)
  WKSWORK  weeks worked last year; HRSWK usual hours per week last year; WSAL_VAL wage & salary earnings
  A_AGE, MARSUPWT (2 implied decimals), PH_SEQ/PPPOS (person keys), household H_SEQ/GESTFIPS
  ASEC 2001-2010 layout: PH_SEQ 2/5 PPPOS 7/2 A_AGE 15/2 MARSUPWT 66/8 WKSWORK 171/2 HRSWK 181/2 LJCW 189/1
                         NOEMP 226/1 WSAL_VAL 243/6 PENPLAN 482/1 PENINCL 483/1; household H_SEQ 2/5 GESTFIPS 42/2
  ASEC 2011-2018 layout (incl. both 2014 files): A_AGE 19/2 MARSUPWT 155/8 WKSWORK 258/2 HRSWK 268/2 LJCW 291/1
                         NOEMP 300/1 WSAL_VAL 364/7 PENPLAN 731/1 PENINCL 732/1 (keys and GESTFIPS unchanged)
  ASEC 2019-2026 + 2017 research + 2018 bridge: CSV (pppubYY.csv, hhpubYY.csv), same variable names.
Universe (headline): age 21-64, worked last year (WKSWORK>0), LJCW=1 (private wage and salary), income year=ASEC-1.
SE: Census replicate weights (CPS_ASEC_ASCII_REPWGT_YYYY, 2005+), Var = 4/160 * sum_r (theta_r - theta_0)^2.
    ASEC 2001-2004 have no public replicate file: SE = binomial SRS SE x sqrt(deff), deff = median ratio of
    replicate variance to SRS variance for the same group/measure in ASEC 2005-2010 (labelled se_method=gvf_deff).
"""
import gzip, io, sys, zipfile, urllib.request, os
from pathlib import Path
import numpy as np, pandas as pd

STAGE = sys.argv[1] if len(sys.argv) > 1 else "all"
RAW = Path(sys.argv[2] if len(sys.argv) > 2 else "/tmp/cpspart/raw")
CACHE = RAW.parent / "cache"
D = Path(__file__).resolve().parent.parent
B = "https://www2.census.gov/programs-surveys/cps/datasets"
X = "https://www2.census.gov/programs-surveys/demo/datasets/income-poverty/time-series/data-extracts"

# ---------------------------------------------------------------- sources
FW = {  # (asec_year, file): (data url, layout)
    (2001, "production"): (f"{B}/2001/march/chip2001pub.cps.gz", "A"),   # SCHIP-expanded sample (as 2002+)
    (2002, "production"): (f"{B}/2002/march/mar02supp.dat.gz", "A"),
    (2003, "production"): (f"{B}/2003/march/asec2003.pub.gz", "A"),
    (2004, "production"): (f"{B}/2004/march/asec2004.pub.gz", "A"),
    (2005, "production"): (f"{B}/2005/march/asec2005_pubuse.pub.gz", "A"),
    (2006, "production"): (f"{B}/2006/march/asec2006_pubuse.pub.gz", "A"),
    (2007, "production"): (f"{B}/2007/march/asec2007_pubuse_tax2.dat.gz", "A"),
    (2008, "production"): (f"{B}/2008/march/asec2008_pubuse.dat.gz", "A"),
    (2009, "production"): (f"{B}/2009/march/asec2009_pubuse.dat.gz", "A"),
    (2010, "production"): (f"{B}/2010/march/asec2010_pubuse.dat.gz", "A"),
    (2011, "production"): (f"{B}/2011/march/asec2011_pubuse.dat.gz", "B"),
    (2012, "production"): (f"{B}/2012/march/asec2012_pubuse.dat.gz", "B"),
    (2013, "production"): (f"{B}/2013/march/asec2013_pubuse.dat.gz", "B"),
    (2014, "traditional_5x8"): (f"{B}/2014/march/asec2014_pubuse_tax_fix_5x8_2017.dat.gz", "B"),
    (2014, "redesign_3x8"): (f"{B}/2014/march/asec2014_pubuse_3x8_rerun_v2.dat.gz", "B"),
    (2015, "production"): (f"{B}/2015/march/asec2015_pubuse.dat.gz", "B"),
    (2016, "production"): (f"{B}/2016/march/asec2016_pubuse_v3.dat.gz", "B"),
    (2017, "production"): (f"{B}/2017/march/asec2017_pubuse.dat.gz", "B"),
    (2018, "production"): (f"{B}/2018/march/asec2018_pubuse.dat.gz", "B"),
}
CSV = {  # (asec_year, file): (person csv/zip, household csv or None if in zip)
    (2017, "research_updated"): (f"{X}/2017/cps-asec-research-file/pppub17.csv", f"{X}/2017/cps-asec-research-file/hhpub17.csv"),
    (2018, "bridge_updated"): (f"{X}/2018/cps-asec-bridge-file/pppub18.csv", f"{X}/2018/cps-asec-bridge-file/hhpub18.csv"),
    **{(2000 + y, "production"): (f"{B}/{2000+y}/march/asecpub{y}csv.zip", None) for y in range(19, 27)},
}
REP = {(y, "production"): f"{B}/{y}/march/CPS_ASEC_ASCII_REPWGT_{y}.dat.gz" for y in range(2005, 2019) if y != 2014}
REP.update({(y, "production"): f"{B}/{y}/march/CPS_ASEC_ASCII_REPWGT_{y}.DAT.GZ" for y in range(2020, 2027)})
REP.update({
    (2019, "production"): f"{B}/2019/march/CPS_ASEC_ASCII_REPWGT_2019.dat.gz",
    (2014, "traditional_5x8"): f"{B}/2014/march/CPS_ASEC_ASCII_REPWGT_2014.dat.gz",
    (2014, "redesign_3x8"): f"{B}/2014/march/CPS_ASEC_ASCII_REPWGT_2014_3x8_run5.dat.gz",
    (2017, "research_updated"): f"{X}/2017/cps-asec-research-file/cps_asec_ascii_repwgt_2017_111618.dat",
    (2018, "bridge_updated"): f"{X}/2018/cps-asec-bridge-file/cps_asec_ascii_repwgt_2018_022619.dat",
})
LAYOUT = {
    "A": dict(ph_seq=(2, 5), pppos=(7, 2), age=(15, 2), wt=(66, 8), wkswork=(171, 2), hrswk=(181, 2), ljcw=(189, 1),
              noemp=(226, 1), wsal=(243, 6), penplan=(482, 1), penincl=(483, 1)),
    "B": dict(ph_seq=(2, 5), pppos=(7, 2), age=(19, 2), wt=(155, 8), wkswork=(258, 2), hrswk=(268, 2), ljcw=(291, 1),
              noemp=(300, 1), wsal=(364, 7), penplan=(731, 1), penincl=(732, 1)),
}
HH = dict(h_seq=(2, 5), gestfips=(42, 2))
CSVCOLS = {"PH_SEQ": "ph_seq", "PPPOS": "pppos", "A_AGE": "age", "MARSUPWT": "wt", "WKSWORK": "wkswork", "HRSWK": "hrswk",
           "LJCW": "ljcw", "NOEMP": "noemp", "WSAL_VAL": "wsal", "PENPLAN": "penplan", "PENINCL": "penincl"}

def keep(d):
    """Universe kept in the cache: age 21-64, worked last year, private wage & salary on longest job."""
    return d[(d.age.between(21, 64)) & (d.wkswork > 0) & (d.ljcw == 1)].copy()

def fetch(url):
    p = RAW / url.rsplit("/", 1)[1]
    if "data-extracts" in url: p = RAW / (url.split("/")[-3] + "_" + url.rsplit("/", 1)[1])
    if not p.exists():
        RAW.mkdir(parents=True, exist_ok=True); tmp = p.with_suffix(p.suffix + ".part")
        for attempt in range(4):   # large Census files occasionally arrive truncated
            try:
                urllib.request.urlretrieve(url, tmp); break
            except OSError as e:     # ContentTooShortError and URLError are OSError subclasses
                print("retry", url, e, flush=True)
                if attempt == 3: raise
        tmp.rename(p)
    return p

def read_fw(path, lay):
    pos = LAYOUT[lay]; a0 = pos["age"][0] - 1; prs, hhs = [], []
    with gzip.open(path, "rt", encoding="latin-1") as f:
        for line in f:
            t = line[0]
            if t == "1":
                hhs.append([int(line[s-1:s-1+n]) for s, n in HH.values()])
            elif t == "3":
                if not 21 <= int(line[a0:a0+2]) <= 64: continue
                prs.append([int(line[s-1:s-1+n]) for s, n in pos.values()])
    d = pd.DataFrame(prs, columns=list(pos)); d["wt"] = d.wt / 100
    h = pd.DataFrame(hhs, columns=list(HH))
    return d, h

def read_csv(purl, hurl):
    pp = fetch(purl)
    if pp.suffix == ".zip":
        z = zipfile.ZipFile(pp)
        pf = z.open(next(n for n in z.namelist() if "pppub" in n)); hf = z.open(next(n for n in z.namelist() if "hhpub" in n))
    else:
        pf = open(pp, "rb"); hf = open(fetch(hurl), "rb")
    d = pd.read_csv(pf, usecols=list(CSVCOLS)).rename(columns=CSVCOLS)
    h = pd.read_csv(hf, usecols=["H_SEQ", "GESTFIPS"]).rename(columns={"H_SEQ": "h_seq", "GESTFIPS": "gestfips"})
    if d.wt.sum() > 1e10: d["wt"] = d.wt / 100        # implied decimals kept in some CSVs
    return d, h, [pp] + ([] if hurl is None else [fetch(hurl)])

def read_rep(path, keys):
    """As cps/scripts/se.py: return ph_seq, pppos, w0..w160 for persons in keys."""
    raw = (gzip.open(path) if str(path).lower().endswith("gz") else open(path, "rb")).read()
    L = raw.index(b"\n"); L = L - 1 if raw[L-1:L] == b"\r" else L
    nb = 10 if L == 1617 else 9
    a = np.frombuffer(raw, dtype=np.uint8); del raw
    step = L + (2 if a[L] == 13 else 1)
    if len(a) % step: a = np.concatenate([a, np.full(step - len(a) % step, 10, np.uint8)])
    a = a.reshape(-1, step)
    dig = lambda blk: (blk.astype(np.int64) - 48) @ (10 ** np.arange(blk.shape[-1] - 1, -1, -1))
    k = pd.DataFrame({"ph_seq": dig(a[:, 161*nb:161*nb+5]), "pppos": dig(a[:, 161*nb+5:161*nb+7])})
    m = k.reset_index().merge(keys, on=["ph_seq", "pppos"])
    sub = a[m["index"].to_numpy(), :161*nb].reshape(len(m), 161, nb)
    if ((sub < 48) | (sub > 57)).any():
        w = sub.view(f"S{nb}").reshape(len(m), 161).astype(str).astype(float) / 1e4
    else:
        w = dig(sub) / 1e4
    return pd.concat([m[["ph_seq", "pppos"]], pd.DataFrame(w.astype(np.float32), columns=[f"w{i}" for i in range(161)])], axis=1)

def extract():
    CACHE.mkdir(parents=True, exist_ok=True)
    jobs = [(k, "fw") for k in FW] + [(k, "csv") for k in CSV]
    for (yr, f), kind in sorted(jobs):
        cp = CACHE / f"{yr}_{f}.parquet"; rp = CACHE / f"{yr}_{f}_rep.parquet"
        if not cp.exists():
            if kind == "fw":
                p = fetch(FW[(yr, f)][0]); d, h = read_fw(p, FW[(yr, f)][1]); used = [p]
            else:
                d, h, used = read_csv(*CSV[(yr, f)])
            allw = d.wt.sum()
            d = keep(d).merge(h, left_on="ph_seq", right_on="h_seq", how="left").drop(columns="h_seq")
            assert d.gestfips.notna().all(), (yr, f)
            d["asec_year"], d["file"] = yr, f
            d.to_parquet(cp, index=False)
            print(yr, f, "kept", len(d), "pop(m)", round(d.wt.sum() / 1e6, 2), "all persons read pop(m)", round(allw / 1e6, 1), flush=True)
            for p in used: p.unlink(missing_ok=True)   # save disk: raw files are re-downloadable
        if (yr, f) in REP and not rp.exists():
            d = pd.read_parquet(cp)
            p = fetch(REP[(yr, f)]); r = read_rep(p, d[["ph_seq", "pppos"]])
            m = d[["ph_seq", "pppos", "wt"]].merge(r, on=["ph_seq", "pppos"], how="left")
            assert m.w0.notna().all() and (m.w0 - m.wt).abs().max() < 0.011, (yr, f, m.w0.isna().sum())
            m.drop(columns="wt").to_parquet(rp, index=False); p.unlink(missing_ok=True)
            print(yr, f, "replicates matched", len(m), flush=True)

# ---------------------------------------------------------------- tabulation
def size_groups(d):
    yr = d.asec_year.iloc[0]
    out = {"emp_lt10": d.noemp == 1, "emp_lt100": d.noemp.between(1, 3), "emp_100plus": d.noemp >= 4,
           "emp_100_499": d.noemp == 4, "emp_500_999": d.noemp == 5, "emp_1000plus": d.noemp == 6}
    # cpsmar11 item 4: values 2/3 redefined as 10-49 / 50-99 from ASEC 2011; the 2019+ dictionaries still print
    # 10-24 / 25-99 but the 2019 questionnaire (Q4788) and the weighted shares confirm 10-49 / 50-99.
    lab = ("emp_10_49", "emp_50_99") if yr >= 2011 else ("emp_10_24", "emp_25_99")
    out[lab[0]] = d.noemp == 2; out[lab[1]] = d.noemp == 3
    return out

def groups(d):
    g = {"all_21_64": np.ones(len(d), bool), "age_21_34": d.age.between(21, 34), "age_35_64": d.age.between(35, 64),
         "fulltime_35h": d.hrswk >= 35, "parttime_lt35h": d.hrswk.between(1, 34),
         "fullyear_fulltime": (d.hrswk >= 35) & (d.wkswork >= 50)}
    g.update(size_groups(d))
    g["emp_lt100_age_21_34"] = d.noemp.between(1, 3) & d.age.between(21, 34)
    g["emp_100plus_age_21_34"] = (d.noemp >= 4) & d.age.between(21, 34)
    return {k: np.asarray(v, bool) for k, v in g.items()}

def measures(W, offer, part, mask):
    """W: n x k weights. Returns dict measure -> length-k vector of %."""
    Wm = W[mask]; o = offer[mask]; p = part[mask]
    tot = Wm.sum(0); wo = Wm[o].sum(0); wp = Wm[p].sum(0)
    with np.errstate(invalid="ignore", divide="ignore"):
        return {"offer": 100 * wo / tot, "participation": 100 * wp / tot, "takeup": 100 * wp / wo}

def tabulate():
    files = sorted(p for p in CACHE.glob("*.parquet") if not p.name.endswith("_rep.parquet"))
    rows = []; srs = []
    for cp in files:
        d = pd.read_parquet(cp); yr, f = int(d.asec_year.iloc[0]), d.file.iloc[0]
        rp = cp.with_name(cp.stem + "_rep.parquet")
        if rp.exists():
            r = pd.read_parquet(rp); d = d.merge(r, on=["ph_seq", "pppos"], how="left")
            W = d[[f"w{i}" for i in range(161)]].to_numpy(np.float64)
        else:
            W = d[["wt"]].to_numpy(np.float64)
        offer = (d.penplan == 1).to_numpy(); part = (d.penincl == 1).to_numpy()
        miss = (~d.penplan.isin([1, 2])).mean()
        for gname, mask in groups(d).items():
            if mask.sum() == 0: continue
            ms = measures(W, offer, part, mask)
            nn = {"offer": mask.sum(), "participation": mask.sum(), "takeup": (mask & offer).sum()}
            for m, v in ms.items():
                se = np.sqrt(4 / 160 * ((v[1:] - v[0]) ** 2).sum()) if W.shape[1] > 1 else np.nan
                pz = v[0] / 100; se_srs = 100 * np.sqrt(pz * (1 - pz) / nn[m])
                rows.append(dict(asec_year=yr, income_year=yr - 1, file=f, group=gname, measure=m, estimate_pct=v[0],
                                 se=se, n=int(nn[m]), se_srs=se_srs, se_method="replicate_sdr" if W.shape[1] > 1 else "",
                                 pop_m=W[mask, 0].sum() / 1e6, penplan_niu_share=miss))
        print(yr, f, "done", flush=True)
    t = pd.DataFrame(rows)
    # generalized SE for 2001-2004: design effect from 2005-2010 replicate SEs
    ref = t[t.asec_year.between(2005, 2010) & t.se.notna()]
    deff = (ref.se ** 2 / ref.se_srs ** 2).groupby([ref.group, ref.measure]).median().rename("deff")
    t = t.join(deff, on=["group", "measure"])
    fill = t.se.isna()
    t.loc[fill, "se"] = t.loc[fill, "se_srs"] * np.sqrt(t.loc[fill, "deff"]); t.loc[fill, "se_method"] = "gvf_deff_2005_2010"
    t = t.sort_values(["asec_year", "file", "group", "measure"])
    out = D / "output"; out.mkdir(parents=True, exist_ok=True)
    t[["asec_year", "income_year", "file", "group", "measure", "estimate_pct", "se", "n", "se_method", "pop_m", "deff"]].to_csv(
        out / "cps_plan_participation_by_year.csv", index=False, float_format="%.4f")
    breaks_and_ppa(t)
    state_check(files)

# ---------------------------------------------------------------- breaks and PPA window test
BREAK_GROUPS = ["all_21_64", "emp_lt100", "emp_100plus", "fulltime_35h", "parttime_lt35h", "age_21_34", "age_35_64"]

def paired_diff(yr, fa, fb):
    """Same-sample comparison (production vs research/bridge file): replicate-by-replicate difference."""
    out = []; ds = {}
    for f in (fa, fb):
        d = pd.read_parquet(CACHE / f"{yr}_{f}.parquet").merge(pd.read_parquet(CACHE / f"{yr}_{f}_rep.parquet"), on=["ph_seq", "pppos"])
        ds[f] = d
    for g in BREAK_GROUPS:
        v = {}
        for f, d in ds.items():
            W = d[[f"w{i}" for i in range(161)]].to_numpy(np.float64)
            v[f] = measures(W, (d.penplan == 1).to_numpy(), (d.penincl == 1).to_numpy(), groups(d)[g])
        for m in v[fa]:
            dv = v[fb][m] - v[fa][m]
            out.append(dict(comparison=f"{yr}: {fb} minus {fa} (same sample)", group=g, measure=m, est_a=v[fa][m][0],
                            est_b=v[fb][m][0], diff_pp=dv[0], se_diff=np.sqrt(4 / 160 * ((dv[1:] - dv[0]) ** 2).sum()),
                            se_method="paired replicate (same sample, same replicate index)"))
    return out

def breaks_and_ppa(t):
    k = t.set_index(["asec_year", "file", "group", "measure"])
    rows = []
    for g in BREAK_GROUPS:
        for m in ["offer", "participation", "takeup"]:
            a = k.loc[(2014, "traditional_5x8", g, m)]; b = k.loc[(2014, "redesign_3x8", g, m)]
            rows.append(dict(comparison="2014: redesign_3x8 minus traditional_5x8 (independent random subsamples)", group=g,
                             measure=m, est_a=a.estimate_pct, est_b=b.estimate_pct, diff_pp=b.estimate_pct - a.estimate_pct,
                             se_diff=np.hypot(a.se, b.se), se_method="independent: sqrt(se_a^2+se_b^2)"))
    rows += paired_diff(2017, "production", "research_updated") + paired_diff(2018, "production", "bridge_updated")
    # PPA window test: mean of yearly estimates; SE assumes independent years (conservative: rotation overlap is positive)
    win = {"pre_PPA_income_2002_2006": (2003, 2007), "post_PPA_income_2009_2012": (2010, 2013)}
    for g in BREAK_GROUPS:
        for m in ["offer", "participation", "takeup"]:
            x = t[(t.file == "production") & (t.group == g) & (t.measure == m)].set_index("asec_year")
            e = {}
            for w, (lo, hi) in win.items():
                s = x.loc[lo:hi]; e[w] = (s.estimate_pct.mean(), np.sqrt((s.se ** 2).sum()) / len(s))
            (a, sa), (b, sb) = e["pre_PPA_income_2002_2006"], e["post_PPA_income_2009_2012"]
            rows.append(dict(comparison="PPA window: mean ASEC 2010-2013 minus mean ASEC 2003-2007", group=g, measure=m,
                             est_a=a, est_b=b, diff_pp=b - a, se_diff=np.hypot(sa, sb), se_method="mean of yearly ests; years independent"))
    r = pd.DataFrame(rows); r["z"] = r.diff_pp / r.se_diff
    r.to_csv(D / "output" / "cps_participation_breaks_ppa.csv", index=False, float_format="%.4f")

# ---------------------------------------------------------------- state auto-IRA check
# First income year in which the state mandate plausibly covered a large share of small (<100) employers.
# Launch / deadline dates verified on state program sites (see notes file). 'wave' groups states by timing.
AUTOIRA = {  # fips: (state, first program deadline (yyyy-mm), first income year treated for <100 employers, wave)
    41: ("OR", "2017-11", 2019, "early"), 17: ("IL", "2018-11", 2020, "early"), 6: ("CA", "2020-06", 2021, "early"),
    9: ("CT", "2022-03", 2023, "mid"), 24: ("MD", "2022-09", 2023, "mid"), 8: ("CO", "2023-03", 2023, "mid"),
    51: ("VA", "2023-07", 2024, "mid"),
    23: ("ME", "2023 pilot, 2024 deadlines", 2025, "late"), 10: ("DE", "2024-07", 2025, "late"), 34: ("NJ", "2024-06", 2025, "late"),
    50: ("VT", "2024-12", 2025, "late"), 32: ("NV", "2025-05", 2026, "late"), 27: ("MN", "2026-01", 2027, "late"),
    44: ("RI", "2025-06", 2026, "late"), 36: ("NY", "2025-10", 2026, "late"), 15: ("HI", "not yet launched", 2099, "late"),
}
PERIODS = {"pre_2012_2016": (2012, 2016), "rollout_2017_2020": (2017, 2020), "post_2021_2025": (2021, 2025)}

def pick_file(files):
    """One file per ASEC year for pooled state work: production, except 2014 -> 3/8 redesign (matches 2015+ questions)."""
    sel = []
    for p in files:
        yr, f = p.stem.split("_", 1); yr = int(yr)
        if f == "production" and yr != 2014: sel.append(p)
        if yr == 2014 and f == "redesign_3x8": sel.append(p)
    return sel

def state_check(files):
    parts = []
    for cp in pick_file(files):
        d = pd.read_parquet(cp)
        d["income_year"] = d.asec_year - 1
        if not 2012 <= d.income_year.iloc[0] <= 2025: continue
        d = d[d.noemp.between(1, 3)]
        rp = cp.with_name(cp.stem + "_rep.parquet"); r = pd.read_parquet(rp)
        d = d.merge(r, on=["ph_seq", "pppos"], how="left"); parts.append(d)
    a = pd.concat(parts, ignore_index=True)
    a["wave"] = a.gestfips.map({k: v[3] for k, v in AUTOIRA.items()}).fillna("none")
    a["period"] = None
    for k, (lo, hi) in PERIODS.items(): a.loc[a.income_year.between(lo, hi), "period"] = k
    a["treated_now"] = a.gestfips.map({k: v[2] for k, v in AUTOIRA.items()}).le(a.income_year).fillna(False)
    wc = [f"w{i}" for i in range(161)]
    offer = (a.penplan == 1).to_numpy(); part = (a.penincl == 1).to_numpy()
    rows = []; est = {}
    W = a[wc].to_numpy(np.float64)
    # replicate weights pooled across years: average of yearly % (equal year weights) to avoid population-growth tilt
    for wave in ["early", "mid", "late", "none", "early_OR_IL_only", "CA_only"]:
        if wave == "early_OR_IL_only": wm = a.gestfips.isin([41, 17]).to_numpy()
        elif wave == "CA_only": wm = (a.gestfips == 6).to_numpy()
        else: wm = (a.wave == wave).to_numpy()
        for per in PERIODS:
            yrs = sorted(a.loc[a.period == per, "income_year"].unique()); vals = {m: [] for m in ["offer", "participation", "takeup"]}; n = 0
            for y in yrs:
                mask = wm & (a.income_year == y).to_numpy(); n += mask.sum()
                for m, v in measures(W, offer, part, mask).items(): vals[m].append(v)
            for m in vals:
                v = np.mean(vals[m], axis=0); est[(wave, per, m)] = v
                rows.append(dict(comparison="level", states=wave, period=per, income_years=f"{yrs[0]}-{yrs[-1]}", measure=m,
                                 estimate_pct=v[0], se=np.sqrt(4 / 160 * ((v[1:] - v[0]) ** 2).sum()), n=int(n)))
    for wave in ["early", "early_OR_IL_only", "CA_only", "mid"]:
        for per in ["rollout_2017_2020", "post_2021_2025"]:
            for m in ["offer", "participation", "takeup"]:
                ch_t = est[(wave, per, m)] - est[(wave, "pre_2012_2016", m)]
                ch_c = est[("none", per, m)] - est[("none", "pre_2012_2016", m)]
                for lab, v in [(f"change_{wave}", ch_t), ("change_none", ch_c), (f"did_{wave}_minus_none", ch_t - ch_c)]:
                    rows.append(dict(comparison=lab, states=wave, period=f"{per}_vs_pre", income_years="", measure=m,
                                     estimate_pct=v[0], se=np.sqrt(4 / 160 * ((v[1:] - v[0]) ** 2).sum()), n=np.nan))
    # event-style: yearly gap early-wave minus none, by income year
    for y in sorted(a.income_year.unique()):
        ym = (a.income_year == y).to_numpy()
        for wave in ["early", "mid"]:
            mt = measures(W, offer, part, ym & (a.wave == wave).to_numpy()); mc = measures(W, offer, part, ym & (a.wave == "none").to_numpy())
            for m in mt:
                v = mt[m] - mc[m]
                rows.append(dict(comparison=f"gap_{wave}_minus_none", states=wave, period=str(y), income_years=str(y), measure=m,
                                 estimate_pct=v[0], se=np.sqrt(4 / 160 * ((v[1:] - v[0]) ** 2).sum()),
                                 n=int((ym & (a.wave == wave).to_numpy()).sum())))
    pd.DataFrame(rows).to_csv(D / "output" / "cps_state_autoira_check.csv", index=False, float_format="%.4f")
    print("state check written")

if __name__ == "__main__":
    if STAGE in ("extract", "all"): extract()
    if STAGE in ("tabulate", "all"): tabulate()
