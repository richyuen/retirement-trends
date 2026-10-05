"""Decline of DB pensions: build percentage series from DOL Form 5500, BLS EBS/NCS and PBGC tables.

Inputs
  ../dc_stay/raw/hist.txt            DOL EBSA, Private Pension Plan Bulletin Historical Tables and Graphs 1975-2023
                                     (Sep 2025, v1.0), pdftotext of dc_stay/raw/private-pension-plan-bulletin-...pdf
  ../dc_stay/raw/abstracts/abs1999.txt  DOL Abstract of 1999 Form 5500 Annual Reports, Table E4 (1980-1999)
  raw/bls_ln_private_wage_salary.txt BLS CPS (LN) series LNU02032189, LNU02032184, LNU03032229 (monthly)
  raw/eb.*                           BLS Employee Benefits Survey (EB) database, download.bls.gov/pub/time.series/eb/
  raw/bls_nb_selected_series*.csv    BLS NCS (NB) database extract, download.bls.gov/pub/time.series/nb/
  raw/2023-pension-data-tables.xlsx  PBGC Pension Insurance Data Tables 2023 (S-22, S-23, S-26, S-27, M-6)
  raw/2024-pension-data-tables.xlsx  PBGC Pension Insurance Data Tables 2024 (S-3, S-20, S-21, M-4, M-5)
Outputs (output/): dol_form5500_db_dc.csv, dol_e4_1980_1999.csv, bls_ebs_ncs_db_dc.csv,
  bls_ncs_db_freeze.csv, pbgc_insured.csv, pbgc_freeze.csv
Run: python3 db_pensions/scripts/build_series.py
"""
import re
from pathlib import Path
import numpy as np, pandas as pd, openpyxl

HERE = Path(__file__).resolve().parents[1]
RAW, OUT = HERE / "raw", HERE / "output"
DC_RAW = HERE.parent / "dc_stay" / "raw"
OUT.mkdir(exist_ok=True)
num = lambda s: float(s.replace(",", ""))


# ---------- DOL Form 5500 historical tables ----------
def dol_table(lines, title):
    """First three numbers (Total, DB, DC; all plan types) of each year row of a historical table."""
    start = next(i for i, l in enumerate(lines) if re.match(rf"\s*Table {title}\s*$", l.rstrip()))
    rows = {}
    for l in lines[start + 1:]:
        if l.strip().startswith("NOTES"):
            break
        m = re.match(r"\s*(19[7-9]\d|20[0-2]\d)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", l)
        if m:
            rows[int(m.group(1))] = [num(m.group(k)) for k in (2, 3, 4)]
    return pd.DataFrame.from_dict(rows, orient="index", columns=["total", "db", "dc"])


hist = (DC_RAW / "hist.txt").read_text().splitlines()
e1 = dol_table(hist, r"E1\. Number of Pension Plans")
e4 = dol_table(hist, r"E4\. Number of Participants in Pension Plans")
e7 = dol_table(hist, r"E7\. Number of Active Participants in Pension Plans")
assert len(e1) == len(e4) == len(e7) == 49, (len(e1), len(e4), len(e7))
assert e7.loc[1980, "db"] == 30100 and e7.loc[2023, "db"] == 11077

# CPS private wage and salary workers (annual average of monthly, thousands), DOL's E&E-style definition:
# employed nonag private wage & salary + agricultural wage & salary + unemployed private nonag wage & salary
ln = pd.read_csv(RAW / "bls_ln_private_wage_salary.txt", sep=r"\s+", header=None, usecols=[0, 1, 2, 3],
                 names=["s", "y", "p", "v"], dtype=str)
ln = ln[ln.p != "M13"].assign(v=lambda d: pd.to_numeric(d.v, errors="coerce"), y=lambda d: d.y.astype(int))
lna = ln.groupby(["s", "y"]).v.mean().unstack(0)
denom = lna.LNU02032189 + lna.LNU02032184 + lna.LNU03032229

