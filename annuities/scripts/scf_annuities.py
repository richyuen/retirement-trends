"""SCF annuity ownership among older households, 1989-2022.

Inputs (read-only, from ../scf/raw/, Fed SCF public files https://www.federalreserve.gov/econres/scfindex.htm):
  rscfpYYYY.dta  summary extract (2022 dollars). ANNUIT = cash value of annuities in which the
                 household has an equity interest (bulletin.macro.txt):
                   2004+      ANNUIT = max(0, X6577)
                   1998-2001  ANNUIT = max(0, X6820)
                   1989-1995  ANNUIT = pro-rata share of X3942 "other managed assets" when the
                              household ticked annuities among up to 4 types (X3934-X3937): an
                              approximation, and pre-1998 is a different question.
                 FIN = total financial assets.
  pYYi6.dta      full public file, 2004+ (nominal dollars):
                   X6815 any annuity, income or assets, "do not include job pensions" (1 yes)
                   X6576 can cash in any (1 yes / 5 no); X6579 also has annuities you cannot cash in
                   X6575 bought with a payout/settlement from a past-job pension
                   X6578, X6580 annuity income received in prior year (cashable / non-cashable)
                   X11000/X11100/X11300/X11400  current-job plan has an account balance (1 yes, 5 no)
                   X11008/...  has a choice about how benefits are received
                   X11013/...  benefit expected to choose (1 lump sum/roll-over, 2 lifetime payments,
                               3 payment level you decide, 5 limited period, -7 other)
Age = age of the SCF reference person (AGE). Point estimates pool the 5 implicates (summary WGT
already divided by 5). No standard errors here: implicate spread is printed for the key series.
Run: python3 annuities/scripts/scf_annuities.py
"""
from pathlib import Path
import numpy as np, pandas as pd, pyreadstat

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT.parent / "scf" / "raw"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)
WAVES = [1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016, 2019, 2022]
GROUPS = {"all": (0, 200), "55-64": (55, 64), "65+": (65, 200), "65-74": (65, 74), "75+": (75, 200)}


def read(path, cols):
    _, meta = pyreadstat.read_dta(str(path), metadataonly=True)
    names = {c.lower(): c for c in meta.column_names}
    use = [names[c] for c in cols if c in names]
    df, _ = pyreadstat.read_dta(str(path), usecols=use)
    df.columns = df.columns.str.lower()
    return df


def wmedian(x, w):
    x, w = np.asarray(x, float), np.asarray(w, float)
    if len(x) == 0:
        return np.nan
    o = np.argsort(x); x, w = x[o], w[o]
    c = np.cumsum(w)
    return x[np.searchsorted(c, c[-1] / 2)]


def wshare(flag, w):
    return 100 * w[flag].sum() / w.sum()


PLAN = [(f"x11{k}00", f"x11{k}08", f"x11{k}13", f"x11{k}09") for k in "012345"]  # slots 2 and 5 (#1c/#2c) exist only in 2004-2007
# X11000 coding: 2010+ "any account balance?" 1 yes / 5 no. 2004-2007: 1 regular payments, 4 standard DB
# (-> traditional DB); 2 account, 3 both, 5 401(k), 6 thrift, 7 profit sharing, 10 SRA, 21 other account (-> account).
OLD_ACCT = {2, 3, 5, 6, 7, 10, 21}
OLD_DB = {1, 4}


def load(year):
    s = read(RAW / f"rscfp{year}.dta", ["y1", "yy1", "x1", "xx1", "wgt", "age", "annuit", "fin", "othma"])
    s = s.rename(columns={"x1": "y1", "xx1": "yy1"})
    s["imp"] = (s.y1 - s.yy1 * 10).astype(int)
    if year >= 2004:
        cols = ["y1", "x6815", "x6575", "x6576", "x6577", "x6578", "x6579", "x6580"]
        for p in PLAN:
            cols += list(p) + [f"x{int(p[3][1:]) + k}" for k in (1, 2, 3)]
        f = read(RAW / f"p{str(year)[2:]}i6.dta", cols)
        s = s.merge(f, on="y1", how="left", validate="1:1")
    s["year"] = year
    return s


