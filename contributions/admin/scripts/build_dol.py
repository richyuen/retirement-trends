"""DOL Form 5500 contribution series (private-sector plans).

Inputs (read-only, from the dc_stay folder; dol.gov is 403 from this environment):
  ../../dc_stay/raw/hist.txt   pdftotext of DOL EBSA "Private Pension Plan Bulletin Historical Tables and
                               Graphs 1975-2023" (Sep 2025): Tables E7, E13, E19
  ../../dc_stay/raw/abstracts/absYYYY.txt  pdftotext of the annual "Private Pension Plan Bulletin: Abstract of
                               YYYY Form 5500 Annual Reports", 1999-2023: Table A4 (income statement by plan type)
                               and Table D8 (1999, 2002-2013) / D7 (2014-2023) (income statement of 401(k)-type plans)
  raw/bea/NipaDataA.txt        BEA NIPA annual flat file, series A132RC (wages & salaries, private industries)
  raw/bls/CUUR0000SA0.html     BLS CPI-U all items (data.bls.gov series report page)
Outputs (output/): dol_e13_contributions_by_type.csv, dol_dc_contrib_by_source.csv, dol_401k_contrib_by_source.csv
Run: python3 -I scripts/build_dol.py   (from contributions/admin/)
"""
import re
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
DC_RAW = HERE.parents[1] / "dc_stay" / "raw"
def num(s):
    s = s.replace(",", "").replace("$", "")
    neg = s.startswith("-") or s.startswith("(")
    return -float(s.strip("-()")) if neg else float(s)
HIST_SRC = ("DOL EBSA Private Pension Plan Bulletin Historical Tables and Graphs 1975-2023 (Sep 2025), "
            "https://www.dol.gov/sites/dolgov/files/ebsa/researchers/statistics/retirement-bulletins/"
            "private-pension-plan-bulletin-historical-tables-and-graphs.pdf")


# ---------- helpers shared with other scripts ----------
def cpi_annual():
    """CPI-U annual average = mean of available monthly values (2025 has no October value: lapse in appropriations)."""
    t = pd.read_html(HERE / "raw" / "bls" / "CUUR0000SA0.html")
    t = next(x for x in t if "Jan" in x.columns)
    t = t[pd.to_numeric(t.Year, errors="coerce").notna()].copy()
    t["Year"] = t.Year.astype(int)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    m = t.set_index("Year")[months].apply(pd.to_numeric, errors="coerce")
    a = m.mean(axis=1)[m.notna().sum(axis=1) >= 11]
    return a.round(3)


def bea_series(code):
    d = pd.read_csv(HERE / "raw" / "bea" / "NipaDataA.txt", dtype=str)
    d.columns = ["code", "year", "value"]
    s = d[d.code == code]
    return pd.Series(s.value.map(num).values, index=s.year.astype(int).values, name=code)


# ---------- historical tables ----------
hist = (DC_RAW / "hist.txt").read_text().splitlines()


def hist_table(title, ncol=3, allow_r=False):
    start = next(i for i, l in enumerate(hist) if re.match(rf"\s*Table {title}", l))
    rows = {}
    for l in hist[start + 1:]:
        if l.strip().startswith("NOTES"):
            break
        m = re.match(r"\s*(19[7-9]\d|20[0-2]\d)(r?)\s*\d?\s+" + r"\s+".join([r"\$?([\d,]+)"] * ncol), l)
        if m and (allow_r or not m.group(2)):
            rows[m.group(1) + m.group(2)] = [num(m.group(k)) for k in range(3, 3 + ncol)]
    return rows


e13 = pd.DataFrame.from_dict(hist_table(r"E13\. Pension Plan Contributions$"), orient="index",
                             columns=["contrib_total_m", "contrib_db_m", "contrib_dc_m"])
e13.index = e13.index.astype(int)
e7r = hist_table(r"E7\. Number of Active Participants in Pension Plans$", allow_r=True)
e7 = pd.DataFrame.from_dict({k: v for k, v in e7r.items() if not k.endswith("r")}, orient="index",
                            columns=["active_total_k", "active_db_k", "active_dc_k"])
e7.index = e7.index.astype(int)
e19r = hist_table(r"E19\. Number of 401\(k\)-Type Plans", ncol=5)
e19 = pd.DataFrame.from_dict(e19r, orient="index",
                             columns=["k401_plans", "k401_active_k", "k401_assets_m", "k401_contrib_m", "k401_benefits_m"])
e19.index = e19.index.astype(int)
assert len(e13) == 49 and e13.loc[2023, "contrib_dc_m"] == 767581 and e13.loc[1975, "contrib_db_m"] == 24242
assert e7.loc[2023, "active_dc_k"] > 80000 and len(e19) == 40 and e19.loc[2023, "k401_contrib_m"] == 677730

