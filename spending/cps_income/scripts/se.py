"""Replicate-weight standard errors for the income-source tables (Census successive-difference replication,
Var = 4/160 * sum_r (theta_r - theta_0)^2, 160 replicates; same formula and files as ../../../cps/scripts/se.py).

Usage: python se.py REP_DIR     (downloads missing replicate files into REP_DIR; reads ../data/... from extract.py)
Outputs (../output/):
  se_income_sources.csv   year x file x unit x age band x measure: estimate, se, 90% CI   (selected years below)
  se_changes.csv          differences between years / files with SEs, z and 90% significance flag.
                          Breaks measured within one ASEC year: 2014 traditional (5/8) vs redesigned (3/8)
                          (independent random subsamples) and 2017 / 2018 production (legacy) vs research / bridge
                          (updated processing): same persons, so the SE uses paired replicates when both files carry
                          identical replicate weights (checked), else treated as independent.
                          Changes over time treat years as independent (conservative: about half the March
                          sample is common to consecutive years).
"""
import gzip, sys, urllib.request
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tabulate import build_units, estimates, BANDS

REP_DIR = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/cps_raw/rep")
D = Path(__file__).resolve().parent.parent
B = "https://www2.census.gov/programs-surveys/cps/datasets"
X = "https://www2.census.gov/programs-surveys/demo/datasets/income-poverty/time-series/data-extracts"
REP = {(y, "production"): f"{B}/{y}/march/CPS_ASEC_ASCII_REPWGT_{y}.dat.gz" for y in (2005, 2010, 2013, 2015, 2017, 2018, 2019)}
REP.update({(y, "production"): f"{B}/{y}/march/CPS_ASEC_ASCII_REPWGT_{y}.DAT.GZ" for y in range(2020, 2027)})
REP.update({
    (2014, "traditional_5x8"): f"{B}/2014/march/CPS_ASEC_ASCII_REPWGT_2014.dat.gz",
    (2014, "redesign_3x8"): f"{B}/2014/march/CPS_ASEC_ASCII_REPWGT_2014_3x8_run5.dat.gz",
    (2017, "research_updated"): f"{X}/2017/cps-asec-research-file/cps_asec_ascii_repwgt_2017_111618.dat",
    (2018, "bridge_updated"): f"{X}/2018/cps-asec-bridge-file/cps_asec_ascii_repwgt_2018_022619.dat",
})
UNITS = ["person65", "aged_unit", "aged_unit_married", "aged_unit_nonmarried"]
Z90 = 1.645
WC = [f"w{i}" for i in range(161)]


def fetch(url):
    p = REP_DIR / url.rsplit("/", 1)[1]
    if not p.exists():
        REP_DIR.mkdir(parents=True, exist_ok=True); urllib.request.urlretrieve(url, p)
    return p


def read_rep(path, keys):
    """ph_seq, pppos, w0..w160 for the person keys given (copied from cps/scripts/se.py)."""
    raw = (gzip.open(path) if str(path).lower().endswith("gz") else open(path, "rb")).read()
    L = raw.index(b"\n"); nb = 10 if L == 1617 else 9
    a = np.frombuffer(raw, dtype=np.uint8)
    if len(a) % (L + 1): a = np.concatenate([a, np.frombuffer(b"\n", np.uint8)])
    a = a.reshape(-1, L + 1)
    dig = lambda blk: (blk.astype(np.int64) - 48) @ (10 ** np.arange(blk.shape[-1] - 1, -1, -1))
    k = pd.DataFrame({"ph_seq": dig(a[:, 161*nb:161*nb+5]), "pppos": dig(a[:, 161*nb+5:161*nb+7])})
    m = k.reset_index().merge(keys, on=["ph_seq", "pppos"])
    sub = a[m["index"].to_numpy(), :161*nb].reshape(len(m), 161, nb)
    if ((sub < 48) | (sub > 57)).any():
        w = sub.view(f"S{nb}").reshape(len(m), 161).astype(str).astype(float) / 1e4
    else:
        w = dig(sub) / 1e4
    return pd.concat([m[["ph_seq", "pppos"]], pd.DataFrame(w, columns=WC)], axis=1)


