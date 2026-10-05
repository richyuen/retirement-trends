"""SCF 1989-2022: debt and housing wealth of older households, by age of the reference person.

Inputs: ../scf/raw/rscfpYYYY.dta (Fed summary extract, 2022 dollars) and pYY_rw1.dta
(999 bootstrap replicate weights, 2004+). Variables are the Fed's bulletin.macro.txt definitions:
  HDEBT (any debt), HMRTHEL (mortgage/HELOC on primary residence), HCCBAL (credit-card balance
  after last payment), DEBT, INCOME, ASSET, NETWORTH, HOMEEQ (= HOUSES - MRTHEL), HOUSES,
  HOUSECL (1 = owns primary residence, Fed homeownership definition), PIRTOTAL, PIR40.
Groups: 55-64, 65-74, 75+, and 65+ (age of reference person at interview).
Point estimates pool the 5 implicates; SEs (2004+) as in scf/scripts/scf_analysis.py
(replicate weights on implicate 1 + 1.2 x between-implicate variance).
Output: ../output/scf_debt_housing_long.csv and wide tables scf_t*.csv
Run: python3 debt_housing/scripts/scf_debt_housing.py   (about 5-10 minutes)
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parent / "scf" / "scripts"))
from scf_analysis import read, estimate, load_rw, wmedian, share, median_of, ratio  # noqa: E402

RAW = HERE.parent / "scf" / "raw"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
WAVES = [1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016, 2019, 2022]
VARS = ["y1", "yy1", "x1", "xx1", "wgt", "age", "hdebt", "hmrthel", "hccbal", "debt", "income", "asset",
        "networth", "homeeq", "houses", "housecl", "pirtotal", "pir40", "debt2inc", "levratio", "mrthel", "ccbal"]
GROUPS = {"55-64": "age >= 55 & age <= 64", "65-74": "age >= 65 & age <= 74",
          "75+": "age >= 75", "65+": "age >= 65", "all": "age >= 0"}


def load(year):
    s = read(RAW / f"rscfp{year}.dta", VARS).rename(columns={"x1": "y1", "xx1": "yy1"})
    s["imp"] = (s.y1 - s.yy1 * 10).astype(int)
    s["owner"] = s.housecl == 1
    s["eqshare"] = np.where(s.networth > 0, 100 * s.homeeq / s.networth.where(s.networth > 0, 1), np.nan)
    return s


def median_ratio(num, den, cond):
    """Weighted median of household-level num/den among cond."""
    def prep(d):
        m = d.eval(cond).values
        x = d[num].values[m] / d[den].values[m]
        return lambda w: 100 * wmedian(x, w[m])
    return prep


def stats(g):
    c = GROUPS[g]
    return {
        "pct_any_debt": share("hdebt == 1", c),
        "pct_home_secured_debt": share("hmrthel == 1", c),
        "pct_cc_balance": share("hccbal == 1", c),
        "median_debt_if_any": median_of("debt", f"({c}) & debt > 0"),
        "agg_debt_to_income_pct": ratio("debt", "income", c),
        "median_debt_to_income_debtors_pct": median_ratio("debt", "income", f"({c}) & debt > 0 & income > 0"),
        "agg_debt_to_assets_pct": ratio("debt", "asset", c),
        "pct_pmt_over_40pct_income_debtors": share("pir40 == 1", f"({c}) & debt > 0"),
        "pct_homeowner": share("owner", c),
        "pct_owners_with_home_debt": share("hmrthel == 1", f"({c}) & owner"),
        "median_home_value_owners": median_of("houses", f"({c}) & owner"),
        "median_home_equity_owners": median_of("homeeq", f"({c}) & owner"),
        "median_mortgage_owners_w_mortgage": median_of("mrthel", f"({c}) & owner & mrthel > 0"),
        "agg_home_equity_share_networth_pct": ratio("homeeq", "networth", c),
        "median_home_equity_share_networth_owners_pct": median_of("eqshare", f"({c}) & owner & networth > 0"),
    }


def main():
    rows = []
    for y in WAVES:
        d = load(y)
        rw = load_rw(y) if y >= 2004 else None
        for g in GROUPS:
            for name, fn in stats(g).items():
                p, se = estimate(d, rw, fn)
                rows.append(dict(year=y, group=g, stat=name, value=p, se=se))
        print(y, "done", flush=True)
    long = pd.DataFrame(rows)
    long.to_csv(OUT / "scf_debt_housing_long.csv", index=False, float_format="%.4f")
    tabs = {
        "scf_t1_any_debt_pct": "pct_any_debt", "scf_t2_home_secured_debt_pct": "pct_home_secured_debt",
        "scf_t3_cc_balance_pct": "pct_cc_balance", "scf_t4_median_debt_debtors_2022usd": "median_debt_if_any",
        "scf_t5_agg_debt_to_income_pct": "agg_debt_to_income_pct",
        "scf_t6_median_debt_to_income_debtors_pct": "median_debt_to_income_debtors_pct",
        "scf_t7_agg_debt_to_assets_pct": "agg_debt_to_assets_pct",
        "scf_t8_pmt_over_40pct_debtors_pct": "pct_pmt_over_40pct_income_debtors",
        "scf_t9_homeownership_pct": "pct_homeowner", "scf_t10_owners_with_home_debt_pct": "pct_owners_with_home_debt",
        "scf_t11_home_equity_share_networth_agg_pct": "agg_home_equity_share_networth_pct",
        "scf_t12_home_equity_share_networth_median_owners_pct": "median_home_equity_share_networth_owners_pct",
        "scf_t13_median_home_equity_owners_2022usd": "median_home_equity_owners",
        "scf_t14_median_mortgage_if_any_owners_2022usd": "median_mortgage_owners_w_mortgage",
    }
    for f, s in tabs.items():
        t = long[long.stat == s]
        w = t.pivot(index="year", columns="group", values="value")[list(GROUPS)]
        se = t.pivot(index="year", columns="group", values="se")[list(GROUPS)].add_suffix("_se")
        w.join(se).round(2).to_csv(OUT / f"{f}.csv")
    show = long[long.group.isin(["55-64", "65-74", "75+"]) & long.year.isin([1989, 2001, 2022])]
    print(show.pivot_table(index=["stat"], columns=["group", "year"], values="value").round(1).to_string())


if __name__ == "__main__":
    main()