wages = bea_series("A132RC")  # wages & salaries, private industries ($ millions), NIPA Table 2.1 line 4
cpi = cpi_annual()
BASE = 2024
defl = cpi.loc[BASE] / cpi

f = e13.join(e7).join(e19[["k401_active_k", "k401_contrib_m"]])
f.index.name = "year"
f["pct_contrib_dc"] = 100 * f.contrib_dc_m / f.contrib_total_m
f["private_wages_m_bea"] = wages.reindex(f.index)
f["db_contrib_pct_private_wages"] = 100 * f.contrib_db_m / f.private_wages_m_bea
f["dc_contrib_pct_private_wages"] = 100 * f.contrib_dc_m / f.private_wages_m_bea
f["dc_contrib_per_active_nominal"] = 1000 * f.contrib_dc_m / f.active_dc_k
f["db_contrib_per_active_nominal"] = 1000 * f.contrib_db_m / f.active_db_k
f[f"dc_contrib_per_active_real{BASE}"] = f.dc_contrib_per_active_nominal * defl.reindex(f.index)
f[f"db_contrib_per_active_real{BASE}"] = f.db_contrib_per_active_nominal * defl.reindex(f.index)
f["source"] = ("Contributions: " + HIST_SRC + " Table E13; actives: Table E7; 401(k): Table E19; wages: BEA NIPA "
               "Table 2.1 line 4 (A132RC); CPI-U CUUR0000SA0 annual avg")
f["note"] = ("Contributions = employer + employee + other (incl. rollovers) + noncash, all plans excl. one-participant "
             "plans. Actives: 2005+ includes eligible non-contributors (2004 = old def; 2004r row in E7 = "
             f"{e7r['2004r'][2]:,.0f}k DC); 2009-2013 all 5500-SF participants counted active. Real = {BASE} dollars.")
f.round(3).to_csv(OUT / "dol_e13_contributions_by_type.csv")


# ---------- annual abstracts: contributions by source ----------
ROW = {"employer": r"Employer contributions", "participant": r"Participant contributions",
       "others_incl_rollovers": r"Contributions from others \(including rollovers\)", "noncash": r"Noncash contributions"}


def parse_income(lines, title_re, ncol):
    """Return {row: [values]} for the first income-statement table matching title_re."""
    hits = [i for i, l in enumerate(lines) if re.search(title_re, l, re.I)]
    for s in hits:
        out = {}
        for l in lines[s:s + 30]:
            for k, lab in ROW.items():
                m = re.match(r"\s*" + lab + r"\s+" + r"\s+".join([r"(-?\$?\(?[\d,]+\)?)"] * ncol) + r"\s*$", l, re.I)
                if m and k not in out:
                    out[k] = [num(m.group(j)) for j in range(1, ncol + 1)]
        if len(out) == 4:
            return out
    return None


recs, k401 = [], []
for y in range(1999, 2024):
    lines = (DC_RAW / "abstracts" / f"abs{y}.txt").read_text(errors="ignore").splitlines()
    a4 = parse_income(lines, r"TABLE A4\. Income Statement of Pension Plans", 3)
    assert a4, y
    for j, pt in enumerate(["total", "db", "dc"]):
        recs.append(dict(year=y, plan_type=pt, **{k: v[j] for k, v in a4.items()}))
    d = parse_income(lines, r"TABLE D[78]\. Income Statement of 401\(k\)", 4)
    if d:
        k401.append(dict(year=y, **{k: v[0] for k, v in d.items()}))

ab = pd.DataFrame(recs)
ab["contrib_total"] = ab[list(ROW)].sum(axis=1)
ab["employer_plus_participant"] = ab.employer + ab.participant
for k in ["employer", "participant", "others_incl_rollovers", "noncash"]:
    ab[f"pct_{k}_of_all_contrib"] = 100 * ab[k] / ab.contrib_total
