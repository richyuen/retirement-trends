"""(c) How much of the 2003/06 -> 2018/21 (and -> 2021) change in withdrawal incidence and dollar rate among
retirement-account holders is explained by composition?

1. Differences late - early with SEs, and an accounting split of the dollar rate:
     rate = (withdrawals per holder) / (balance per holder)
     ln(rate_late / rate_early) = ln(wd/holder ratio) - ln(balance/holder ratio)
   and rate = IRA part + account-pension part.
2. DiNardo-Fortin-Lemieux reweighting: a weighted logit of P(late | X) on the pooled early+late holders gives
   psi = P(early|X)/P(late|X) x P(late)/P(early); reweighting late households by psi gives the counterfactual
   late outcome with the early composition of X. composition = actual late - counterfactual;
   unexplained (within-cell) = counterfactual - early.  The logit is refit for every implicate and every
   replicate weight, so SEs include the reweighting step.
3. Pooled weighted linear probability model, all 7 waves, holders: 100*1{withdrew} on wave dummies with and
   without controls; the late-vs-early contrast before and after controls.
Outputs: output/c_differences.csv, output/c_dfl.csv, output/c_lpm.csv
Run: python3 scf_6064/scripts/c_decomposition.py   (about 10 minutes)
"""
import numpy as np, pandas as pd
from common import load_all, band, add_derived, estimate_v, OUT, BANDS, PERIODS

SPECS = {
    "work_ss": ["r_work", "sp_work", "marr", "r_ss"],
    "accounts": ["has_ira", "has_oldpen", "tsh_1", "tsh_2"],  # tsh_1 + tsh_2 = has THRIFT
    "balance_income": ["bal_1", "bal_2", "bal_3", "bal_4", "bal_5", "inc_1", "inc_2", "inc_3", "inc_4"],
    "demographics": ["ed_2", "ed_3", "ed_4", "db", "female", "age_1", "age_2", "age_3", "age_4"],
}
SPECS["all"] = sum(SPECS.values(), [])
TARGETS = {"2009": [2010], "2012": [2013], "2015": [2016], "2018": [2019], "2021": [2022], "2018/21": PERIODS["2018/21"]}
EARLY = PERIODS["2003/06"]


def dummies(d, lo):
    d = d.copy()
    for k in (1, 2):
        d[f"tsh_{k}"] = d.tsh_bin == k
    for k in range(1, 6):
        d[f"bal_{k}"] = d.bal_bin == k
    for k in range(1, 5):
        d[f"inc_{k}"] = d.inc_bin == k
    for k in (2, 3, 4):
        d[f"ed_{k}"] = d.edcl == k
    for k in range(1, 5):
        d[f"age_{k}"] = d.age == lo + k
    return d


def logit(X, y, w, lam=1e-3, iters=50):
    w = w / w.mean()
    b = np.zeros(X.shape[1])
    R = lam * np.eye(X.shape[1]); R[0, 0] = 0
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(X @ b, -30, 30)))
        g = X.T @ (w * (y - p)) - R @ b
        H = (X * (w * p * (1 - p))[:, None]).T @ X + R
        step = np.linalg.solve(H, g)
        b += step
        if np.abs(step).max() < 1e-9:
            break
    return 1 / (1 + np.exp(-np.clip(X @ b, -30, 30)))


def dfl(spec):
    def prep(d):
        h = d.holder.values
        X = np.column_stack([np.ones(len(d))] + [d[c].values.astype(float) for c in SPECS[spec]])[h]
        per = d.per.values[h].astype(float)
        ys = {"inc": d.wd_any.values[h].astype(float) * 100, "wd5": d.wd5.values[h].astype(float) * 100,
              "wd10": d.wd10.values[h].astype(float) * 100}
        W, B = d.penacctwd.values[h], d.retqliq.values[h]
        NT = (~d.top3.values[h]).astype(float)

        def f(w):
            w = w[h]
            p = logit(X, per, w)
            l, e = per == 1, per == 0
            psi = (1 - p[l]) / p[l] * w[l].sum() / w[e].sum()
            wl = w[l] * psi
            out = []
            for k, y in ys.items():
                y0 = (y[e] * w[e]).sum() / w[e].sum(); y1 = (y[l] * w[l]).sum() / w[l].sum()
                cf = (y[l] * wl).sum() / wl.sum()
                out += [y0, y1, y1 - y0, cf, y1 - cf, cf - y0]
            r0 = 100 * (W[e] * w[e]).sum() / (B[e] * w[e]).sum(); r1 = 100 * (W[l] * w[l]).sum() / (B[l] * w[l]).sum()
            rc = 100 * (W[l] * wl).sum() / (B[l] * wl).sum()
            out += [r0, r1, r1 - r0, rc, r1 - rc, rc - r0]
            Wn, Bn = W * NT, B * NT   # rate excluding each wave's top-3 withdrawing households
            r0 = 100 * (Wn[e] * w[e]).sum() / (Bn[e] * w[e]).sum(); r1 = 100 * (Wn[l] * w[l]).sum() / (Bn[l] * w[l]).sum()
            rc = 100 * (Wn[l] * wl).sum() / (Bn[l] * wl).sum()
            out += [r0, r1, r1 - r0, rc, r1 - rc, rc - r0]
            out += [(wl.max() / wl.sum()) * 100, wl.sum() ** 2 / (wl ** 2).sum()]  # diagnostics
            return np.array(out)
        return f
    return prep


DFL_NAMES = [f"{o}_{c}" for o in ("incidence_per100", "wd_ge5pct_per100", "wd_ge10pct_per100", "rate_pct", "rate_excl_top3_pct")
             for c in ("early", "late", "change", "counterfactual_late", "composition", "unexplained")] + \
            ["max_weight_share_pct", "effective_n_late"]


