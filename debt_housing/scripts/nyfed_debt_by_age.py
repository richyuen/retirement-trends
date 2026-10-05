"""NY Fed Household Debt and Credit Report (2026Q2 data file): debt by borrower age.
Input: raw/HHD_C_Report_2026Q2.xlsx from
https://www.newyorkfed.org/medialibrary/interactives/householdcredit/data/xls/HHD_C_Report_2026Q2.xlsx
Page 20 = total debt balance by age (trillions $, 1999Q1-), Page 21 = product x age (2026Q2),
Page 3 = total debt balance (for comparison with the sum of age groups),
Page 23 = mortgage originations by age, Page 29 = new foreclosures by age.
Shares use the sum of the six age groups as denominator (unknown birth years excluded).
Output: output/nyfed_debt_share_by_age_quarterly.csv, nyfed_debt_share_by_age_annual_q4.csv,
        nyfed_product_by_age_2026q2.csv, nyfed_mortgage_orig_share_by_age_annual.csv
"""
from pathlib import Path
import pandas as pd, openpyxl

HERE = Path(__file__).resolve().parents[1]
wb = openpyxl.load_workbook(HERE / "raw" / "HHD_C_Report_2026Q2.xlsx", read_only=True, data_only=True)
AGES = ["18-29", "30-39", "40-49", "50-59", "60-69", "70+"]


def series(sheet):
    rows = [r for r in wb[sheet].iter_rows(values_only=True)]
    out = []
    for r in rows:
        r = [c for c in r if c is not None]
        if r and isinstance(r[0], str) and ":Q" in r[0] and len(r) >= 7:
            yy, q = r[0].split(":Q")
            out.append([2000 + int(yy) if int(yy) < 90 else 1900 + int(yy), int(q)] + list(r[1:7]))
    return pd.DataFrame(out, columns=["year", "q"] + AGES)


def shares(df):
    s = df[AGES].div(df[AGES].sum(axis=1), axis=0) * 100
    s.insert(0, "q", df.q); s.insert(0, "year", df.year)
    s["60+"] = s["60-69"] + s["70+"]
    s["total_trn_age_sum"] = df[AGES].sum(axis=1)
    return s


bal = series("Page 20 Data")
sh = shares(bal)
sh.round(2).to_csv(HERE / "output" / "nyfed_debt_share_by_age_quarterly.csv", index=False)
q4 = sh[sh.q == 4].drop(columns="q")
last = sh.iloc[[-1]].drop(columns="q").assign(year=lambda d: d.year.astype(str) + "Q" + str(sh.q.iloc[-1]))
pd.concat([q4.assign(year=q4.year.astype(str) + "Q4"), last]).round(2).to_csv(
    HERE / "output" / "nyfed_debt_share_by_age_annual_q4.csv", index=False)
print("Share of total debt by borrower age (%), Q4 values:")
print(pd.concat([q4, last]).set_index("year")[["50-59", "60-69", "70+", "60+", "total_trn_age_sum"]].iloc[::3].round(1).to_string())
print(last[["year", "60-69", "70+", "60+", "total_trn_age_sum"]].round(2).to_string(index=False))

# balances in trillions for 60-69 and 70+
b = bal.assign(**{"60+": bal["60-69"] + bal["70+"]})
print("Balances, $T:", b[(b.q == 1) & (b.year == 1999)][["60-69", "70+", "60+"]].values, b.iloc[-1][["60-69", "70+", "60+"]].values)

# product x age, 2026Q2
rows = [[c for c in r if c is not None] for r in wb["Page 21 Data"].iter_rows(values_only=True)]
prod = pd.DataFrame([r[:7] for r in rows if r and r[0] in ("Auto Loans", "Credit Card", "Mortgage", "HELOC", "Student Loans")],
                    columns=["product"] + AGES).set_index("product")
prod.loc["Sum of products"] = prod.sum()
pct_of_product = prod.div(prod.sum(axis=1), axis=0) * 100
mix = prod.div(prod.loc["Sum of products"], axis=1) * 100
out = pd.concat({"trillions": prod, "pct_of_product_across_ages": pct_of_product, "pct_of_age_group_debt": mix}, names=["measure"])
out.round(3).to_csv(HERE / "output" / "nyfed_product_by_age_2026q2.csv")
print("2026Q2 share of each product held by 60-69 / 70+ (%):")
print(pct_of_product[["60-69", "70+"]].round(1).to_string())
print("Mortgage+HELOC share of each age group's (listed-product) debt (%):")
print((mix.loc["Mortgage"] + mix.loc["HELOC"]).round(1).to_string())

# mortgage originations by age, annual sums
orig = series("Page 23 Data")
oa = orig.groupby("year")[AGES].sum()
oa = oa[orig.groupby("year").size() == 4]
osh = oa.div(oa.sum(axis=1), axis=0) * 100
osh["60+"] = osh["60-69"] + osh["70+"]
osh.round(2).to_csv(HERE / "output" / "nyfed_mortgage_orig_share_by_age_annual.csv")
print("Mortgage origination $ share 60+ (%):", osh["60+"].round(1).iloc[[0, 5, 10, 15, 20, -1]].to_dict())
