"""SCF 1989-2022: DB pension coverage of households by age of the reference person.

Complements spending/scf_income (t6_db_vs_dc_coverage.csv), which already gives, for 55-64 / 65+ / 65-74 / 75+:
receiving a pension now, DB from current or past job, DB-only / DC-only splits. This script adds the
working-age view: DB on a CURRENT job (head or spouse/partner), by age band, for all households and for
"employee households" (reference person works for someone else, Fed OCCAT1=1).

Fed summary-extract variables (scf/raw/rscfpYYYY.dta; definitions in scf/raw/bulletin.macro.txt):
  DBPLANCJ  1 = R or spouse/partner has a defined-benefit pension on a current job
  DCPLANCJ  1 = R or spouse/partner has an account-type (DC) plan on a current job
  BPLANCJ   1 = both types on a current job
  DBPLANT   1 = DB on current job OR a pension from a past job to be received in the future
  OCCAT1    1 = reference person works for someone else
Point estimates pool the 5 implicates (WGT already /5). SEs: 999 bootstrap replicate weights (wt1bK*mmK) on
implicate 1 plus (1+1/5) x between-implicate variance (same method as scf/ and spending/scf_income/).
Replicate files: 2004+ in scf/raw/; 1989-2001 downloaded from federalreserve.gov to $SCF_OLD_DIR (default /tmp/scf_old).
Run: python3 db_pensions/scripts/scf_db_coverage.py   -> db_pensions/output/scf_db_coverage_long.csv
"""
import os, urllib.request, zipfile
from pathlib import Path
import numpy as np, pandas as pd, pyreadstat

HERE = Path(__file__).resolve().parents[1]
SCF = HERE.parent / "scf" / "raw"
OUT = HERE / "output"
OLD = Path(os.environ.get("SCF_OLD_DIR", "/tmp/scf_old"))
WAVES = [1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016, 2019, 2022]
OLD_RW = {1989: ("scf89rw1s", "p89_rw1.dta"), 1992: ("scf92rw1s", "p92_rw1.dta"),
          1995: ("scf95rw1s", "p95_rw1.dta"), 1998: ("scf98rw1s", "p98_rw1.dta"),
          2001: ("scf2001rw1s", "scf2001rw1s.dta")}
GROUPS = {"all": "age >= 0", "<35": "age < 35", "35-44": "35 <= age <= 44", "45-54": "45 <= age <= 54",
          "55-64": "55 <= age <= 64", "65+": "age >= 65"}
EMP = "occat1 == 1"
STATS = {  # name: (numerator flag, extra denominator condition)
    "pct_db_current_job": ("dbplancj == 1", None),
    "pct_dc_current_job": ("dcplancj == 1", None),
    "pct_db_only_current_job": ("dbplancj == 1 and dcplancj != 1", None),
    "pct_dc_only_current_job": ("dcplancj == 1 and dbplancj != 1", None),
    "pct_db_cj_or_past_job_future": ("dbplant == 1", None),
}


def read(path, cols):
    _, meta = pyreadstat.read_dta(str(path), metadataonly=True)
    names = {c.lower(): c for c in meta.column_names}
    df, _ = pyreadstat.read_dta(str(path), usecols=[names[c] for c in cols if c in names])
    df.columns = df.columns.str.lower()
    return df


def rw_path(year):
    if year >= 2004:
        return SCF / f"p{str(year)[2:]}_rw1.dta"
    z, f = OLD_RW[year]
    p = OLD / f
    if not p.exists():
        OLD.mkdir(parents=True, exist_ok=True)
        zp = OLD / f"{z}.zip"
        req = urllib.request.Request(f"https://www.federalreserve.gov/econres/files/{z}.zip",
                                     headers={"User-Agent": "Mozilla/5.0"})
        zp.write_bytes(urllib.request.urlopen(req).read())
        zipfile.ZipFile(zp).extractall(OLD)
        zp.unlink()
    return p


def load(year):
    s = read(SCF / f"rscfp{year}.dta", ["y1", "yy1", "x1", "xx1", "wgt", "age", "occat1", "lf",
                                        "dbplancj", "dcplancj", "bplancj", "dbplant"])
    if "y1" not in s:
        s = s.rename(columns={"x1": "y1", "xx1": "yy1"})
    s["imp"] = (s.y1 - s.yy1 * 10).astype(int)
    return s


def load_rw(year):
    cols = ["y1", "x1"] + [f"wt1b{k}" for k in range(1, 1000)] + [f"mm{k}" for k in range(1, 1000)]
    r = read(rw_path(year), cols)
    if "y1" not in r:
        r = r.rename(columns={"x1": "y1"})
    r = r.set_index("y1")
    return np.column_stack([np.nan_to_num(r[f"wt1b{k}"].to_numpy(float) * r[f"mm{k}"].to_numpy(float))
                            for k in range(1, 1000)]), r.index


def share(d, num, w):
    m = d.eval(num).values
    m = m[:, None] if w.ndim == 2 else m
    return 100 * (w * m).sum(axis=0) / w.sum(axis=0)


def run():
    rows = []
    for year in WAVES:
        df = load(year)
        W, idx = load_rw(year)
        rwi = pd.DataFrame(W, index=idx)
        for pop, popq in [("all households", "age >= 0"), ("employee households", EMP)]:
            for g, gq in GROUPS.items():
                d = df.query(f"({popq}) and ({gq})")
                d1 = d[d.imp == 1]
                Wd = rwi.reindex(d1.y1.values).fillna(0).to_numpy()
                for name, (num, _) in STATS.items():
                    est = share(d, num, d.wgt.values)
                    imps = [share(gi, num, gi.wgt.values * 5) for _, gi in d.groupby("imp")]
                    reps = share(d1, num, Wd)
                    reps = reps[np.isfinite(reps)]
                    se = float(np.sqrt(np.var(reps, ddof=1) + 1.2 * np.var(imps, ddof=1)))
                    rows.append(dict(survey_year=year, population=pop, age_group=g, stat=name,
                                     estimate=round(float(est), 2), se=round(se, 2), n_cases=len(d1)))
        print(year, "done", flush=True)
    res = pd.DataFrame(rows)
    OUT.mkdir(exist_ok=True)
    res.to_csv(OUT / "scf_db_coverage_long.csv", index=False)
    wide = res.pivot_table(index=["population", "age_group", "stat"], columns="survey_year", values="estimate")
    for pop, g, st in [("employee households", "all", "pct_db_current_job"),
                       ("employee households", "all", "pct_dc_current_job"),
                       ("employee households", "<35", "pct_db_current_job"),
                       ("employee households", "45-54", "pct_db_current_job"),
                       ("all households", "55-64", "pct_db_cj_or_past_job_future")]:
        print(pop, g, st, wide.loc[(pop, g, st)].round(1).to_dict())
    return res


if __name__ == "__main__":
    run()