# DOL published Table E4 (Abstract of 1999 Form 5500), 1980-1999
abs99 = (DC_RAW / "abstracts" / "abs1999.txt").read_text().splitlines()
s = next(i for i, l in enumerate(abs99) if "Table E4. Estimated Private Wage and Salary Worker" in l)
e4p = {}
for l in abs99[s:s + 45]:
    m = re.match(r"\s*(19[89]\d)\s+([\d,]+)\s+([\d,]+)\s+(\d+)\s+([\d,]+)\s+(\d+)\s+([\d,]+)\s+(\d+)\s*$", l)
    if m:
        g = [num(x) for x in m.groups()]
        e4p[int(g[0])] = dict(ws_workers_k=g[1], db_only_k=g[2], db_only_pct=g[3], dc_only_k=g[4],
                              dc_only_pct=g[5], both_k=g[6], both_pct=g[7])
e4p = pd.DataFrame.from_dict(e4p, orient="index")
assert len(e4p) == 20
e4p["db_any_pct_computed"] = 100 * (e4p.db_only_k + e4p.both_k) / e4p.ws_workers_k
e4p["dc_any_pct_computed"] = 100 * (e4p.dc_only_k + e4p.both_k) / e4p.ws_workers_k
e4p.index.name = "year"
e4p.round(2).to_csv(OUT / "dol_e4_1980_1999.csv")

f = pd.DataFrame(index=e1.index.rename("year"))
f["plans_db"], f["plans_dc"], f["plans_total"] = e1.db, e1.dc, e1.total
f["pct_plans_db"] = 100 * e1.db / e1.total
f["participants_db_k"], f["participants_dc_k"] = e4.db, e4.dc
f["pct_participants_db"] = 100 * e4.db / e4.total
f["active_db_k"], f["active_dc_k"] = e7.db, e7.dc
f["pct_active_db"] = 100 * e7.db / e7.total
f["pct_db_participants_active"] = 100 * e7.db / e4.db
f["private_ws_workers_k_cps"] = denom.reindex(f.index).round(0)
f["active_db_pct_private_ws"] = 100 * e7.db / f.private_ws_workers_k_cps
f["active_dc_pct_private_ws"] = 100 * e7.dc / f.private_ws_workers_k_cps
f["dol_published_ws_workers_k"] = e4p.ws_workers_k.reindex(f.index)
f["dol_published_db_any_pct"] = e4p.db_any_pct_computed.reindex(f.index)
f.round(2).to_csv(OUT / "dol_form5500_db_dc.csv")

# ---------- BLS EBS (1979-2006) and NCS (2010-2026) ----------
eb = pd.read_csv(RAW / "eb.data.1.AllData", sep="\t", dtype=str)
eb.columns = eb.columns.str.strip()
eb = eb.apply(lambda c: c.str.strip())
keep = {"DBINC000000": "db_participation", "DCINC000000": "dc_participation", "ALLRET00000": "any_participation"}
eb["stat"] = eb.series_id.str[3:14].map(keep)
eb["scope"] = eb.series_id.str[14:16].map({"ML": "EBS private medium & large establishments",
                                            "SM": "EBS private small establishments (<100)",
                                            "SL": "EBS state & local government",
                                            "AP": "NCS/EBS all private industry (1999-2006)"})
eb = eb.dropna(subset=["stat", "scope"])
ebs = eb.assign(year=eb.year.astype(int), value=pd.to_numeric(eb.value)).pivot_table(
    index=["scope", "year"], columns="stat", values="value").reset_index()
ebs["source"] = "BLS EB database (download.bls.gov/pub/time.series/eb/), series EBU{DBINC000000|DCINC000000|ALLRET00000}{ML|SM|SL|AP}"

