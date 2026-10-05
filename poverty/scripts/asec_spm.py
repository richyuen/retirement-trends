"""Official and SPM poverty for people 65+ from Census public-use CPS ASEC CSV files, 2019-2026
(income years 2018-2025), with standard errors from Census replicate weights.

Usage: python3 asec_spm.py RAW_DIR
RAW_DIR holds asecpubYYcsv.zip (YY = 19..26) from
https://www2.census.gov/programs-surveys/cps/datasets/20YY/march/asecpubYYcsv.zip (~140-185MB each;
kept outside the project). Missing zips are downloaded.

What it computes (person weight MARSUPWT, as Census does for person rates):
- OPM poor: PERLIS == 1 (universe PERLIS > 0). Near-poor: PERLIS in (1,2,3) = below 150%.
- SPM poor: SPM_RESOURCES < SPM_POVTHRESHOLD (checked against SPM_POOR). SPM ratio = resources/threshold.
- Element effects (Census Table 5 method): recompute SPM poverty after removing one element, threshold fixed.
  * Social Security: resources minus the SPM unit's summed SS_VAL. Effect = rate - rate_without (negative).
  * SSI: same with SSI_VAL.
  * Medical expenses (MOOP): resources plus SPM_MEDXPNS. Effect = rate - rate_without (positive).
- Groups among 65+: all, 65-74, 75+, men, women, living alone (1-person household), living with others,
  White alone non-Hispanic, Black alone, Asian alone, Hispanic (any race).
- SE: successive difference replication, Var = 4/160 * sum_r (theta_r - theta_0)^2, replicate weights
  from asec_csv_repwgt_YYYY.csv in the same zip, merged on (PH_SEQ, PPPOS).
Writes ../output/asec_65plus_poverty_by_group.csv (long) and prints a validation summary.
"""
import os, sys, zipfile, urllib.request
import numpy as np, pandas as pd

RAW = sys.argv[1] if len(sys.argv) > 1 else "/tmp/asec"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
COLS = ["PH_SEQ", "PPPOS", "A_AGE", "A_SEX", "MARSUPWT", "PERLIS", "PRDTRACE", "PEHSPNON", "SPM_ID",
        "SPM_RESOURCES", "SPM_POVTHRESHOLD", "SPM_POOR", "SPM_MEDXPNS", "SS_VAL", "SSI_VAL"]


def load(yy):
    z = os.path.join(RAW, f"asecpub{yy}csv.zip")
    if not os.path.exists(z):
        urllib.request.urlretrieve(
            f"https://www2.census.gov/programs-surveys/cps/datasets/20{yy}/march/asecpub{yy}csv.zip", z)
    zf = zipfile.ZipFile(z)
    names = zf.namelist()
    pp = [n for n in names if os.path.basename(n).lower() == f"pppub{yy}.csv"][0]
    rw = [n for n in names if "repwgt" in n.lower()][0]
    p = pd.read_csv(zf.open(pp), usecols=lambda c: c.upper() in COLS)
    p.columns = [c.upper() for c in p.columns]
    r = pd.read_csv(zf.open(rw))
    r.columns = [c.upper() for c in r.columns]
    r = r.rename(columns={"H_SEQ": "PH_SEQ"})
    return p, r


