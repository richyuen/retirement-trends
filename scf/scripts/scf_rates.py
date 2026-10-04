"""SCF withdrawal rates, households 60+: all account holders vs withdrawers only.
Rates = withdrawals in the prior calendar year / account balance at interview (both in 2022 dollars).
  dollar-weighted: sum(withdrawals) / sum(balances) over the group
  median: weighted median of each household's own withdrawals / balance (withdrawers only)
Measures for all retirement accounts (PENACCTWD / RETQLIQ) and for IRAs only (IRA withdrawal items / IRAKH).
IRA withdrawal items (X6558+X6566+X6574) are nominal prior-year dollars; they are put in 2022 dollars
with the Fed's own factors (CPILAG x CPIADJ, from bulletin.macro.txt), as the Fed does for PENACCTWD.
Run: python3 scf/scripts/scf_rates.py   (uses scf_analysis.py helpers; about 1 minute)
"""
import numpy as np, pandas as pd
from scf_analysis import load, load_rw, estimate, ratio, median_of, WD_WAVES, OUT

# CPIBASE (2022 output) = 4376; (CPIADJ denominator, CPILAG) per wave from bulletin.macro.txt
CPI = {2004: (2785, 2770/2698), 2007: (3058, 3041/2957), 2010: (3204, 3198/3147), 2013: (3438, 3420/3369),
       2016: (3548, 3528/3483), 2019: (3775, 3758/3691), 2022: (4376, 4315/3992)}

STATS = {
    "any_rate_all_holders": ratio("penacctwd", "retqliq", "retqliq > 0"),
    "any_rate_withdrawers": ratio("penacctwd", "retqliq", "retqliq > 0 and penacctwd > 0"),
    "any_median_rate_withdrawers": median_of("r_any", "retqliq > 0 and penacctwd > 0"),
    "ira_rate_all_holders": ratio("ira_wd", "irakh", "irakh > 0"),
    "ira_rate_withdrawers": ratio("ira_wd", "irakh", "irakh > 0 and ira_wd > 0"),
    "ira_median_rate_withdrawers": median_of("r_ira", "irakh > 0 and ira_wd > 0"),
}

rows = []
for year in WD_WAVES:
    df = load(year)
    den, lag = CPI[year]
    df["ira_wd"] = df.ira_amt_raw * lag * 4376 / den
    df["r_any"] = 100 * df.penacctwd / df.retqliq.where(df.retqliq > 0)
    df["r_ira"] = 100 * df.ira_wd / df.irakh.where(df.irakh > 0)
    chk = (df.ira_wd <= df.penacctwd + 1).mean()  # IRA part should not exceed PENACCTWD
    print(year, "share of rows with IRA withdrawals <= PENACCTWD:", round(chk, 4), flush=True)
    rw = load_rw(year)
    groups = [("60+", df)] + [(b, g) for b, g in df.groupby("band", observed=True)]
    for band, g in groups:
        for name, fn in STATS.items():
            est, se = estimate(g, rw, fn)
            rows.append(dict(survey_year=year, ref_year=year - 1, age_band=band, stat=name, estimate=est, se=se))
res = pd.DataFrame(rows)
res.to_csv(OUT / "scf_rates_long.csv", index=False, float_format="%.4f")
w = res.pivot_table(index=["stat", "ref_year"], columns="age_band", values="estimate").round(2)
w.to_csv(OUT / "t14_withdrawal_rates_holders_vs_withdrawers.csv")
print(w.to_string())