nb = pd.read_csv(RAW / "bls_nb_selected_series_data.csv", dtype=str)
nb["value"] = pd.to_numeric(nb.value, errors="coerce")
nb["year"] = nb.year.astype(int)
own = {"2": "NCS private industry", "3": "NCS state & local government", "1": "NCS civilian"}
code = {"290": "db_access", "291": "db_participation", "292": "db_takeup", "312": "dc_access",
        "313": "dc_participation", "314": "dc_takeup", "319": "any_access", "320": "any_participation",
        "321": "any_takeup"}
n1 = nb[nb.provision_code.isin(code)].assign(stat=lambda d: d.provision_code.map(code),
                                             scope=lambda d: d.ownership_code.map(own))
ncs = n1.pivot_table(index=["scope", "year"], columns="stat", values="value").reset_index()
ncs["source"] = "BLS NB database (download.bls.gov/pub/time.series/nb/), March reference; see raw/bls_nb_selected_series.csv for series ids"
both = pd.concat([ebs, ncs], ignore_index=True)
cols = ["scope", "year", "db_access", "db_participation", "db_takeup", "dc_access", "dc_participation",
        "dc_takeup", "any_access", "any_participation", "any_takeup", "source"]
both[cols].sort_values(["scope", "year"]).to_csv(OUT / "bls_ebs_ncs_db_dc.csv", index=False)

fz = {"298": "open_no_freeze", "387": "soft_frozen_all_accrue_closed", "388": "soft_frozen_some_accrue",
      "389": "hard_frozen", "299": "frozen_any_2010_13", "804": "open_to_new_employees",
      "805": "not_open_to_new_employees"}
n2 = nb[nb.provision_code.isin(fz) & nb.ownership_code.isin(["2", "3"])].assign(
    stat=lambda d: d.provision_code.map(fz), scope=lambda d: d.ownership_code.map(own))
frz = n2.pivot_table(index=["scope", "year"], columns="stat", values="value").reset_index()
frz.to_csv(OUT / "bls_ncs_db_freeze.csv", index=False)


# ---------- PBGC ----------
def sheet(path, name):
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)[name]
    return [[c for c in r] for r in ws.iter_rows(values_only=True)]


def year_rows(rows, ncol, start=0, stop=None):
    out = {}
    for r in rows[start:stop]:
        v = [c for c in r if c is not None]
        if v and re.fullmatch(r"(19|20)\d\d( 1)?", str(v[0]).strip()) and len(v) >= ncol + 1:
            out[int(str(v[0]).strip()[:4])] = [float(x) if not isinstance(x, str) else np.nan for x in v[1:ncol + 1]]
    return out


P23, P24 = RAW / "2023-pension-data-tables.xlsx", RAW / "2024-pension-data-tables.xlsx"
s20 = year_rows(sheet(P24, "S-20"), 1)
s21 = year_rows(sheet(P24, "S-21"), 1)
m4 = year_rows(sheet(P24, "M-4"), 1)
m5 = year_rows(sheet(P24, "M-5"), 1)
s22 = year_rows(sheet(P23, "S-22"), 3)
m6 = year_rows(sheet(P23, "M-6"), 3)
s23 = year_rows(sheet(P23, "S-23"), 4)
s3 = {}
for r in sheet(P24, "S-3"):
    v = [c for c in r if c is not None]
    if v and re.fullmatch(r"\d{4}", str(v[0]).strip()):
        s3[int(v[0])] = (v[1], v[2])
pb = pd.DataFrame(index=pd.Index(sorted(set(s20) | set(s23)), name="year"))
pb["se_insured_participants_k"] = pd.Series({k: v[0] for k, v in s20.items()})
pb["se_insured_plans"] = pd.Series({k: v[0] for k, v in s21.items()})
pb["me_insured_participants_k"] = pd.Series({k: v[0] for k, v in m4.items()})
pb["me_insured_plans"] = pd.Series({k: v[0] for k, v in m5.items()})
for nm, d in [("se", s22), ("me", m6)]:
    pb[f"{nm}_pct_active"] = pd.Series({k: 100 * v[0] for k, v in d.items()})
    pb[f"{nm}_pct_retired"] = pd.Series({k: 100 * v[1] for k, v in d.items()})
    pb[f"{nm}_pct_separated_vested"] = pd.Series({k: 100 * v[2] for k, v in d.items()})