def diffs():
    """late - early differences and log accounting of the rate."""
    def prep(d):
        h = d.holder.values.astype(float); p1 = d.per.values.astype(float) * h; p0 = (1 - d.per.values) * h
        cols = {k: d.eval(v).values.astype(float) for k, v in dict(
            inc="wd_any * 100", wd5="wd5 * 100", wd10="wd10 * 100", wd="penacctwd", ira="ira_wd", pen="pen_wd", bal="retqliq",
            balx="retqliq - thrift", nt="(not top3) * 1.0").items()}

        def f(w):
            res = []
            for p in (p0, p1):
                n = p @ w
                s = {k: (v * p) @ w for k, v in cols.items()}
                wd_nt = (cols["wd"] * cols["nt"] * p) @ w; bal_nt = (cols["bal"] * cols["nt"] * p) @ w
                res.append(np.array([s["inc"] / n, s["wd5"] / n, s["wd10"] / n, 100 * s["wd"] / s["bal"], 100 * s["ira"] / s["bal"],
                                     100 * s["pen"] / s["bal"], 100 * s["wd"] / s["balx"], 100 * wd_nt / bal_nt,
                                     s["wd"] / n / 1e3, s["bal"] / n / 1e3]))
            e, l = res
            acc = np.stack([np.log(l[3] / e[3]), np.log(l[8] / e[8]), -np.log(l[9] / e[9])])
            return np.concatenate([e, l, l - e, acc])
        f.vec = True
        return f
    return prep


DIFF_STATS = ["incidence_per100", "wd_ge5pct_per100", "wd_ge10pct_per100", "rate_pct", "rate_ira_part_pct", "rate_pension_part_pct",
              "rate_excl_thrift_pct", "rate_excl_top3_pct", "wd_per_holder_k", "bal_per_holder_k"]
DIFF_NAMES = [f"{s}_early" for s in DIFF_STATS] + [f"{s}_late" for s in DIFF_STATS] + [f"{s}_change" for s in DIFF_STATS] + \
             ["ln_rate_ratio", "ln_rate_from_wd_per_holder", "ln_rate_from_balance_per_holder"]

WAVES = [2004, 2007, 2010, 2013, 2016, 2019, 2022]


def lpm(controls, outcome):
    def prep(d):
        h = d.holder.values
        dd = d[h]
        X = np.column_stack([np.ones(len(dd))] + [(dd.year == y).values.astype(float) for y in WAVES[1:]] +
                            [dd[c].values.astype(float) for c in controls])
        y = dd[outcome].values.astype(float) * 100

        def f(w):
            w = w[h]
            XtW = X.T * w
            b = np.linalg.lstsq(XtW @ X, XtW @ y, rcond=None)[0]
            bw = dict(zip(WAVES, [0.0] + list(b[1:len(WAVES)])))
            early = (bw[2004] + bw[2007]) / 2
            return np.array([(bw[2019] + bw[2022]) / 2 - early, bw[2022] - early] + [bw[yr] for yr in WAVES[1:]])
        return f
    return prep


def run():
    df = load_all()
    drows, frows, lrows = [], [], []
    for bname, (lo, hi) in BANDS.items():
        d = dummies(add_derived(band(df, bname), bname), lo)
        early = d[d.year.isin(EARLY)].assign(per=0)
        for tlab, yrs in TARGETS.items():
            dd = pd.concat([early, d[d.year.isin(yrs)].assign(per=1)])
            est, se = estimate_v(dd, diffs())
            for k, nm in enumerate(DIFF_NAMES):
                drows.append(dict(age_band=bname, early="2003/06", late=tlab, stat=nm, estimate=est[k], se=se[k]))
            for spec in SPECS:
                est, se = estimate_v(dd, dfl(spec))
                for k, nm in enumerate(DFL_NAMES):
                    frows.append(dict(age_band=bname, early="2003/06", late=tlab, spec=spec, stat=nm, estimate=est[k], se=se[k]))
            print(bname, tlab, "done", flush=True)
        for outcome in ("wd_any", "wd5", "wd10"):
            for cname, ctrl in [("none", []), ("work_ss", SPECS["work_ss"]), ("accounts", SPECS["accounts"]),
                                ("balance_income", SPECS["balance_income"]), ("demographics", SPECS["demographics"]),
                                ("all", SPECS["all"])]:
                est, se = estimate_v(d, lpm(ctrl, outcome))
                for k, nm in enumerate(["late_2018_21_minus_early_2003_06", "2021_minus_early_2003_06"] +
                                       [f"wave_{y - 1}_vs_2003" for y in WAVES[1:]]):
                    lrows.append(dict(age_band=bname, outcome=outcome, controls=cname, stat=nm, estimate=est[k], se=se[k]))
    pd.DataFrame(drows).to_csv(OUT / "c_differences.csv", index=False, float_format="%.4f")
    pd.DataFrame(frows).to_csv(OUT / "c_dfl.csv", index=False, float_format="%.4f")
    pd.DataFrame(lrows).to_csv(OUT / "c_lpm.csv", index=False, float_format="%.4f")


if __name__ == "__main__":
    run()
    f = pd.read_csv(OUT / "c_dfl.csv")
    x = f[(f.age_band == "60-64") & f.late.isin(["2018/21", "2021"]) & f.stat.str.contains("change|composition|unexplained|max_weight|effective")]
    print(x.pivot_table(index=["late", "stat"], columns="spec", values="estimate", sort=False).round(2).to_string())
    l = pd.read_csv(OUT / "c_lpm.csv")
    print(l[l.stat.str.contains("minus")].pivot_table(index=["age_band", "outcome", "stat"], columns="controls", values="estimate", sort=False).round(2).to_string())