def unit_frames(g):
    """person65 / aged-unit frames, each with the 161 weights of its representative person"""
    r = read_rep(fetch(REP[(g.asec_year.iloc[0], g.file.iloc[0])]), g[["ph_seq", "pppos"]].drop_duplicates())
    gp = g.merge(r, on=["ph_seq", "pppos"], how="left")
    assert gp.w0.notna().all() and (gp.w0 - gp.wt).abs().max() < 0.011, "replicate merge failed"
    p65, u = build_units(g)
    p65 = p65.merge(r, on=["ph_seq", "pppos"])
    rep_of_line = gp[["ph_seq", "a_lineno"] + WC].rename(columns={"a_lineno": "unit_line"})
    u = u.merge(rep_of_line, on=["ph_seq", "unit_line"])
    return {"person65": p65, "aged_unit": u, "aged_unit_married": u[u.n_members == 2],
            "aged_unit_nonmarried": u[u.n_members == 1]}, r


def all_estimates(frames):
    """(unit, band) -> dict measure -> array(161)"""
    out = {}
    for unit, df in frames.items():
        for band, lo, hi in BANDS:
            b = df[df.unit_age.between(lo, hi)]
            out[(unit, band)] = estimates(b, b[WC].to_numpy())
    return out


def se(th):
    return np.sqrt(4 / 160 * ((th[1:] - th[0]) ** 2).sum())


def main():
    a = pd.read_parquet(D / "data" / "asec_aged_income_persons.parquet")
    res, reps, rows = {}, {}, []
    for key in REP:
        g = a[(a.asec_year == key[0]) & (a.file == key[1])]
        frames, r = unit_frames(g)
        res[key] = all_estimates(frames); reps[key] = r
        for (unit, band), est in res[key].items():
            for m, th in est.items():
                s = se(th)
                rows.append(dict(asec_year=key[0], income_year=key[0] - 1, file=key[1], unit=unit, age=band,
                                 measure=m, estimate=th[0], se=s, ci90_lo=th[0] - Z90 * s, ci90_hi=th[0] + Z90 * s))
        print(key, "done", flush=True)
    pd.DataFrame(rows).to_csv(D / "output" / "se_income_sources.csv", index=False, float_format="%.4f")

    def paired_ok(k0, k1):
        m = reps[k0].merge(reps[k1], on=["ph_seq", "pppos"], suffixes=("_a", "_b"))
        if len(m) < 0.99 * len(reps[k0]): return False
        return bool(np.allclose(m[[c + "_a" for c in WC]].to_numpy(), m[[c + "_b" for c in WC]].to_numpy(), atol=0.011))

    comps = [((2014, "traditional_5x8"), (2014, "redesign_3x8"), "break: 2014 redesign of income questions"),
             ((2017, "production"), (2017, "research_updated"), "break: 2019 processing system (2017 sample)"),
             ((2018, "production"), (2018, "bridge_updated"), "break: 2019 processing system (2018 sample)"),
             ((2005, "production"), (2013, "production"), "change: legacy traditional series"),
             ((2015, "production"), (2018, "production"), "change: legacy redesigned series"),
             ((2019, "production"), (2020, "production"), "change: updated series"),
             ((2020, "production"), (2021, "production"), "change: updated series"),
             ((2021, "production"), (2022, "production"), "change: updated series"),
             ((2019, "production"), (2022, "production"), "change: updated series"),
             ((2025, "production"), (2026, "production"), "change: updated series"),
             ((2019, "production"), (2026, "production"), "change: updated series"),
             ((2018, "bridge_updated"), (2026, "production"), "change: updated series")]
    dr = []
    for k0, k1, kind in comps:
        paired = kind.startswith("break") and k0[0] == k1[0] and k0[0] != 2014 and paired_ok(k0, k1)
        print(k0, k1, "paired replicates" if paired else "independent")
        for uk in res[k0]:
            for m in res[k0][uk]:
                t0, t1 = res[k0][uk][m], res[k1][uk][m]
                d = t1[0] - t0[0]
                s = se(t1 - t0) if paired else np.hypot(se(t0), se(t1))
                dr.append(dict(kind=kind, from_asec=k0[0], from_file=k0[1], to_asec=k1[0], to_file=k1[1],
                               unit=uk[0], age=uk[1], measure=m, from_est=t0[0], to_est=t1[0], diff=d, se_diff=s,
                               z=d / s if s > 0 else np.nan, sig90=bool(s > 0 and abs(d / s) > Z90),
                               se_method="paired replicates" if paired else "independent samples"))
    pd.DataFrame(dr).to_csv(D / "output" / "se_changes.csv", index=False, float_format="%.4f")
    t = pd.DataFrame(rows)
    sel = t[(t.age == "65+") & (t.unit.isin(["person65", "aged_unit"])) & (t.asec_year == 2026) &
            t.measure.str.startswith(("share_of_aggregate__", "pct_receiving__", "ss_reliance_ge"))]
    print(sel[["unit", "measure", "estimate", "se"]].round(2).to_string())


if __name__ == "__main__":
    main()
