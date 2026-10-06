"""Recordkeeper / industry context series (NOT administrative data): Vanguard How America Saves (HAS), federal TSP
(FRTIB participant behavior reports), Fidelity quarterly retirement analysis.

Inputs
  raw/vanguard/has2025.pdf  https://corporate.vanguard.com/content/dam/corp/research/pdf/how_america_saves_report_2025.pdf
  raw/vanguard/has2026.pdf  https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf
  ../../dc_policy/raw/autoenroll/FRTIB_*.pdf  (FRTIB participant behavior & demographics reports, on disk)
Method: pdftotext -layout; 'at a glance' rows (5 most recent years) are parsed by regex. Earlier years come from
  labelled bar charts (HAS 2025 Figures 24, 33, 46 cover 2015-2024; TSP 2017-2021 report Figures 1 and 3) and from
  report text; these are transcribed below with the figure/page cited and checked against overlapping parsed years.
Output: output/recordkeeper_contribution_rates.csv
Run: python3 -I scripts/build_recordkeeper.py
"""
import re, subprocess, tempfile
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
VG = HERE / "raw" / "vanguard"
TSP = HERE.parents[1] / "dc_policy" / "raw" / "autoenroll"
HAS25 = "Vanguard How America Saves 2025 (https://corporate.vanguard.com/content/dam/corp/research/pdf/how_america_saves_report_2025.pdf)"
HAS26 = "Vanguard How America Saves 2026 (https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf)"


def text(pdf):
    with tempfile.TemporaryDirectory() as d:
        o = Path(d) / "t.txt"
        subprocess.run(["pdftotext", "-layout", str(pdf), str(o)], check=True)
        return o.read_text(errors="ignore")


def glance(txt, label, years, pct=True):
    """Parse an 'at a glance' row: label ... Figure NN  v1 v2 v3 v4 v5."""
    m = re.search(re.escape(label) + r"\s+(?:Figure \d+\s+)?" + r"\s+".join([r"([\d.]+)%\*?"] * len(years)), txt)
    assert m, label
    return dict(zip(years, [float(x) for x in m.groups()]))


rows = []


def add(org, measure, vals, source, note, estimated=()):
    for y, v in vals.items():
        rows.append(dict(org=org, measure=measure, year=y, value_pct=v, estimated=y in estimated, source=source, note=note))


# ---- Vanguard ----
VNOTE = ("Vanguard recordkeeping clients (DC plans permitting employee-elective deferrals), participants only "
         "(excludes eligible non-participants) unless stated; year = calendar year of data; ")
t26 = text(VG / "has2026.pdf")
y26 = [2021, 2022, 2023, 2024, 2025]
for lab, meas in [("Average participant deferral rate", "avg_employee_deferral_rate"),
                  ("Median participant deferral rate", "median_employee_deferral_rate"),
                  ("Average total contribution rate (participant and employer)", "avg_total_contrib_rate_employee_plus_employer"),
                  ("Median total contribution rate (participant and employer)", "median_total_contrib_rate_employee_plus_employer"),
                  ("Plan-weighted participation rate", "plan_weighted_participation_rate"),
                  ("Participant-weighted participation rate", "participant_weighted_participation_rate"),
                  ("Percentage of participants increasing their deferral rate", "pct_participants_increasing_deferral")]:
    add("Vanguard HAS", meas, glance(t26, lab, y26), HAS26 + ", 'at a glance' table",
        VNOTE + "2025 value is Vanguard's estimate.", estimated=(2025,))
# 2015-2020 from HAS 2025 labelled charts (2021-2024 there agree with HAS 2026 except 2024 estimates revised)
t25 = text(VG / "has2025.pdf")
chk = glance(t25, "Average participant deferral rate", [2020, 2021, 2022, 2023, 2024])
assert chk[2020] == 7.3 and chk[2021] == 7.4
fig = {"avg_employee_deferral_rate": {2015: 6.9, 2016: 6.8, 2017: 7.0, 2018: 7.0, 2019: 7.1, 2020: 7.3},
       "median_employee_deferral_rate": {2015: 6.0, 2016: 6.0, 2017: 6.0, 2018: 6.0, 2019: 6.0, 2020: 6.1},
       "avg_total_contrib_rate_employee_plus_employer": {2015: 10.8, 2016: 10.4, 2017: 10.8, 2018: 10.7, 2019: 11.3, 2020: 11.3},
       "median_total_contrib_rate_employee_plus_employer": {2015: 10.0, 2016: 9.7, 2017: 10.0, 2018: 9.9, 2019: 10.5, 2020: 10.5},
       "plan_weighted_participation_rate": {2015: 81, 2016: 81, 2017: 81, 2018: 82, 2019: 83, 2020: 85},
       "participant_weighted_participation_rate": {2015: 78, 2016: 71, 2017: 72, 2018: 77, 2019: 78, 2020: 81}}
figref = {"avg_employee_deferral_rate": 33, "median_employee_deferral_rate": 33, "avg_total_contrib_rate_employee_plus_employer": 46,
          "median_total_contrib_rate_employee_plus_employer": 46, "plan_weighted_participation_rate": 24,
          "participant_weighted_participation_rate": 24}