def main():
    rows = []
    for yy in range(19, 27):
        p, r = load(yy)
        asec = 2000 + yy
        # household size for "living alone"
        p["hhsize"] = p.groupby("PH_SEQ")["PH_SEQ"].transform("size")
        # SPM unit Social Security and SSI
        p["ss_unit"] = p.groupby(["PH_SEQ", "SPM_ID"])["SS_VAL"].transform("sum")
        p["ssi_unit"] = p.groupby(["PH_SEQ", "SPM_ID"])["SSI_VAL"].transform("sum")
        res, thr = p["SPM_RESOURCES"].astype(float), p["SPM_POVTHRESHOLD"].astype(float)
        p["spm"] = (res < thr).astype(float)
        mism = (p["spm"] != (p["SPM_POOR"] == 1)).mean()
        ratio = res / thr
        p["spm150"] = (ratio < 1.5).astype(float)
        p["spm200"] = (ratio < 2.0).astype(float)
        p["spm_noss"] = ((res - p["ss_unit"]) < thr).astype(float)
        p["spm_nossi"] = ((res - p["ssi_unit"]) < thr).astype(float)
        p["spm_nomoop"] = ((res + p["SPM_MEDXPNS"]) < thr).astype(float)
        p["opm"] = (p["PERLIS"] == 1).astype(float)
        p["opm125"] = p["PERLIS"].isin([1, 2]).astype(float)
        p["opm150"] = p["PERLIS"].isin([1, 2, 3]).astype(float)
        p = p[p["PERLIS"] > 0]  # poverty universe (same universe for SPM, as in Census tables)
        p = p.merge(r, on=["PH_SEQ", "PPPOS"], how="left", validate="1:1")
        assert p["PWWGT1"].notna().all()
        wcols = ["MARSUPWT"] + [f"PWWGT{i}" for i in range(1, 161)]
        W = p[wcols].to_numpy(float)
        age = p["A_AGE"].to_numpy()
        groups = {
            "all ages": np.ones(len(p), bool),
            "under 18": age < 18,
            "18-64": (age >= 18) & (age <= 64),
            "65+": age >= 65,
            "65-74": (age >= 65) & (age <= 74),
            "75+": age >= 75,
            "65+ men": (age >= 65) & (p["A_SEX"].to_numpy() == 1),
            "65+ women": (age >= 65) & (p["A_SEX"].to_numpy() == 2),
            "65+ living alone": (age >= 65) & (p["hhsize"].to_numpy() == 1),
            "65+ living with others": (age >= 65) & (p["hhsize"].to_numpy() > 1),
            "65+ White alone non-Hispanic": (age >= 65) & (p["PRDTRACE"].to_numpy() == 1) & (p["PEHSPNON"].to_numpy() == 2),
            "65+ Black alone": (age >= 65) & (p["PRDTRACE"].to_numpy() == 2),
            "65+ Asian alone": (age >= 65) & (p["PRDTRACE"].to_numpy() == 4),
            "65+ Hispanic": (age >= 65) & (p["PEHSPNON"].to_numpy() == 1),
        }
        ind = {k: p[k].to_numpy(float) for k in
               ["opm", "opm125", "opm150", "spm", "spm150", "spm200", "spm_noss", "spm_nossi", "spm_nomoop"]}
        for g, m in groups.items():
            Wg = W[m]
            den = Wg.sum(0)
            est = {k: (Wg * v[m][:, None]).sum(0) / den * 100 for k, v in ind.items()}
            est["ss_effect"] = est["spm"] - est["spm_noss"]
            est["ssi_effect"] = est["spm"] - est["spm_nossi"]
            est["moop_effect"] = est["spm"] - est["spm_nomoop"]
            est["spm_minus_opm"] = est["spm"] - est["opm"]
            for k, v in est.items():
                se = np.sqrt(4 / 160 * ((v[1:] - v[0]) ** 2).sum())
                rows.append(dict(asec_year=asec, income_year=asec - 1, group=g, measure=k,
                                 pct=round(v[0], 2), se=round(se, 2), n=int(m.sum()),
                                 pop_k=round(den[0] / 100 / 1000, 0)))  # MARSUPWT: 2 implied decimals
        print(f"ASEC {asec}: n={len(p)}, SPM_POOR mismatch {mism:.4%}")
    df = pd.DataFrame(rows)
    os.makedirs(OUT, exist_ok=True)
    df.to_csv(os.path.join(OUT, "asec_65plus_poverty_by_group.csv"), index=False)
    piv = df[df.group == "65+"].pivot(index="income_year", columns="measure", values="pct")
    print(piv[["opm", "spm", "ss_effect", "moop_effect", "ssi_effect", "opm150", "spm150", "spm200"]].round(2).to_string())


if __name__ == "__main__":
    main()
