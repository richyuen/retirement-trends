"""Share of people receiving Social Security by single year of age, CPS ASEC 2010-2026.

A rough, public-microdata proxy for later claiming. Reads the shared extract built by the cps thread
(../cps/data/asec_persons_50plus.parquet, not modified here).

Caveats: SS_YN covers any Social Security income received during the prior calendar year (retired-worker,
disabled-worker, survivor and spouse benefits). Age is age at the March interview, so a person aged 63 in
March 2026 was mostly 62 during income year 2025. Ages 60-61 (before retirement eligibility) give the
baseline from disability/survivor benefits.

Output: output/cps_ss_receipt_by_age.csv (year, file, age band, % receiving SS, unweighted n)
Run:    python3 scripts/build_cps_ss.py
"""
import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARQ = os.path.join(os.path.dirname(ROOT), "cps", "data", "asec_persons_50plus.parquet")
OUT = os.path.join(ROOT, "output", "cps_ss_receipt_by_age.csv")
BANDS = {"60-61": (60, 61), "62": (62, 62), "63-64": (63, 64), "65-66": (65, 66), "67-69": (67, 69), "70-74": (70, 74)}


def main():
    d = pd.read_parquet(PARQ, columns=["age", "sex", "wt", "ss_recip", "asec_year", "file"])
    rows = []
    for (yr, f), g in d.groupby(["asec_year", "file"]):
        for band, (lo, hi) in BANDS.items():
            for sexlab, gg in [("both", g), ("men", g[g.sex == 1]), ("women", g[g.sex == 2])]:
                x = gg[gg.age.between(lo, hi)]
                rows.append(dict(asec_year=yr, income_year=yr - 1, file=f, sex=sexlab, age_at_interview=band,
                                 pct_receiving_ss=round((x.wt * x.ss_recip).sum() / x.wt.sum() * 100, 1), n=len(x)))
    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False)
    main_files = out[out.file.isin(["production", "traditional_5x8"]) & (out.sex == "both")]
    w = main_files.pivot(index="asec_year", columns="age_at_interview", values="pct_receiving_ss")
    print("% receiving Social Security (both sexes, production files; 2014 = traditional 5/8 file):")
    print(w[list(BANDS)].to_string())
    print("n per band, 2026:", out[(out.asec_year == 2026) & (out.sex == "both") & (out.file == "production")].set_index("age_at_interview").n.to_dict())
    for s in ["men", "women"]:
        m = out[(out.sex == s) & out.file.isin(["production", "traditional_5x8"])].pivot(index="asec_year", columns="age_at_interview", values="pct_receiving_ss")
        print(s, m.loc[[2010, 2019, 2026], ["63-64", "65-66"]].to_dict())


if __name__ == "__main__":
    main()