for meas, vals in fig.items():
    add("Vanguard HAS", meas, vals, HAS25 + f", Figure {figref[meas]} (bar labels)",
        VNOTE + "2016 dip in total contribution/participation reflects a change in Vanguard's client mix (HAS text).")
# eligible-employee basis (includes non-participants at 0%) -- 2024 from HAS 2025 text p.44
m = re.search(r"aggregate contribution rate was ([\d.]+)%;\s+the\s+.*?median rate, ([\d.]+)%", t25, re.S)
add("Vanguard HAS", "avg_total_contrib_rate_all_eligible_incl_nonparticipants", {2024: float(m.group(1))},
    HAS25 + ", p.44 text / Figure 47", VNOTE + "includes eligible non-participants at 0%; 2024 estimated.", estimated=(2024,))

# ---- TSP (FERS participants) ----
TNOTE = ("Federal TSP, FERS civilian participants; deferral rate = annualized employee contributions (traditional+Roth+"
         "catch-up) / estimated salary (FRTIB approximation); excludes 1% agency automatic + match (up to 5% of pay "
         "total employer). Auto-enrollment default 3% (Aug 2010), 5% (Oct 2020). Report methods differ across editions.")
t21_25 = text(TSP / "FRTIB_TSP-Annual-Report_2025_participant_behavior_2021-2025.pdf")
t19_23 = text(TSP / "FRTIB_Participant-Behavior-and-Demographics-2019-2023.pdf")
for lab, meas in [("FERS Deferral Rate", "avg_employee_deferral_rate"), ("FERS Participation Rate", "participation_rate"),
                  ("FERS Traditional Deferral Rate", "avg_traditional_deferral_rate"), ("FERS Roth Deferral Rate", "avg_roth_deferral_rate")]:
    v25 = glance(t21_25, lab, y26)
    v23 = glance(t19_23, lab, [2019, 2020, 2021, 2022, 2023])
    assert all(v23[y] == v25[y] for y in (2021, 2022, 2023)), lab
    add("Federal TSP (FRTIB)", meas, v25, "FRTIB TSP Annual Report 2025, Participant Behavior 2021-2025, Highlights at a Glance "
        "(file dc_policy/raw/autoenroll/FRTIB_TSP-Annual-Report_2025_participant_behavior_2021-2025.pdf)", TNOTE)
    add("Federal TSP (FRTIB)", meas, {y: v23[y] for y in (2019, 2020)}, "FRTIB Participant Behavior and Demographics "
        "2019-2023, Highlights at a Glance", TNOTE)
add("Federal TSP (FRTIB)", "avg_employee_deferral_rate", {2017: 7.9, 2018: 7.9},
    "FRTIB Participant Behavior and Demographics 2017-2021, Figure 3 (bar labels)", TNOTE)
add("Federal TSP (FRTIB)", "participation_rate", {2017: 92.6, 2018: 93.3},
    "FRTIB Participant Behavior and Demographics 2017-2021, Figure 1 (bar labels)", TNOTE)
add("Federal TSP (FRTIB)", "avg_employee_deferral_rate", {2014: 8.1},
    "FRTIB Participant Behavior and Demographics 2014, p.7 text ('dropping slightly to 8.1% in 2014'; "
    "mid-2000s ~9.5%)", TNOTE)
add("Federal TSP (FRTIB)", "participation_rate", {2014: 89.9}, "FRTIB Participant Behavior and Demographics 2014, p.4 text", TNOTE)
add("Federal TSP (FRTIB)", "avg_employee_deferral_rate", {2012: 8.5},
    "FRTIB Participant Behavior and Demographics 2012, p.5 text ('rose to 8.5% in 2012')", TNOTE)
add("Federal TSP (FRTIB)", "participation_rate", {2012: 88.6}, "FRTIB Participant Behavior and Demographics 2012, p.4 text", TNOTE)

# ---- Fidelity (single data point; quarterly press release) ----
add("Fidelity", "avg_employee_deferral_rate", {2026: 9.6}, "Fidelity Q2 2026 Retirement Analysis, "
    "https://about.fidelity.com/data-and-insights/q2-2026-retirement-analysis", "Q2 2026; Fidelity 401(k) recordkeeping "
    "participants; employee rate record high")
add("Fidelity", "avg_employer_contrib_rate", {2026: 4.8}, "Fidelity Q2 2026 Retirement Analysis (same URL)", "Q2 2026")
add("Fidelity", "avg_total_contrib_rate_employee_plus_employer", {2026: 14.4}, "Fidelity Q2 2026 Retirement Analysis "
    "(same URL)", "Q2 2026; also 14.4% in Q1 2026")

d = pd.DataFrame(rows).sort_values(["org", "measure", "year"])
d.to_csv(OUT / "recordkeeper_contribution_rates.csv", index=False)
p = d.pivot_table(index="year", columns=["org", "measure"], values="value_pct")
for c in [("Vanguard HAS", "avg_employee_deferral_rate"), ("Vanguard HAS", "avg_total_contrib_rate_employee_plus_employer"),
          ("Federal TSP (FRTIB)", "avg_employee_deferral_rate"), ("Federal TSP (FRTIB)", "participation_rate")]:
    print(c, p[c].dropna().to_dict())
