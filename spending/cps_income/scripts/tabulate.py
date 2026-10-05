"""Income sources of people 65+ and of SSA-style aged units, CPS ASEC 1998-2026 (point estimates, MARSUPWT).

Usage: python tabulate.py      (reads ../data/asec_aged_income_persons.parquet from extract.py)
Outputs (../output/):
  income_sources_long.csv        every year x file x unit (person65 | aged_unit) x age band x source:
                                 pct_receiving, share_of_aggregate_income (both %), plus unit-level rows
                                 (population, n, mean income, SS reliance, % with any earnings)
  income_share_65plus_wide.csv   headline: share of aggregate income by source, persons 65+, one row per year/file
  income_share_exclRINT_65plus_wide.csv   the same with interest credited inside retirement accounts (RINT, updated
                                 processing only) removed from asset income and from the total
  income_recipiency_65plus_wide.csv   headline: % receiving each source, persons 65+
  aged_unit_share_wide.csv / aged_unit_recipiency_wide.csv / aged_unit_share_exclRINT_wide.csv   aged units
  income_by_age_band_persons.csv  shares and % receiving by age band 65-69 / 70-74 / 75-79 / 80+ (persons)
  ss_reliance_wide.csv           % of Social Security beneficiary aged units (and persons 65+) with SS >= 50% / >= 90%
                                 of their income

Units
  person65   each person aged 65+ (own income only). Simple, and the unit Census uses in its PINC tables.
  aged_unit  SSA "Income of the Aged" unit: a married couple living together with at least one spouse 65+ (incomes
             of both spouses pooled) or a nonmarried person 65+. Spouses are linked by A_SPOUSE -> A_LINENO
             within the household; ASEC gives both spouses the same MARSUPWT (checked: all 385k pairs), so the unit
             takes that weight. Age band of a couple = age of the older spouse. Also split into
             aged_unit_married / aged_unit_nonmarried (SSA reports SS reliance separately for these).
"""
from pathlib import Path
import numpy as np, pandas as pd

D = Path(__file__).resolve().parent.parent
GROUPS = {  # output source -> harmonized components (extract.py)
    "earnings": ["earn"],
    "social_security": ["ss"],
    "db_pension": ["pen_db"],
    "annuity": ["annuity"],
    "acct_withdrawal": ["acct"],
    "asset_income": ["int_nonret", "int_ret", "div", "rent"],
    "ssi_public_assist": ["ssi", "pa"],
    "other": ["vet", "other"],
    # memo items (overlap with the above)
    "memo_retirement_income": ["pen_db", "annuity", "acct"],
    "memo_db_own_pension": ["pen_own"],
    "memo_db_survivor_disability": ["pen_survdis"],
    "memo_interest_in_retirement_accts": ["int_ret"],
    "memo_asset_excl_ret_acct_interest": ["int_nonret", "div", "rent"],
    "memo_veterans": ["vet"],
}
MAIN = ["earnings", "social_security", "db_pension", "annuity", "acct_withdrawal", "asset_income",
        "ssi_public_assist", "other"]
BANDS = [("65+", 65, 200), ("65-69", 65, 69), ("70-74", 70, 74), ("75-79", 75, 79), ("80+", 80, 200)]
FILE_LABEL = {"production": "production", "traditional_5x8": "2014 traditional questions (5/8 sample)",
              "redesign_3x8": "2014 redesigned questions (3/8 sample)",
              "research_updated": "2017 research file (updated processing)",
              "bridge_updated": "2018 bridge file (updated processing)"}


def series(asec_year, file, system):
    if system == "updated": return "C: updated processing (2017R, 2018B, 2019+)"
    if asec_year >= 2015 or file == "redesign_3x8": return "B: legacy processing, redesigned questions"
    return "A: legacy processing, traditional questions"


