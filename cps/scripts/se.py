"""Replicate-weight standard errors, pandemic (entropy-balanced) weights and alternative population-control
weights for the CPS ASEC retirement-account withdrawal tables. Everything comes from www2.census.gov.

Usage: python se.py RAW_DIR   (downloads missing files into RAW_DIR; reads ../data/asec_persons_50plus.parquet,
       which must carry ph_seq/pppos from extract.py)
Outputs (../output/):
  asec_acct_wd_se_by_age.csv        long: estimate, SE and 90% CI of % with account withdrawals, withdrawer
                                    count and population, for every year/file/age band (MARSUPWT + its replicates)
  acct_withdrawal_se_by_age_wide.csv  SE (percentage points) of the headline % table, same layout as
                                    acct_withdrawal_pct_by_age_wide.csv
  asec_acct_wd_changes_se.csv       year-to-year differences with SEs (treated as independent samples: conservative)
  asec_alt_weights_by_age.csv       the same measures under (a) Census's entropy-balanced pandemic weights for
                                    ASEC 2019-2021, (b) the 2020-Census-based reweights of ASEC 2020-2021,
                                    (c) the September 2026 re-release of ASEC 2025 weights (vintage/ folder)

Replicate-weight files (CPS_ASEC_ASCII_REPWGT_YYYY): 161 weights PWWGT0-160 (PWWGT0 = MARSUPWT) then H_SEQ (5)
and PPPOS (2). Weights are 9 digits with 4 implied decimals (record length 1456); the 2014 3/8 file uses
10 digits (record length 1617). Variance (Census "Estimating ASEC Variances with Replicate Weights", successive
difference replication with Fay-type factors): Var = 4/160 * sum_r (theta_r - theta_0)^2.
"""
import gzip, sys, urllib.request
from pathlib import Path
import numpy as np, pandas as pd

RAW = Path(sys.argv[1] if len(sys.argv) > 1 else "raw")
D = Path(__file__).resolve().parent.parent
B = "https://www2.census.gov/programs-surveys/cps/datasets"
X = "https://www2.census.gov/programs-surveys/demo/datasets/income-poverty/time-series/data-extracts"

REP = {(y, "production"): f"{B}/{y}/march/CPS_ASEC_ASCII_REPWGT_{y}.dat.gz" for y in range(2010, 2019) if y != 2014}
REP.update({(y, "production"): f"{B}/{y}/march/CPS_ASEC_ASCII_REPWGT_{y}.DAT.GZ" for y in range(2020, 2027)})
REP.update({
    (2019, "production"): f"{B}/2019/march/CPS_ASEC_ASCII_REPWGT_2019.dat.gz",
    (2014, "traditional_5x8"): f"{B}/2014/march/CPS_ASEC_ASCII_REPWGT_2014.dat.gz",
    (2014, "redesign_3x8"): f"{B}/2014/march/CPS_ASEC_ASCII_REPWGT_2014_3x8_run5.dat.gz",
    (2017, "research_updated"): f"{X}/2017/cps-asec-research-file/cps_asec_ascii_repwgt_2017_111618.dat",
    (2018, "bridge_updated"): f"{X}/2018/cps-asec-bridge-file/cps_asec_ascii_repwgt_2018_022619.dat",
})
# alternative full-sample weights that come with their own replicates (PWWGT0 is the alternative weight)
ALT_REP = {
    (2020, "production", "2020_census_base"): f"{B}/2020/march/CPS_ASEC_ASCII_REPWGT_2020_2020BASE.gz",
    (2021, "production", "2020_census_base"): f"{B}/2021/march/CPS_ASEC_ASCII_REPWGT_2021_2020BASE.gz",
    (2025, "production", "rerelease_2026_09_vintage_dir"): f"{B}/2025/march/vintage/CPS_ASEC_ASCII_REPWGT_2025.DAT.GZ",
}
EBW = {y: f"{X}/2020/cps{y}_ebw_covidnonresp.csv" for y in (2019, 2020, 2021)}
BANDS = [(50,54),(55,59),(60,64),(65,69),(70,74),(75,79),(80,99),(60,99),(65,99),(73,99)]
Z90 = 1.645

def fetch(url, sub=""):
    p = RAW / sub / url.rsplit("/", 1)[1]
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True); urllib.request.urlretrieve(url, p)
    return p

