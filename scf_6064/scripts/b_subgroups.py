"""(b) Withdrawal incidence and dollar rate within subgroups of account holders, by wave, and a shift-share
split of the early (2003/06) -> late (2018/21, and 2021 alone) change into between-group (composition) and
within-group parts.
  incidence = sum_g s_g y_g with s_g = holder shares;  rate = sum_g s_g r_g with s_g = balance (RETQLIQ) shares
  between = sum (s_g1 - s_g0) r_g0 ; within = sum s_g0 (r_g1 - r_g0) ; interaction = rest
Outputs: output/b_subgroups_long.csv, output/b_shiftshare.csv
Run: python3 scf_6064/scripts/b_subgroups.py
"""
import numpy as np, pandas as pd
from common import load_all, band, add_derived, groups_by_wave, estimate_v, vshare, vratio, OUT, BANDS, PERIODS

GROUPS = {
    "r_or_spouse_working": ("any_work", {True: "working", False: "neither working"}),
    "r_working": ("r_work", {True: "R working", False: "R not working"}),
    "account_type": ("acct_type", {"IRA only": "IRA only", "IRA and DC": "IRA and DC", "DC only": "DC only"}),
    "current_job_dc": ("has_thrift", {True: "has THRIFT", False: "no THRIFT"}),
    "r_social_security": ("r_ss", {True: "R gets SS", False: "R no SS"}),
    "db_pension": ("db", {True: "DB", False: "no DB"}),
    "work_x_thrift": ("wk_thr", {}),
}


def subgroup_stats(col, val):
    c = f"holder and {col} == {val!r}"
    return {
        "pct_of_holders": vshare(f"{col} == {val!r}"),
        "pct_of_balances": vratio(f"retqliq * ({col} == {val!r})", "retqliq"),
        "incidence_per100": vshare("wd_any", c),
        "rate_pct": vratio("penacctwd", "retqliq", c),
        "rate_ira_part_pct": vratio("ira_wd", "retqliq", c),
        "rate_pension_part_pct": vratio("pen_wd", "retqliq", c),
    }


def shiftshare(col, cats, outcome):
    """d has per (0/1). outcome 'inc' (holder-share weights) or 'rate' (balance-share weights)."""
    def prep(d):
        h = d.holder.values.astype(float)
        p1 = d.per.values.astype(float); p0 = 1 - p1
        G = np.column_stack([(d[col].values == c).astype(float) * h for c in cats])
        if outcome == "inc":
            den = np.ones(len(d)); num = d.wd_any.values.astype(float)
        else:
            den = d.retqliq.values.astype(float); num = d.penacctwd.values.astype(float)

        def f(w):
            w2 = w if w.ndim == 2 else w[:, None]
            res = []
            for p in (p0, p1):
                Dg = (G * (den * p)[:, None]).T @ w2          # cats x R
                Ng = (G * (num * p)[:, None]).T @ w2
                res.append((Dg / Dg.sum(0), Ng / Dg))
            (s0, r0), (s1, r1) = res
            y0 = (s0 * r0).sum(0); y1 = (s1 * r1).sum(0)
            btw = ((s1 - s0) * r0).sum(0); wit = (s0 * (r1 - r0)).sum(0)
            out = 100 * np.vstack([y0, y1, y1 - y0, btw, wit, y1 - y0 - btw - wit])
            return out[:, 0] if w.ndim == 1 else out
        f.vec = True
        return f
    return prep


def run():
    df = load_all()
    rows, ss = [], []
    for b in BANDS:
        d = add_derived(band(df, b), b)
        d["wk_thr"] = np.where(d.any_work, "working", "not working") + np.where(d.has_thrift, " + THRIFT", " no THRIFT")
        GROUPS["work_x_thrift"] = ("wk_thr", {v: v for v in sorted(d.wk_thr.unique())})
        for lab, g in groups_by_wave(d):
            for gname, (col, cats) in GROUPS.items():
                for val, vlab in cats.items():
                    n = int(((g[col] == val) & g.holder).sum() / 5)
                    nw = int(((g[col] == val) & g.holder & g.wd_any).sum() / 5)
                    for sname, fn in subgroup_stats(col, val).items():
                        est, se = estimate_v(g, fn)
                        rows.append(dict(age_band=b, wd_year=lab, grouping=gname, group=vlab, stat=sname,
                                         estimate=float(est), se=float(se), n_holders=n, n_withdrawers=nw))
        early = d[d.year.isin(PERIODS["2003/06"])].assign(per=0)
        for late_lab, yrs in [("2018/21", PERIODS["2018/21"]), ("2021", [2022])]:
            dd = pd.concat([early, d[d.year.isin(yrs)].assign(per=1)])
            for gname, (col, cats) in GROUPS.items():
                for outcome in ("inc", "rate"):
                    est, se = estimate_v(dd, shiftshare(col, list(cats), outcome))
                    for k, nm in enumerate(["early_2003_06", "late", "change", "between_composition", "within", "interaction"]):
                        ss.append(dict(age_band=b, late=late_lab, grouping=gname,
                                       outcome="incidence_per100" if outcome == "inc" else "rate_pct",
                                       component=nm, estimate=est[k], se=se[k]))
        print(b, "done", flush=True)
    pd.DataFrame(rows).to_csv(OUT / "b_subgroups_long.csv", index=False, float_format="%.4f")
    s = pd.DataFrame(ss)
    s.to_csv(OUT / "b_shiftshare.csv", index=False, float_format="%.4f")
    return pd.DataFrame(rows), s


if __name__ == "__main__":
    r, s = run()
    x = r[(r.age_band == "60-64") & r.stat.isin(["incidence_per100", "rate_pct", "pct_of_holders"])]
    print(x.pivot_table(index=["grouping", "group", "stat"], columns="wd_year", values="estimate", sort=False).round(2).to_string())
    print(s[s.age_band == "60-64"].pivot_table(index=["late", "grouping", "outcome"], columns="component", values="estimate", sort=False).round(2).to_string())