def build_units(a):
    """Return (persons65, aged_units) frames with component columns and wkswork-based worked flag."""
    comps = ["earn", "ss", "pen_db", "pen_own", "pen_survdis", "annuity", "acct", "int_nonret", "int_ret", "div",
             "rent", "ssi", "pa", "vet", "other", "total"]
    a = a.copy(); a["worked"] = (a.wkswork > 0).astype(int)
    p65 = a[a.age >= 65].copy(); p65["unit_age"] = p65.age
    p65["n_members"] = 1
    # aged units: key = (year, file, ph_seq, min(lineno, spouse lineno)) for couples; own lineno otherwise
    keys = ["asec_year", "file", "ph_seq"]
    has_sp = a.a_spouse > 0
    lines = a[keys + ["a_lineno"]].assign(present=1)
    sp_present = a[keys + ["a_spouse"]].merge(lines.rename(columns={"a_lineno": "a_spouse"}), on=keys + ["a_spouse"],
                                             how="left").present.fillna(0).to_numpy() == 1
    a["unit_line"] = np.where(has_sp & sp_present, np.minimum(a.a_lineno, a.a_spouse), a.a_lineno)
    g = a.groupby(keys + ["unit_line"], sort=False)
    u = g[comps].sum()
    u["wt"] = g.wt.first(); u["unit_age"] = g.age.max(); u["n_members"] = g.size(); u["worked"] = g.worked.max()
    u["system"] = g.system.first(); u["income_year"] = g.income_year.first()
    u = u.reset_index()
    u = u[u.unit_age >= 65]   # spouses kept only when the other spouse is 65+, so every unit qualifies; safety check
    return p65, u


def group_values(df):
    return {k: df[v].sum(axis=1).to_numpy(dtype=float) for k, v in GROUPS.items()}


def estimates(df, W):
    """df rows = units, W = (n, k) weight matrix. Returns dict name -> array(k)."""
    gv = group_values(df); tot = df.total.to_numpy(dtype=float)
    pop = W.sum(0); agg_tot = tot @ W
    r = {"population": pop, "mean_total_income": agg_tot / pop, "pct_worked_last_year": 100 * (df.worked.to_numpy() > 0) @ W / pop}
    for k, v in gv.items():
        if k in ("earnings", "asset_income", "other"):
            recv = v != 0 if k != "asset_income" else (df[GROUPS[k]].to_numpy() != 0).any(1)
        else:
            recv = v > 0
        r[f"pct_receiving__{k}"] = 100 * recv @ W / pop
        r[f"share_of_aggregate__{k}"] = 100 * (v @ W) / agg_tot
    # variant: total income without interest credited inside retirement accounts (updated processing only)
    rint = gv["memo_interest_in_retirement_accts"]; tot2 = tot - rint; agg2 = tot2 @ W
    for k in MAIN:
        v = gv[k] - (rint if k == "asset_income" else 0)
        r[f"share_of_aggregate_exclRINT__{k}"] = 100 * (v @ W) / agg2
    ss = gv["social_security"]; ben = (ss > 0) & (tot > 0)
    ratio = np.where(ben, ss / np.where(tot > 0, tot, 1), 0)
    ratio2 = np.where(ben, ss / np.where(tot2 > 0, tot2, 1), 0)
    nb = ben @ W
    r["pct_ss_beneficiary"] = 100 * nb / pop
    for thr, lab in [(0.5, "50"), (0.9, "90")]:
        r[f"ss_reliance_ge{lab}_pct_of_beneficiaries"] = 100 * (ben & (ratio >= thr)) @ W / nb
        r[f"ss_reliance_ge{lab}_pct_of_all"] = 100 * (ben & (ratio >= thr)) @ W / pop
        r[f"ss_reliance_ge{lab}_exclRINT_pct_of_beneficiaries"] = 100 * (ben & (ratio2 >= thr)) @ W / nb
    r["ss_reliance_100_pct_of_beneficiaries"] = 100 * (ben & (ratio >= 0.9999)) @ W / nb
    # median total income (point estimate only)
    return r


def wmedian(x, w):
    o = np.argsort(x); c = np.cumsum(w[o]); return x[o][np.searchsorted(c, c[-1] / 2)]


