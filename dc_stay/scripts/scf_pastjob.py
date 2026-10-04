"""SCF 1989-2022: money left in former employers' DC plans (Fed FUTPEN, CURRPEN) vs IRAs.

FUTPEN  = account-type plans from a PAST job not yet paying out (the 'future pensions' section: rights to
          pensions or retirement accounts from a previous employer that the household will draw on later).
CURRPEN = account-type plans now paying out (from 2001; the Fed sets it to 0 before 2001). Mostly past-job plans
          taken as installments/withdrawals from the plan itself.
pastplan = FUTPEN + CURRPEN (2001+) = money still sitting in a former employer's plan.
Households are classified by the reference person's age; 'not working' = Fed LF == 0 (reference person).
SEs (2004+) use the replicate-weight + imputation method in scf/scripts/scf_analysis.py.
Run: python3 dc_stay/scripts/scf_pastjob.py  (reads scf/raw/, writes dc_stay/output/scf_pastjob_long.csv)
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parents[1]
SCF = HERE.parent / "scf"
sys.path.insert(0, str(SCF / "scripts"))
from scf_analysis import read, estimate, share, ratio, load_rw, WAVES  # noqa: E402

RAW, OUT = SCF / "raw", HERE / "output"
OUT.mkdir(exist_ok=True)
VARS = ["y1", "yy1", "wgt", "age", "lf", "irakh", "thrift", "futpen", "currpen", "retqliq"]
GROUPS = {
    "all": "age >= 0",
    "45-54": "age >= 45 & age <= 54",
    "55-64": "age >= 55 & age <= 64",
    "65-74": "age >= 65 & age <= 74",
    "75+": "age >= 75",
    "60-74 not working": "age >= 60 & age <= 74 & lf == 0",
    "60-74 working": "age >= 60 & age <= 74 & lf == 1",
}


def load(year):
    s = read(RAW / f"rscfp{year}.dta", VARS + ["x1", "xx1"]).rename(columns={"x1": "y1", "xx1": "yy1"})
    s["imp"] = (s.y1 - s.yy1 * 10).astype(int)
    s["pastplan"] = s.futpen + s.currpen
    s["leaver_pool"] = s.pastplan + s.irakh  # money that left (IRA) or stayed (past-job plan) after job change
    s["year"] = year
    return s


STATS = {
    "pct_hh_with_futpen": share("futpen > 0", "age >= 0"),
    "pct_hh_with_pastplan": share("pastplan > 0", "age >= 0"),
    "pct_hh_with_ira": share("irakh > 0", "age >= 0"),
    "pct_of_ret_holders_with_pastplan": share("pastplan > 0", "retqliq > 0"),
    "pct_of_pastplan_or_ira_holders_with_pastplan": share("pastplan > 0", "leaver_pool > 0"),
    "pastplan_pct_of_pastplan_plus_ira_dollars": ratio("pastplan", "leaver_pool", "leaver_pool > 0"),
    "futpen_pct_of_futpen_plus_ira_dollars": ratio("futpen", "leaver_pool", "leaver_pool > 0"),
    "pastplan_pct_of_ret_dollars": ratio("pastplan", "retqliq", "retqliq > 0"),
}


def run():
    rows = []
    for year in WAVES:
        df = load(year)
        rw = load_rw(year) if year >= 2004 else None
        for gname, cond in GROUPS.items():
            g = df[df.eval(cond)]
            for name, fn in STATS.items():
                est, se = estimate(g, rw, fn)
                rows.append(dict(survey_year=year, group=gname, stat=name, estimate=est, se=se,
                                 n_cases=int((g.imp == 1).sum())))
        print(year, "done", flush=True)
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "scf_pastjob_long.csv", index=False, float_format="%.3f")
    return res


if __name__ == "__main__":
    run()