rows, imp_rows, plan_rows = [], [], []
for year in WAVES:
    s = load(year)
    s["has_cash"] = s.annuit > 0
    for g, (lo, hi) in GROUPS.items():
        d = s[(s.age >= lo) & (s.age <= hi)]
        w = d.wgt.values
        r = {"year": year, "group": g, "n_obs_5imp": len(d),
             "pct_cashvalue_annuity": wshare(d.has_cash.values, w)}
        h = d[d.has_cash]
        r["median_cashvalue_holders_2022usd"] = wmedian(h.annuit, h.wgt)
        hf = h[h.fin > 0]
        r["median_annuit_pct_fin_holders"] = wmedian(100 * hf.annuit / hf.fin, hf.wgt)
        r["agg_annuit_pct_fin_allhh"] = 100 * (d.annuit * d.wgt).sum() / (d.fin * d.wgt).sum()
        if year >= 2004:
            anyann = d.x6815.values == 1
            noncash = anyann & ((d.x6576.values == 5) | (d.x6579.values == 1))
            inc = anyann & ((d.x6578.values > 0) | (d.x6580.values > 0))
            r["pct_any_annuity"] = wshare(anyann, w)
            r["pct_noncashable_annuity"] = wshare(noncash, w)
            r["pct_cashvalue_only"] = wshare(anyann & ~noncash, w)
            r["pct_receiving_annuity_income"] = wshare(inc, w)
            r["pct_holders_bought_with_pension_payout"] = wshare(d.x6575.values[anyann] == 1, w[anyann]) if anyann.any() else np.nan
            # median annual annuity income among recipients, nominal $ of prior year
            ai = (d.x6578.clip(lower=0) + d.x6580.clip(lower=0)).values
            r["median_annuity_income_recipients_nominal"] = wmedian(ai[inc], w[inc])
        rows.append(r)
        if g in ("55-64", "65+"):
            for i in range(1, 6):
                di = d[d.imp == i]
                rr = {"year": year, "group": g, "implicate": i,
                      "pct_cashvalue_annuity": wshare(di.has_cash.values, di.wgt.values)}
                if year >= 2004:
                    rr["pct_any_annuity"] = wshare(di.x6815.values == 1, di.wgt.values)
                imp_rows.append(rr)
    # expected benefit form for current-job plans where the worker has a choice (2004+)
    if year >= 2004:
        recs = []
        for acct, choice, pick, opt1 in PLAN:
            o = [f"x{int(opt1[1:]) + k}" for k in range(4)]
            if acct not in s:
                continue
            t = s[["y1", "wgt", "age", acct, choice, pick] + o].copy()
            t.columns = ["y1", "wgt", "age", "acct", "choice", "pick", "o1", "o2", "o3", "o4"]
            if year < 2010:
                t["acct"] = np.where(t.acct.isin(OLD_ACCT), 1, np.where(t.acct.isin(OLD_DB), 5, 0))
            recs.append(t[t.choice.isin([1, 5])])
        p = pd.concat(recs)
        p["ptype"] = np.where(p.acct == 1, "account balance (DC/cash balance)", np.where(p.acct == 5, "no account (traditional DB)", "unknown"))
        for (ptype, ages), sub in [((pt, a), p[(p.ptype == pt) & a_mask(p)]) for pt in p.ptype.unique() if pt != "unknown"
                                   for a, a_mask in [("all ages", lambda x: x.age > 0), ("50+", lambda x: x.age >= 50)]]:
            w = sub.wgt.values
            ch = sub[sub.choice == 1]
            wc = ch.wgt.values
            annuity_offered = (ch[["o1", "o2", "o3", "o4"]] == 2).any(axis=1).values
            r = {"year": year, "plan_type": ptype, "ref_person_age": ages, "n_plans_5imp": len(sub),
                 "pct_with_choice": wshare(sub.choice.values == 1, w),
                 "pct_choice_incl_lifetime_option": wshare(annuity_offered, wc)}
            # pick is 0 when only one option was reported -> exclude
            pk = ch[ch.pick != 0]
            wp = pk.wgt.values
            for code, lab in [(1, "lump_sum_rollover"), (2, "lifetime_payments"), (3, "payment_level_you_decide"), (5, "limited_period"), (-7, "other")]:
                r[f"pct_expect_{lab}"] = wshare(pk.pick.values == code, wp)
            # among those whose options included lifetime payments
            ann = pk[(pk[["o1", "o2", "o3", "o4"]] == 2).any(axis=1)]
            r["pct_expect_lifetime_given_offered"] = wshare(ann.pick.values == 2, ann.wgt.values)
            r["n_plans_offered_lifetime_and_picked_5imp"] = len(ann)
            plan_rows.append(r)

res = pd.DataFrame(rows).round(2)
res.to_csv(OUT / "scf_annuity_ownership_by_age.csv", index=False)
pd.DataFrame(imp_rows).round(2).to_csv(OUT / "scf_annuity_ownership_implicates.csv", index=False)
pr = pd.DataFrame(plan_rows).round(2)
pr.to_csv(OUT / "scf_pension_benefit_choice.csv", index=False)

pd.set_option("display.width", 200)
print("Share of households holding annuities (%), by age of reference person")
for g in ("55-64", "65+"):
    print(f"\n{g}")
    print(res[res.group == g][["year", "pct_cashvalue_annuity", "pct_any_annuity", "pct_noncashable_annuity",
                               "pct_receiving_annuity_income", "median_cashvalue_holders_2022usd",
                               "median_annuit_pct_fin_holders", "agg_annuit_pct_fin_allhh"]].to_string(index=False))
imp = pd.DataFrame(imp_rows)
print("\nImplicate range (max-min, pct points), any annuity / cash-value annuity, 65+:")
print(imp[imp.group == "65+"].groupby("year")[["pct_cashvalue_annuity", "pct_any_annuity"]].agg(lambda x: x.max() - x.min()).round(2).T.to_string())
print("\nCurrent-job plans with benefit choice, 50+ (expected form):")
print(pr[pr.ref_person_age == "50+"][["year", "plan_type", "pct_with_choice", "pct_choice_incl_lifetime_option",
                                       "pct_expect_lump_sum_rollover", "pct_expect_lifetime_payments",
                                       "pct_expect_lifetime_given_offered", "n_plans_offered_lifetime_and_picked_5imp"]].to_string(index=False))