def read_rep(path, keys):
    """Return DataFrame ph_seq, pppos, w0..w160 for the person keys in `keys` (DataFrame ph_seq, pppos)."""
    raw = (gzip.open(path) if str(path).lower().endswith("gz") else open(path, "rb")).read()
    L = raw.index(b"\n"); nb = 10 if L == 1617 else 9
    a = np.frombuffer(raw, dtype=np.uint8)
    if len(a) % (L + 1): a = np.concatenate([a, np.frombuffer(b"\n", np.uint8)])  # missing final newline
    a = a.reshape(-1, L + 1)
    dig = lambda blk: (blk.astype(np.int64) - 48) @ (10 ** np.arange(blk.shape[-1] - 1, -1, -1))
    k = pd.DataFrame({"ph_seq": dig(a[:, 161*nb:161*nb+5]), "pppos": dig(a[:, 161*nb+5:161*nb+7])})
    m = k.reset_index().merge(keys, on=["ph_seq", "pppos"])
    sub = a[m["index"].to_numpy(), :161*nb].reshape(len(m), 161, nb)
    if ((sub < 48) | (sub > 57)).any():   # signs/blanks: parse those cells as text
        txt = sub.view(f"S{nb}").reshape(len(m), 161).astype(str); w = txt.astype(float) / 1e4
    else:
        w = dig(sub) / 1e4
    return pd.concat([m[["ph_seq", "pppos"]], pd.DataFrame(w, columns=[f"w{i}" for i in range(161)])], axis=1)

def se_from(reps, full):
    return np.sqrt(4 / 160 * ((reps - full) ** 2).sum())

def band_stats(g, wcols, label):
    """g has acct_wd, age and weight columns wcols[0] (full) + wcols[1:] (160 replicates)."""
    rows = []
    for lo, hi in BANDS:
        b = g[g.age.between(lo, hi)]
        W = b[wcols].to_numpy(); y = b.acct_wd.to_numpy()
        pop = W.sum(0); wd = W[y].sum(0); pct = 100 * wd / pop
        r = dict(age=f"{lo}-{hi}" if hi < 99 else f"{lo}+", weight=label, n=len(b), n_wd=int(y.sum()),
                 pct_acct_wd=pct[0], se_pct_acct_wd=se_from(pct[1:], pct[0]) if W.shape[1] > 1 else np.nan,
                 acct_wd_m=wd[0] / 1e6, se_acct_wd_m=se_from(wd[1:], wd[0]) / 1e6 if W.shape[1] > 1 else np.nan,
                 pop_m=pop[0] / 1e6, se_pop_m=se_from(pop[1:], pop[0]) / 1e6 if W.shape[1] > 1 else np.nan)
        rows.append(r)
    return rows

