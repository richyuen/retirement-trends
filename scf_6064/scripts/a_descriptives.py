"""(a) Withdrawal measures and characteristics of retirement-account holders, ages 55-59 / 60-64 / 65-69,
by withdrawal year (SCF 2004-2022 -> 2003-2021) and for pooled periods 2003/06 and 2018/21.
Unit: households holding RETQLIQ > 0 at interview (age of reference person at interview).
Output: output/a_descriptives_long.csv (estimate, se, n = unweighted households) and a_descriptives_6064_wide.csv
Run: python3 scf_6064/scripts/a_descriptives.py
"""
import pandas as pd
from common import load_all, band, add_derived, groups_by_wave, estimate_v, vshare, vratio, vmean, vpop, median_of, estimate, OUT, BANDS

H = "holder"
STATS = {
    # withdrawal outcomes
    "inc_any_per100_holders": vshare("wd_any"),
    "inc_ira_per100_ira_holders": vshare("wd_ira", "has_ira"),
    "inc_pen_per100_dc_holders": vshare("wd_pen", "pen > 0"),
    "pct_holders_wd_ge5pct_of_balance": vshare("wd5"),
    "pct_holders_wd_ge10pct_of_balance": vshare("wd10"),
    "rate_all_pct": vratio("penacctwd", "retqliq"),
    "rate_ira_part_pct": vratio("ira_wd", "retqliq"),
    "rate_pension_part_pct": vratio("pen_wd", "retqliq"),
    "rate_ira_wd_over_irakh_pct": vratio("ira_wd", "irakh", "has_ira"),
    "rate_pen_wd_over_futpen_currpen_pct": vratio("pen_wd", "futpen + currpen", "has_oldpen"),
    "rate_excl_thrift_from_balance_pct": vratio("penacctwd", "retqliq - thrift"),
    "rate_excl_top3_withdrawers_pct": vratio("penacctwd", "retqliq", "holder and not top3"),
    "mean_hh_rate_capped100_pct": vmean("hh_rate"),
    "mean_wd_per_holder_k": vmean("penacctwd", scale=1e-3),
    "mean_bal_per_holder_k": vmean("retqliq", scale=1e-3),
    "holders_millions": vpop(H),
    # work / retirement
    "pct_r_working": vshare("r_work"),
    "pct_r_retired": vshare("r_retired"),
    "pct_spouse_working": vshare("sp_work"),
    "pct_r_or_spouse_working": vshare("any_work"),
    "pct_r_receives_ss": vshare("r_ss"),
    "pct_r_receives_ss_retirement": vshare("r_ss_ret"),
    "pct_hh_receives_ss": vshare("hh_ss"),
    # account structure
    "pct_ira_only": vshare("ira_only"),
    "pct_dc_only": vshare("dc_only"),
    "pct_ira_and_dc": vshare("ira_dc"),
    "pct_has_thrift": vshare("has_thrift"),
    "pct_has_past_job_or_paying_dc": vshare("has_oldpen"),
    "dollar_share_irakh": vratio("irakh", "retqliq"),
    "dollar_share_thrift": vratio("thrift", "retqliq"),
    "dollar_share_futpen": vratio("futpen", "retqliq"),
    "dollar_share_currpen": vratio("currpen", "retqliq"),
    "roth_share_of_ira_dollars": vratio("roth", "irakh", "has_ira"),
    "rollover_ira_share_of_ira_dollars": vratio("rollover", "irakh", "has_ira"),
    "pct_has_roth": vshare("has_roth"),
    # demographics
    "pct_married": vshare("marr"),
    "pct_ba_plus": vshare("ba"),
    "pct_db_pension": vshare("db"),
    "pct_female_ref": vshare("female"),
    "mean_age": vmean("age"),
}
MEDIANS = {"median_bal_per_holder_k": median_of("retqliq", H), "median_income_ex_wd_k": median_of("income_x", H)}


def run():
    df = load_all()
    rows = []
    for b in BANDS:
        d = add_derived(band(df, b), b)
        for lab, g in groups_by_wave(d):
            n = int(g[g.holder].shape[0] / 5)
            for name, fn in STATS.items():
                if name == "holders_millions" and "/" in lab:
                    continue  # a pooled-period population total is not meaningful
                est, se = estimate_v(g, fn)
                rows.append(dict(age_band=b, wd_year=lab, stat=name, estimate=float(est), se=float(se), n=n))
            for name, fn in MEDIANS.items():
                est, se = estimate(g, fn)
                rows.append(dict(age_band=b, wd_year=lab, stat=name, estimate=float(est) / 1e3, se=float(se) / 1e3, n=n))
        print(b, "done", flush=True)
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "a_descriptives_long.csv", index=False, float_format="%.4f")
    w = res[res.age_band == "60-64"].pivot_table(index="stat", columns="wd_year", values=["estimate", "se"], sort=False)
    w = w.swaplevel(axis=1).sort_index(axis=1, level=0, sort_remaining=False)
    w.round(3).to_csv(OUT / "a_descriptives_6064_wide.csv")
    return res


if __name__ == "__main__":
    r = run()
    print(r[r.age_band == "60-64"].pivot_table(index="stat", columns="wd_year", values="estimate", sort=False).round(2).to_string())