ab["participant_share_excl_rollovers_pct"] = 100 * ab.participant / ab.employer_plus_participant
dc = ab[ab.plan_type == "dc"].set_index("year").drop(columns="plan_type")
db = ab[ab.plan_type == "db"].set_index("year")
dc["db_employer_m"] = db.employer
dc["hist_e13_dc_contrib_m"] = e13.contrib_dc_m.reindex(dc.index)
dc["abstract_vs_hist_pct_diff"] = 100 * (dc.contrib_total / dc.hist_e13_dc_contrib_m - 1)
dc["active_dc_k_hist_e7"] = e7.active_dc_k.reindex(dc.index)
dc["private_wages_m_bea"] = wages.reindex(dc.index)
dc["dc_employer_plus_participant_pct_private_wages"] = 100 * dc.employer_plus_participant / dc.private_wages_m_bea
dc["dc_employer_pct_private_wages"] = 100 * dc.employer / dc.private_wages_m_bea
dc["dc_participant_pct_private_wages"] = 100 * dc.participant / dc.private_wages_m_bea
dc["db_employer_pct_private_wages"] = 100 * dc.db_employer_m / dc.private_wages_m_bea
dc["dc_emp_plus_part_per_active_nominal"] = 1e3 * dc.employer_plus_participant / dc.active_dc_k_hist_e7
dc[f"dc_emp_plus_part_per_active_real{BASE}"] = dc.dc_emp_plus_part_per_active_nominal * defl.reindex(dc.index)
dc["dc_employer_per_active_nominal"] = 1e3 * dc.employer / dc.active_dc_k_hist_e7
dc["dc_participant_per_active_nominal"] = 1e3 * dc.participant / dc.active_dc_k_hist_e7
dc["source"] = ("DOL EBSA Private Pension Plan Bulletin, Abstract of YYYY Form 5500 Annual Reports, Table A4 (DC column); "
                "actives: Historical Tables E7; wages: BEA A132RC; CPI-U CUUR0000SA0")
dc["note"] = ("$ millions. Abstract vintages are not revised (hist tables are; e.g. DB/DC reclassification in 2015 "
              "release), so totals can differ from E13. 'others' includes rollovers from other plans/IRAs and is excluded "
              "from employer+participant. 1999 abstract = plan years beginning in 1999; later = ending in year. "
              "Actives definition widened 2005 (incl. eligible non-contributors); 2009-2013 5500-SF all participants "
              f"counted active. Real = {BASE} dollars.")
dc.round(3).to_csv(OUT / "dol_dc_contrib_by_source.csv")
ab.round(3).to_csv(OUT / "dol_a4_contrib_by_source_all_types.csv", index=False)

k = pd.DataFrame(k401).set_index("year")
k["contrib_total"] = k[list(ROW)].sum(axis=1)
k["employer_plus_participant"] = k.employer + k.participant
k["participant_share_excl_rollovers_pct"] = 100 * k.participant / k.employer_plus_participant
k["pct_others_incl_rollovers_of_all"] = 100 * k.others_incl_rollovers / k.contrib_total
k["hist_e19_contrib_m"] = e19.k401_contrib_m.reindex(k.index)
k["k401_active_k_hist_e19"] = e19.k401_active_k.reindex(k.index)
k["emp_plus_part_per_active_nominal"] = 1e3 * k.employer_plus_participant / k.k401_active_k_hist_e19
k[f"emp_plus_part_per_active_real{BASE}"] = k.emp_plus_part_per_active_nominal * defl.reindex(k.index)
k["source"] = ("DOL EBSA Abstract of YYYY Form 5500 Annual Reports, Table D8 (1999, 2002-2013) / D7 (2014-2023), "
               "'Total' column; actives: Historical Tables E19")
k["note"] = "$ millions; 2000-2001 abstracts have no 401(k) income statement. Same active-definition breaks as DC."
k.round(3).to_csv(OUT / "dol_401k_contrib_by_source.csv")

# ---------- summary ----------
print("E13 DC share of all contributions: 1975 %.1f%%, 1990 %.1f%%, 2000 %.1f%%, 2023 %.1f%%" %
      tuple(f.pct_contrib_dc.loc[[1975, 1990, 2000, 2023]]))
print("E13 DC contrib %% private wages: 1975 %.2f, 1990 %.2f, 2000 %.2f, 2023 %.2f" %
      tuple(f.dc_contrib_pct_private_wages.loc[[1975, 1990, 2000, 2023]]))
print("E13 DB contrib %% private wages: 1975 %.2f, 1990 %.2f, 2003 %.2f, 2023 %.2f" %
      tuple(f.db_contrib_pct_private_wages.loc[[1975, 1990, 2003, 2023]]))
cols = ["participant_share_excl_rollovers_pct", "pct_others_incl_rollovers_of_all_contrib", "dc_employer_plus_participant_pct_private_wages",
        "dc_emp_plus_part_per_active_nominal", f"dc_emp_plus_part_per_active_real{BASE}", "abstract_vs_hist_pct_diff"]
print(dc.loc[[1999, 2004, 2005, 2008, 2009, 2013, 2014, 2019, 2023], cols].round(1).to_string())
print("401(k):", k.loc[[1999, 2008, 2023], ["participant_share_excl_rollovers_pct", "pct_others_incl_rollovers_of_all",
                                            "emp_plus_part_per_active_nominal"]].round(1).to_string())