def main():
    a = pd.read_parquet(D / "data" / "asec_persons_50plus.parquet")
    wc = [f"w{i}" for i in range(161)]
    out, alt, check = [], [], []
    for (yr, f), g in a.groupby(["asec_year", "file"]):
        g = g[["ph_seq", "pppos", "age", "wt", "acct_wd", "system"]].copy()
        if (yr, f) not in REP:
            print("no replicate file", yr, f); continue
        r = read_rep(fetch(REP[(yr, f)]), g[["ph_seq", "pppos"]])
        m = g.merge(r, on=["ph_seq", "pppos"], how="left")
        dif = (m.w0 - m.wt).abs()
        check.append(dict(asec_year=yr, file=f, persons=len(g), matched=int(m.w0.notna().sum()),
                          max_abs_wt_diff=float(dif.max())))
        for row in band_stats(m, wc, "marsupwt"):
            out.append(dict(asec_year=yr, income_year=yr - 1, file=f, system=g.system.iloc[0], **row))
        # alternative weights
        for (ay, af, lab), url in ALT_REP.items():
            if (ay, af) != (yr, f): continue
            ra = read_rep(fetch(url, sub=lab), g[["ph_seq", "pppos"]])
            ma = g.merge(ra, on=["ph_seq", "pppos"], how="left")
            assert ma.w0.notna().all(), (yr, lab)
            for row in band_stats(ma, wc, lab):
                alt.append(dict(asec_year=yr, income_year=yr - 1, file=f, **row))
        if f == "production" and yr in EBW:
            e = pd.read_csv(fetch(EBW[yr], sub="ebw")).rename(columns={"h_seq": "ph_seq"})
            me = m.merge(e, on=["ph_seq", "pppos"], how="left")
            assert me.ebw_pu_person.notna().all(), yr
            me["ebw_pu_person"] *= 1000   # file is in thousands (sums to the same 324-326M total as MARSUPWT)
            # approximate replicates: scale each replicate weight by the person's EBW/MARSUPWT ratio
            ratio = (me.ebw_pu_person / me.w0).to_numpy()[:, None]
            me[wc[1:]] = me[wc[1:]].to_numpy() * ratio; me["w0"] = me.ebw_pu_person
            for row in band_stats(me, wc, "entropy_balanced_ebw"):
                alt.append(dict(asec_year=yr, income_year=yr - 1, file=f, **row))
    ck = pd.DataFrame(check); print(ck.to_string())
    assert (ck.persons == ck.matched).all() and (ck.max_abs_wt_diff < 0.011).all(), "replicate merge failed"
    t = pd.DataFrame(out)
    t["ci90_lo"] = t.pct_acct_wd - Z90 * t.se_pct_acct_wd; t["ci90_hi"] = t.pct_acct_wd + Z90 * t.se_pct_acct_wd
    t["cv_acct_wd_m"] = t.se_acct_wd_m / t.acct_wd_m
    t.to_csv(D / "output" / "asec_acct_wd_se_by_age.csv", index=False, float_format="%.4f")
    # wide SE table matching acct_withdrawal_pct_by_age_wide.csv
    lab = {"production": "production", "traditional_5x8": "2014 traditional questions (5/8)",
           "redesign_3x8": "2014 redesigned questions (3/8)", "research_updated": "updated processing (research file)",
           "bridge_updated": "updated processing (bridge file)"}
    wide = t.assign(series=t.file.map(lab)).pivot_table(index=["asec_year", "income_year", "series"], columns="age",
                                                         values="se_pct_acct_wd")
    wide = wide[["55-59", "60-64", "65-69", "70-74", "75-79", "80+", "60+", "65+"]].reset_index()
    wide.columns.name = None
    wide.to_csv(D / "output" / "acct_withdrawal_se_by_age_wide.csv", index=False, float_format="%.2f")
    # differences (independent-sample SEs; CPS month-in-sample overlap makes true SEs somewhat smaller)
    p = t[t.file == "production"].set_index(["asec_year", "age"])
    pairs = [(y, y + 1) for y in range(2015, 2018)] + [(y, y + 1) for y in range(2019, 2026)] + \
            [(2020, y) for y in range(2022, 2027)] + [(2019, 2026)]
    dr = []
    for y0, y1 in pairs:
        for ag in p.loc[y0].index:
            a0, a1 = p.loc[(y0, ag)], p.loc[(y1, ag)]
            for v, s in [("pct_acct_wd", "se_pct_acct_wd"), ("acct_wd_m", "se_acct_wd_m")]:
                d = a1[v] - a0[v]; se = np.hypot(a1[s], a0[s])
                dr.append(dict(from_asec=y0, to_asec=y1, age=ag, measure=v, from_est=a0[v], to_est=a1[v],
                               diff=d, se_diff_indep=se, z=d / se, sig90=abs(d / se) > Z90))
    pd.DataFrame(dr).to_csv(D / "output" / "asec_acct_wd_changes_se.csv", index=False, float_format="%.4f")
    al = pd.DataFrame(alt)
    base = t.set_index(["asec_year", "file", "age"])[["pct_acct_wd", "acct_wd_m", "pop_m"]].add_prefix("marsupwt_")
    al = al.join(base, on=["asec_year", "file", "age"])
    al["diff_pct_vs_marsupwt"] = al.pct_acct_wd - al.marsupwt_pct_acct_wd
    al.to_csv(D / "output" / "asec_alt_weights_by_age.csv", index=False, float_format="%.4f")
    pd.set_option("display.width", 250)
    print(wide.round(2).to_string())
    print(al[al.age.isin(["65-69", "70-74", "75-79", "65+"])][["asec_year", "weight", "age", "pct_acct_wd",
          "marsupwt_pct_acct_wd", "se_pct_acct_wd", "acct_wd_m", "marsupwt_acct_wd_m", "pop_m", "marsupwt_pop_m"]].round(2).to_string())

if __name__ == "__main__":
    main()
