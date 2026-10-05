"""Check our SCF estimates against the Fed's published SCF historical tables (2022 dollars), and
extract the Fed's debt-payment block (Table 18) by age, which we cite directly.
Input: raw/scf2022_tables_public_real_historical.xlsx
  https://www.federalreserve.gov/econres/files/scf2022_tables_public_real_historical.xlsx
Compares: Table 13 (any debt, home-secured debt on primary residence, credit-card balance, median debt),
Table 12 (leverage = aggregate debt/assets), Table 18 (debtors with payments > 40% of income),
Table 9 (owns primary residence) for ages 55-64, 65-74, 75+.
Output: output/fed_table18_payment_ratios_by_age.csv, output/check_vs_fed_tables.csv
"""
from pathlib import Path
import pandas as pd, openpyxl

HERE = Path(__file__).resolve().parents[1]
wb = openpyxl.load_workbook(HERE / "raw" / "scf2022_tables_public_real_historical.xlsx", read_only=True, data_only=True)
WAVES = [1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016, 2019, 2022]
AGEMAP = {"55–64": "55-64", "65–74": "65-74", "75 or more": "75+"}
ours = pd.read_csv(HERE / "output" / "scf_debt_housing_long.csv")


def age_rows(sheet, first_only=True):
    out = {}
    for r in wb[sheet].iter_rows(values_only=True):
        k = str(r[0]).strip() if r[0] else ""
        if k in AGEMAP and (AGEMAP[k] not in out or not first_only):
            out.setdefault(AGEMAP[k], []).append(list(r[1:]))
    return out


fed = []
# Table 12 leverage, Table 18 four blocks of 12 waves
for g, rr in age_rows("Table 12").items():
    for y, v in zip(WAVES, rr[0][:12]):
        fed.append(dict(year=y, group=g, stat="agg_debt_to_assets_pct", fed=v))
t18 = []
for g, rr in age_rows("Table 18").items():
    row = rr[0]
    for b, name in enumerate(["aggregate_payment_to_income_pct", "median_payment_to_income_debtors_pct",
                              "pct_debtors_payments_over_40pct", "pct_debtors_60days_late"]):
        for y, v in zip(WAVES, row[12 * b:12 * b + 12]):
            t18.append(dict(year=y, group=g, stat=name, value=v))
t18 = pd.DataFrame(t18)
t18.pivot_table(index="year", columns=["stat", "group"], values="value").round(1).to_csv(HERE / "output" / "fed_table18_payment_ratios_by_age.csv")
fed += [dict(year=r.year, group=r.group, stat="pct_pmt_over_40pct_income_debtors", fed=r.value)
        for r in t18[t18.stat == "pct_debtors_payments_over_40pct"].itertuples()]
# per-wave tables 13 and 9
for y in WAVES:
    yy = str(y)[2:]
    for g, rr in age_rows(f"Table 13 {yy} %s & medians", first_only=False).items():
        pct, med = rr[0], rr[1]
        fed += [dict(year=y, group=g, stat="pct_home_secured_debt", fed=pct[0]),
                dict(year=y, group=g, stat="pct_cc_balance", fed=pct[3]),
                dict(year=y, group=g, stat="pct_any_debt", fed=pct[6]),
                dict(year=y, group=g, stat="median_debt_if_any", fed=med[6] * 1000)]
    for g, rr in age_rows(f"Table 9 {yy} %s & medians", first_only=True).items():
        fed.append(dict(year=y, group=g, stat="pct_homeowner", fed=rr[0][1]))
fed = pd.DataFrame(fed)
m = fed.merge(ours, on=["year", "group", "stat"])
m["diff"] = m.value - m.fed
m["rel_diff_pct"] = 100 * m["diff"] / m.fed
m.round(3).to_csv(HERE / "output" / "check_vs_fed_tables.csv", index=False)
print(f"{len(m)} cells compared")
print(m.groupby("stat").apply(lambda d: pd.Series({"n": len(d), "max_abs_diff": d["diff"].abs().max(),
                                                    "max_abs_rel_pct": d.rel_diff_pct.abs().max()})).round(3).to_string())
print("Fed Table 18, 2022:")
print(t18[t18.year.isin([1989, 2022])].pivot_table(index=["stat"], columns=["group", "year"], values="value").round(1).to_string())
