"""Published series typed in from source documents saved in readiness/raw/ (each row cites its file).
python3 readiness/scripts/build_published.py"""
from pathlib import Path
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "output"

# CRR National Retirement Risk Index: share of working-age households (30-59) "at risk".
# Three vintages; methods differ, so do not splice.
nrri = []
for y, v in zip([1983, 1986, 1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016],
                [31, 31, 30, 37, 38, 40, 38, 45, 44, 53, 52, 50]):
    nrri.append(("original (IB 18-1, Jan 2018)", y, v, "raw/crr/IB_18-1.pdf Fig 2"))
for y, v in zip([2004, 2007, 2010, 2013, 2016, 2019], [41, 40, 51, 51, 50, 49]):
    nrri.append(("revised (IB 21-2, Jan 2021)", y, v, "raw/crr/IB_21-2.pdf Fig 2"))
for y, v in zip([2004, 2007, 2010, 2013, 2016, 2019, 2022], [42, 41, 51, 51, 48, 47, 39]):
    nrri.append(("Version 2.0 w/ varying claiming ages (IB 24-5, Feb 2024)", y, v, "raw/crr/IB_24-5.pdf Fig 2"))
pd.DataFrame(nrri, columns=["vintage", "scf_year", "pct_at_risk", "source"]).to_csv(OUT / "p1_crr_nrri.csv", index=False)

# NRRI 2019 vs 2022 by subgroup (IB 24-5 Tables 1-4)
sub = [("homeownership", "renter", 74, 72), ("homeownership", "homeowner", 34, 24),
       ("plan", "defined benefit (incl. DB+DC)", 21, 13), ("plan", "DC only", 42, 35), ("plan", "none", 68, 65),
       ("income", "low third", 71, 64), ("income", "middle third", 38, 29), ("income", "high third", 32, 23),
       ("age", "30-39", 48, 40), ("age", "40-49", 46, 41), ("age", "50-59", 48, 36), ("all", "all", 47, 39)]
pd.DataFrame(sub, columns=["dimension", "group", "pct_at_risk_2019", "pct_at_risk_2022"]).assign(
    source="raw/crr/IB_24-5.pdf Tables 1-4").to_csv(OUT / "p2_crr_nrri_subgroups.csv", index=False)

# EBRI/Greenwald RCS: workers "very or somewhat confident" of enough money to live comfortably in retirement.
# 1993-2011 = very + somewhat bar labels in the 2011 fact sheet (sum of rounded parts, +/-1);
# later years = headline text of each year's Fact Sheet #1, except 2012-2014 (bar labels summed).
rcs = [(1993, 18, 73, "rcs11 fig1 (2026 fact sheet chart shows 74)"), (1996, 19, 60, "rcs11 fig1"),
       (2001, 22, 63, "rcs11 fig1"), (2002, 23, 70, "rcs11 fig1"), (2003, 21, 66, "rcs11 fig1"),
       (2004, 24, 68, "rcs11 fig1"), (2005, 25, 65, "rcs11 fig1"), (2006, 24, 68, "rcs11 fig1"),
       (2007, 27, 70, "rcs11 fig1"), (2008, 18, 61, "rcs11 fig1"), (2009, 13, 54, "rcs11 fig1"),
       (2010, 16, 54, "rcs11 fig1"), (2011, 13, 49, "rcs11 fig1"), (2012, 14, 52, "rcs12 text+fig1"),
       (2013, 13, 51, "rcs13 text"), (2014, 18, 55, "rcs14 fig1"), (2015, 22, 59, "rcs17 text"),
       (2016, 21, 64, "rcs17 text"), (2017, 18, 60, "rcs17 text"), (2018, 17, 64, "rcs18 text"),
       (2019, 23, 67, "rcs19 text"), (2020, 27, 69, "rcs20 text"), (2021, 29, 72, "rcs21 text"),
       (2022, 28, 73, "rcs22 text"), (2023, 18, 64, "rcs23 text"), (2024, 21, 68, "rcs24 text"),
       (2025, 24, 67, "rcs25 text"), (2026, 21, 61, "rcs26 text")]
pd.DataFrame(rcs, columns=["survey_year", "workers_very_confident_pct", "workers_very_or_somewhat_pct", "source"]
             ).to_csv(OUT / "p3_ebri_rcs_worker_confidence.csv", index=False)

# Fed SHED: non-retirees who think their retirement saving plan is on track (2025 report, Figure 26)
shed = list(zip(range(2017, 2026), [38, 36, 37, 36, 40, 31, 34, 35, 35]))
pd.DataFrame(shed, columns=["survey_year", "pct_on_track"]).assign(
    source="raw/fed/shed_2025_report.pdf Figure 26").to_csv(OUT / "p4_fed_shed_on_track.csv", index=False)

print("NRRI v2.0:", dict((r[1], r[2]) for r in nrri if r[0].startswith("Version")))
print("RCS workers confident:", {r[0]: r[2] for r in rcs})
print("SHED on track:", dict(shed))
