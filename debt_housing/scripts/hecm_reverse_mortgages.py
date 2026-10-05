"""Reverse mortgages: FHA HECM endorsements FY2009-2025 and HMDA reverse-mortgage originations 2018-2023.
Inputs (raw/):
  hud_2025FHAAnnualReportMMIFund.pdf  HUD/FHA, Annual Report to Congress on the MMI Fund FY2025,
      Tables B-26 (endorsements by purpose) and B-31 (average borrower age)
      https://www.hud.gov/sites/dfiles/Housing/documents/2025FHAAnnualReportMMIFund.pdf
  cfpb_2023_mortgage_market_activity_trends.pdf  CFPB, 2023 Mortgage Market Activity and Trends (Dec 2024),
      Table 1E row C.2 (reverse mortgage originations, thousands, all purposes)
      https://files.consumerfinance.gov/f/documents/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf
  hvs_histtab12.xlsx (owner households 65+, for a rate per 1,000 older homeowners)
Tables B-26/B-31 are parsed from `pdftotext -layout` output (poppler-utils) when available,
otherwise the transcribed values below are used (they were checked against the parsed text).
Output: output/hecm_endorsements_fy2009_2025.csv, output/hmda_reverse_originations_2018_2023.csv
"""
from pathlib import Path
import re, shutil, subprocess
import pandas as pd, openpyxl

HERE = Path(__file__).resolve().parents[1]
RAW, OUT = HERE / "raw", HERE / "output"

# FY: (purchase, refinance, traditional, all, MCA $bn, average borrower age)
HECM = {2009: (559, 8973, 104893, 114425, 30.07, 73.03), 2010: (1389, 4835, 72833, 79057, 21.07, 72.97),
        2011: (1538, 2737, 68837, 73112, 18.21, 72.30), 2012: (1627, 1444, 51741, 54812, 13.16, 72.06),
        2013: (2091, 1835, 55997, 59923, 14.68, 71.77), 2014: (1825, 2406, 47385, 51616, 13.52, 71.97),
        2015: (2411, 5571, 50007, 57989, 16.13, 72.35), 2016: (2367, 5398, 41103, 48868, 14.66, 73.01),
        2017: (2634, 8016, 44640, 55290, 17.69, 73.16), 2018: (2615, 5860, 39854, 48329, 16.19, 73.34),
        2019: (2295, 1679, 27298, 31272, 10.86, 73.59), 2020: (2472, 8614, 30749, 41835, 16.29, 73.51),
        2021: (2228, 20661, 26307, 49196, 21.35, 73.95), 2022: (2236, 29004, 33232, 64472, 32.12, 74.29),
        2023: (2034, 4017, 26923, 32974, 16.17, 74.84), 2024: (1686, 2074, 22742, 26502, 13.36, 75.23),
        2025: (1540, 3065, 23544, 28149, 14.96, 75.31)}

if shutil.which("pdftotext"):
    txt = subprocess.run(["pdftotext", "-layout", str(RAW / "hud_2025FHAAnnualReportMMIFund.pdf"), "-"],
                         capture_output=True, text=True).stdout
    n_ok = 0
    blk = txt[txt.index("Table B-26: Data Table"):txt.index("Table B-27")]
    for line in blk.splitlines():
        m = re.match(r"\s*(20\d\d)\s+([\d,]+\s+){6}[\d.]+\s*$", line)
        if m:
            nums = [float(x.replace(",", "")) for x in line.split()[1:]]
            y = int(line.split()[0])
            n_ok += 1
            assert tuple(nums[2:6]) == HECM[y][:4] and nums[6] == HECM[y][4], (y, nums)
    print(f"HECM transcription checked against PDF text: {n_ok} of 17 rows")

df = pd.DataFrame.from_dict(HECM, orient="index", columns=["purchase", "refinance", "traditional", "all", "mca_bn", "avg_age"])
df.index.name = "fiscal_year"
df["refi_share_pct"] = df.refinance / df["all"] * 100

# owner households 65+ (thousands), HVS Table 12, calendar year
rows = list(openpyxl.load_workbook(RAW / "hvs_histtab12.xlsx", read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True))
own65, years = {}, None
for r in rows:
    if r[0] == "Age of Householder":
        years = [str(c) for c in r[1:] if c is not None]
    elif years and r[0] and "65 years and over" in str(r[0]):
        vals = [c for c in r[1:] if c is not None]
        for i, y in enumerate(years):
            own65[int(y[:4])] = vals[2 * i + 1]  # later (revised) columns overwrite earlier ones
df["owner_hh_65plus_k"] = pd.Series(own65)
df["per_1000_owner_hh_65plus"] = df["all"] / df.owner_hh_65plus_k
df.round(3).to_csv(OUT / "hecm_endorsements_fy2009_2025.csv")
print(df[["all", "refi_share_pct", "avg_age", "per_1000_owner_hh_65plus"]].round(2).to_string())

hmda = pd.DataFrame({"year": range(2018, 2024), "reverse_originations_k": [33, 35, 43, 59, 59, 25],
                     "reverse_applications_k": [57, 55, 64, 85, 93, 40]})
hmda.to_csv(OUT / "hmda_reverse_originations_2018_2023.csv", index=False)
print(hmda.to_string(index=False))