def main():
    a = pd.read_parquet(D / "data" / "asec_aged_income_persons.parquet")
    rows = []
    for (yr, f), g in a.groupby(["asec_year", "file"]):
        p65, u = build_units(g)
        for unit, df in [("person65", p65), ("aged_unit", u), ("aged_unit_married", u[u.n_members == 2]),
                         ("aged_unit_nonmarried", u[u.n_members == 1])]:
            for band, lo, hi in BANDS:
                b = df[df.unit_age.between(lo, hi)]
                W = b.wt.to_numpy()[:, None]
                est = estimates(b, W)
                base = dict(asec_year=yr, income_year=yr - 1, file=f, file_label=FILE_LABEL[f],
                            series=series(yr, f, g.system.iloc[0]), unit=unit, age=band, n=len(b))
                for k, v in est.items():
                    rows.append({**base, "measure": k, "value": float(v[0])})
                rows.append({**base, "measure": "median_total_income",
                             "value": float(wmedian(b.total.to_numpy(float), b.wt.to_numpy()))})
                if unit == "aged_unit":
                    rows.append({**base, "measure": "pct_couple_units",
                                 "value": float(100 * (b.n_members == 2) @ b.wt / b.wt.sum())})
    t = pd.DataFrame(rows)
    t.to_csv(D / "output" / "income_sources_long.csv", index=False, float_format="%.4f")
    idx = ["asec_year", "income_year", "series", "file_label"]
    for unit, stem in [("person65", "income_{}_65plus_wide.csv"), ("aged_unit", "aged_unit_{}_wide.csv")]:
        s = t[(t.unit == unit) & (t.age == "65+")]
        for kind, nm in [("share_of_aggregate", "share"), ("pct_receiving", "recipiency"),
                         ("share_of_aggregate_exclRINT", "share_exclRINT")]:
            w = s[s.measure.str.startswith(kind + "__")].assign(src=lambda x: x.measure.str.split("__").str[1])
            w = w.pivot_table(index=idx, columns="src", values="value", sort=False)
            w = w[[c for c in MAIN + sorted(w.columns) if c in w.columns and (c in MAIN or c.startswith("memo"))]]
            w = w.loc[:, ~w.columns.duplicated()]
            extra = s[s.measure.isin(["population", "mean_total_income", "median_total_income", "pct_worked_last_year"])]
            extra = extra.pivot_table(index=idx, columns="measure", values="value", sort=False)
            w = w.join(extra).reset_index(); w.columns.name = None
            w["population"] = w.population / 1e6; w = w.rename(columns={"population": "population_m"})
            w = w.sort_values(["series", "asec_year"])
            w.to_csv(D / "output" / stem.format(nm), index=False, float_format="%.2f")
    # by age band, persons 65+: share of aggregate income and % receiving, main sources
    ab = t[(t.unit == "person65") & t.measure.str.match(r"^(share_of_aggregate|pct_receiving)__")]
    ab = ab[ab.measure.str.split("__").str[1].isin(MAIN)]
    ab = ab.pivot_table(index=idx + ["age"], columns="measure", values="value", sort=False).reset_index()
    ab.columns.name = None
    ab.sort_values(["series", "asec_year", "age"]).to_csv(D / "output" / "income_by_age_band_persons.csv",
                                                          index=False, float_format="%.2f")
    rel = t[(t.age == "65+") & t.measure.str.startswith(("ss_reliance", "pct_ss_beneficiary"))]
    rel = rel.pivot_table(index=idx, columns=["unit", "measure"], values="value", sort=False)
    rel.columns = [f"{u}__{m}" for u, m in rel.columns]
    rel.reset_index().sort_values(["series", "asec_year"]).to_csv(D / "output" / "ss_reliance_wide.csv", index=False,
                                                                 float_format="%.2f")
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
    print(pd.read_csv(D / "output" / "income_share_65plus_wide.csv").iloc[:, [0, 2] + list(range(4, 13))].round(1).to_string())
    print(pd.read_csv(D / "output" / "ss_reliance_wide.csv").round(1).to_string())


if __name__ == "__main__":
    main()
