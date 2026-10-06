"""BEA NIPA employer contributions to DC and DB pension plans as % of wages and salaries.

Input: raw/bea/NipaDataA.txt and raw/bea/SeriesRegister.txt, downloaded from
  https://apps.bea.gov/national/Release/TXT/NipaDataA.txt  (annual values, $ millions)
  https://apps.bea.gov/national/Release/TXT/SeriesRegister.txt
Series (table:line from SeriesRegister):
  A132RC  Wages and salaries, private industries          T2.1 line 4      1929-
  B202RC  Wages and salaries, government                  T2.1 line 5      1929-
  B4921C  Employer contributions, private pension plans    T7.8 line 11 / T6.11D line 24   1948-
  Y934RC  Actual employer contributions to DC plans: private plans        T7.25 line 6   1984-
  W351RC  Employer contributions, private DC plans         T6.11D line 26   1998- (= Y934RC)
  W350RC  Actual employer contributions, private DB plans  T7.22 line 5     1984-
  Y240RC  Imputed employer contributions, private DB plans T7.22 line 6     1984-
  Y696RC  Employer contributions, private DB (actual+imputed) T6.11D line 25 1998-
  Y344RC  Actual household (employee) contributions, all DC plans (private+federal TSP+S&L) T7.25 line 9  1984-
  Y912RC / Y955RC  Actual employer contributions, federal / state & local government DC plans, T7.25 lines 7-8
  S25110  Actual employer contributions, state & local DB plans, T7.24 line 5
  Y239RC  Employer contributions, state & local pension plans (all, accrual basis), T7.8 line 10  1948-
  A4182C  Wages and salaries, state and local government, T6.3D line 92  1998-
Output: output/bea_nipa_pension_contrib.csv (wide, one row per year) and bea_nipa_pension_contrib_long.csv
Run: python3 -I scripts/build_bea.py
"""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parents[1]
RAW, OUT = HERE / "raw" / "bea", HERE / "output"
d = pd.read_csv(RAW / "NipaDataA.txt", dtype=str)
d.columns = ["code", "year", "value"]
d["value"] = pd.to_numeric(d.value.str.replace(",", ""), errors="coerce")
d["year"] = d.year.astype(int)
codes = ["A132RC", "B202RC", "A034RC", "B4921C", "Y934RC", "W351RC", "W350RC", "Y240RC", "Y696RC", "Y344RC",
         "Y340RC", "Y912RC", "Y955RC", "S25110", "Y239RC", "A4182C"]
w = d[d.code.isin(codes)].pivot(index="year", columns="code", values="value")
w = w[w.index >= 1948]
assert (w.loc[1998:, "W351RC"] == w.loc[1998:, "Y934RC"]).all()

f = pd.DataFrame(index=w.index.rename("year"))
pw = w.A132RC
f["private_wages_m"] = pw
f["priv_pension_employer_pct_priv_wages"] = 100 * w.B4921C / pw
f["priv_dc_employer_pct_priv_wages"] = 100 * w.Y934RC / pw
f["priv_db_employer_actual_pct_priv_wages"] = 100 * w.W350RC / pw
f["priv_db_employer_actual_plus_imputed_pct_priv_wages"] = 100 * (w.W350RC + w.Y240RC) / pw
f["dc_share_of_priv_employer_actual_contrib_pct"] = 100 * w.Y934RC / (w.Y934RC + w.W350RC)
f["dc_household_contrib_all_sectors_pct_total_wages"] = 100 * w.Y344RC / w.A034RC
f["dc_employer_all_sectors_pct_total_wages"] = 100 * w.Y340RC / w.A034RC
f["dc_employee_share_all_sectors_pct"] = 100 * w.Y344RC / (w.Y344RC + w.Y340RC)
f["sl_db_employer_actual_pct_sl_wages"] = 100 * w.S25110 / w.A4182C
f["sl_dc_employer_pct_sl_wages"] = 100 * w.Y955RC / w.A4182C
f = f.join(w.rename(columns=lambda c: f"{c}_m"))
f["source"] = ("BEA NIPA flat file https://apps.bea.gov/national/Release/TXT/NipaDataA.txt (Tables 2.1, 6.11D, 7.8, "
               "7.22, 7.24, 7.25); downloaded 2026-10-06")
f["note"] = ("$ millions. Private DB 'actual' = cash employer contributions (W350RC, matches Form 5500 DB employer "
             "contributions); 'imputed' = accrual-basis normal cost minus actual (can be negative; NIPA since 2013 "
             "comprehensive revision). B4921C = DC + DB(actual+imputed). DC/DB split only from 1984 (T7.22/7.25); B4921C (DB+DC) from 1948. "
             "Household DC contributions cover private + federal TSP + state/local DC plans.")
f.round(3).to_csv(OUT / "bea_nipa_pension_contrib.csv")

long = w.stack().rename("value_m").reset_index().rename(columns={"code": "series"})
long["source"] = "BEA NipaDataA.txt"
long.to_csv(OUT / "bea_nipa_pension_contrib_long.csv", index=False)

yrs = [1950, 1960, 1970, 1980, 1984, 1990, 2000, 2008, 2015, 2020, 2024, 2025]
print(f.loc[[y for y in yrs if y in f.index], ["priv_pension_employer_pct_priv_wages", "priv_dc_employer_pct_priv_wages",
      "priv_db_employer_actual_pct_priv_wages", "priv_db_employer_actual_plus_imputed_pct_priv_wages",
      "dc_share_of_priv_employer_actual_contrib_pct", "dc_employee_share_all_sectors_pct"]].round(2).to_string())