pb["private_ws_workers_k_pbgc"] = pd.Series({k: v[0] for k, v in s23.items()})
pb["se_active_pct_private_ws"] = pd.Series({k: 100 * v[1] for k, v in s23.items()})
pb["me_active_pct_private_ws"] = pd.Series({k: 100 * v[2] for k, v in s23.items()})
pb["insured_active_pct_private_ws"] = pd.Series({k: 100 * v[3] for k, v in s23.items()})
pb["se_standard_terminations"] = pd.Series({k: v[0] for k, v in s3.items()})
pb["se_trusteed_terminations"] = pd.Series({k: v[1] for k, v in s3.items()})
pb["se_std_terminations_pct_of_insured_plans"] = 100 * pb.se_standard_terminations / pb.se_insured_plans
pb.round(2).to_csv(OUT / "pbgc_insured.csv")

r26 = sheet(P23, "S-26")
i = next(k for k, r in enumerate(r26) if r[0] == "Number of Plans")
n26 = pd.DataFrame(year_rows(r26, 7, i, i + 17)).T
n26.columns = ["hard_frozen", "accruals_continue_closed", "partial_freeze_closed", "partial_freeze_open",
               "any_freeze", "no_freeze", "total"]
r27 = sheet(P23, "S-27")
i = next(k for k, r in enumerate(r27) if r[0] and str(r[0]).startswith("Number of Active"))
n27 = pd.DataFrame(year_rows(r27, 8, i, i + 17)).T
n27.columns = ["hard_frozen", "partial_freeze_closed", "partial_freeze_open", "frozen_subtotal",
               "no_freeze_closed", "no_freeze_open", "no_freeze_subtotal", "total"]
fr = pd.DataFrame(index=n26.index.rename("year"))
for c in n26.columns[:-1]:
    fr["plans_pct_" + c] = 100 * n26[c] / n26.total
fr["plans_total"] = n26.total
for c in n27.columns[:-1]:
    fr["actives_pct_" + c] = 100 * n27[c] / n27.total
fr["actives_pct_closed_or_frozen"] = 100 * (n27.total - n27.no_freeze_open) / n27.total
fr["actives_total_k"] = n27.total
fr.round(2).to_csv(OUT / "pbgc_freeze.csv")

# ---------- summaries ----------
pd.set_option("display.width", 200)
print("DOL Form 5500 (all private plans):")
print(f.loc[[1975, 1980, 1990, 2000, 2010, 2023], ["pct_plans_db", "pct_participants_db", "pct_active_db",
                                                   "active_db_pct_private_ws", "active_dc_pct_private_ws",
                                                   "dol_published_db_any_pct"]].round(1).to_string())
print("max |own - DOL published| DB % of W&S workers 1980-99:",
      round((f.active_db_pct_private_ws - f.dol_published_db_any_pct).abs().max(), 2))
print("\nPBGC insured actives as % of private W&S workers:",
      pb.insured_active_pct_private_ws.dropna().iloc[[0, 5, 15, 25, -1]].round(1).to_dict())
print("PBGC single-employer insured plans:", pb.se_insured_plans.loc[[1980, 1985, 2000, 2025]].to_dict())
print("PBGC single-employer participants (k):", pb.se_insured_participants_k.loc[[1980, 2004, 2025]].to_dict())
print("PBGC SE actives in closed/frozen plans %:", fr.actives_pct_closed_or_frozen.round(1).to_dict())
print("\nBLS NCS private DB participation:", ncs[ncs.scope == "NCS private industry"].set_index("year").db_participation.to_dict())
print("BLS NCS state/local DB participation:", ncs[ncs.scope == "NCS state & local government"].set_index("year").db_participation.to_dict())
