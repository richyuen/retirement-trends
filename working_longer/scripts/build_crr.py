"""CRR (Boston College) average retirement age and Social Security claiming figures.

Inputs (raw/crr/, downloaded from crr.bc.edu; text via `pdftotext -layout`):
  avg_ret_age_2025-11.pdf/.txt  https://crr.bc.edu/wp-content/uploads/2025/11/Average-retirement-age.pdf
  avg_ret_age_2025-03.pdf/.txt  https://crr.bc.edu/wp-content/uploads/2025/03/Average-retirement-age.pdf (1962-2024 edition)
  IB_25-10.pdf  https://crr.bc.edu/wp-content/uploads/2025/05/IB_25-10.pdf  (claiming ages, Figure 1 bar labels)
  IB_21-9.pdf   https://crr.bc.edu/wp-content/uploads/2021/05/IB_21-9.pdf   (pre-COVID claiming)
Outputs:
  output/crr_average_retirement_age.csv   year, men, women (whole years as tabulated; 2024/2025 decimals from chart labels)
  output/crr_claiming_age_distribution.csv  claim-year distribution of retired-worker awards, 2019 vs 2023 (IB 25-10 Fig 1)
  output/crr_claiming_at_62_cohort.csv     % claiming at 62, claim-year vs birth-year (cohort) basis (IB 15-8 Table 1)
  IB_15-8.pdf   https://crr.bc.edu/wp-content/uploads/2015/05/IB_15-8.pdf   (claim-year vs cohort claiming at 62)
Run: python3 scripts/build_crr.py
"""
import os, re
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "raw", "crr")
OUT = os.path.join(ROOT, "output")


def avg_ret_age():
    rows = []
    for line in open(os.path.join(RAW, "avg_ret_age_2025-11.txt")):
        m = re.search(r"\b(19[6-9]\d|20[0-2]\d)\s+(\d\d)\s+(\d\d)\s*$", line)
        if m:
            rows.append(dict(year=int(m.group(1)), men=int(m.group(2)), women=int(m.group(3))))
    df = pd.DataFrame(rows).drop_duplicates("year").sort_values("year")
    # chart end-point labels (one decimal): 2025 edition 64.8 / 63.3; 2024 edition 64.6 / 62.6 (also in IB 25-8 Fig 3)
    dec = {2025: (64.8, 63.3), 2024: (64.6, 62.6)}
    df["men_decimal"] = df.year.map(lambda y: dec.get(y, (None, None))[0])
    df["women_decimal"] = df.year.map(lambda y: dec.get(y, (None, None))[1])
    df["note"] = "CRR: age at which LFPR (CPS) consistently drops below 50%; table rounds to whole years"
    df.to_csv(os.path.join(OUT, "crr_average_retirement_age.csv"), index=False)
    print("CRR average retirement age, selected years:")
    print(df[df.year.isin([1962, 1971, 1983, 1986, 1995, 2004, 2010, 2016, 2019, 2024, 2025])][["year", "men", "women", "men_decimal", "women_decimal"]].to_string(index=False))
    return df


def claiming():
    # IB 25-10 Figure 1 (read from bar labels; verified against the rendered page). Shares of retired-worker awards by age.
    ages = ["62", "63", "64", "65", "66 (FRA)", "67+"]
    men = {2019: [31, 7, 7, 13, 23, 19], 2023: [26, 7, 8, 16, 17, 26]}
    women = {2019: [34, 7, 8, 13, 17, 20], 2023: [27, 8, 8, 16, 15, 25]}
    rows = []
    for sex, d in [("men", men), ("women", women)]:
        for yr, vals in d.items():
            assert 99 <= sum(vals) <= 101, (sex, yr, sum(vals))
            for a, v in zip(ages, vals):
                rows.append(dict(claim_year=yr, sex=sex, claim_age=a, pct_of_awards=v,
                                 source="CRR IB 25-10 Fig 1, from SSA Annual Statistical Supplement 2024"))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "crr_claiming_age_distribution.csv"), index=False)
    print("Claim-year distribution (% of retired-worker awards):")
    print(df.pivot(index=["sex", "claim_year"], columns="claim_age", values="pct_of_awards")[ages].to_string())


def cohort62():
    # IB 15-8 Table 1: % claiming retired-worker benefits at 62. "Year" = claim year, or year the birth cohort turned 62.
    t = []
    for line in open(os.path.join(RAW, "IB_15-8.txt")):
        m = re.search(r"\b(1985|1996|2013)\s+([\d.]+)\s*%?\s+([\d.]+)\s*%?\s+([\d.]+)\s*%?\s+([\d.]+)", line)
        if m:
            y, a, b, c, d = m.groups()
            t.append(dict(year=int(y), men_claim_year=float(a), men_birth_year=float(b),
                          women_claim_year=float(c), women_birth_year=float(d),
                          source="CRR IB 15-8 Table 1 (SSA data)"))
    df = pd.DataFrame(t)
    df = df[df.men_claim_year < 100]
    assert len(df) == 3, df
    df.to_csv(os.path.join(OUT, "crr_claiming_at_62_cohort.csv"), index=False)
    print("% claiming at 62 (claim-year vs birth-year basis):"); print(df.drop(columns="source").to_string(index=False))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    avg_ret_age()
    claiming()
    cohort62()
