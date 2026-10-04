"""Bridge years 2014-2019: SIPP's pooled item ERET_LUMPSUM ("receipt of any lump sum or regular distribution payments
from a retirement plan": IRAs, 401k-type plans and DB pensions together; asked at 59+), among year-end IRA/401k
holders (IRA/Keogh + 401k/403b/thrift balance > 0 on Dec 31). Not comparable with the account-specific series.

Inputs: ../data/sipp2014_dec.parquet (2014 panel waves 2-4 = ref 2014-2016) and
        ../../sipp/data/sipp_persons_dec.parquet (SIPP 2018-2020 = ref 2017-2019).
2014-2016 is a yes/no item; 2017-2019 splits lump sum / regular / both / none ("any" = not none).
SEs: Fay BRR (4/240) from /tmp/sipph/rw2014_w*_dec.parquet and /tmp/sipp/reps/rwYYYY_dec.parquet (kept outside the
shared folder; rebuild with extract_2014.py and sipp/scripts/extract.py).
Writes ../output/sipp_bridge_long.csv.
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "output")
BANDS = [("60-64", 60, 64), ("65-69", 65, 69), ("70-74", 70, 74), ("75-79", 75, 79), ("80+", 80, 200),
         ("60+", 60, 200), ("70+", 70, 200)]

a = pd.read_parquet(os.path.join(HERE, "..", "data", "sipp2014_dec.parquet"))
a["src"] = "2014 panel"
b = pd.read_parquet(os.path.join(HERE, "..", "..", "sipp", "data", "sipp_persons_dec.parquet"))
b = b[b.ref_year.between(2017, 2019)].rename(columns={"PNUM": "PNUM"})
b["src"] = "SIPP " + b.sipp_year.astype(str)
cols = ["SSUID", "PNUM", "ref_year", "src", "WPFINWGT", "TAGE_EHC", "EOWN_IRAKEO", "EOWN_THR401", "EOWN_PENSION",
        "TIRAKEOVAL", "TTHR401VAL", "ERET_LUMPSUM", "ERETTYP1YN"]
d = pd.concat([a[cols + ["sipp_wave"]], b[cols]], ignore_index=True)
d["bal"] = d.TIRAKEOVAL.fillna(0).clip(lower=0) * d.EOWN_IRAKEO.eq(1) + \
           d.TTHR401VAL.fillna(0).clip(lower=0) * d.EOWN_THR401.eq(1)
d = d[(d.bal > 0) & (d.WPFINWGT > 0)]
# 2014 panel codes 1 yes / 2 no; SIPP 2018-2020 code 1 lump sum, 2 regular, 3 both, 4 none
d["any"] = np.where(d.ref_year <= 2016, d.ERET_LUMPSUM.eq(1), d.ERET_LUMPSUM.isin([1, 2, 3])).astype(float)
d["no_db"] = d.EOWN_PENSION.ne(1) & d.ERETTYP1YN.ne(1)

rows = []
for yr, g in d.groupby("ref_year"):
    reps = None
    if yr <= 2016:
        r = pd.read_parquet(f"/tmp/sipph/rw2014_w{yr - 2012}_dec.parquet")
        r["SSUID"] = r.SSUID.astype(str)
        g = g.assign(SSUID=g.SSUID.astype(str)).merge(r, on=["SSUID", "PNUM"], how="left")
        reps = g[[f"repwt{i}" for i in range(1, 241)]].fillna(0).to_numpy()
    elif os.path.exists(f"/tmp/sipp/reps/rw{yr + 1}_dec.parquet"):
        r = pd.read_parquet(f"/tmp/sipp/reps/rw{yr + 1}_dec.parquet")
        g = g.merge(r, on=["SSUID", "PNUM"], how="left")
        reps = g[[f"REPWGT{i}" for i in range(1, 241)]].fillna(0).to_numpy(float)
    w = g.WPFINWGT.to_numpy()
    for sub, sm in (("all_holders", np.ones(len(g), bool)), ("no_db_pension", g.no_db.to_numpy())):
        for name, lo, hi in BANDS:
            m = sm & g.TAGE_EHC.between(lo, hi).to_numpy()
            for meas in ("any",):
                y = g[meas].to_numpy()
                f = lambda ww: 100 * (ww[m] * y[m]).sum() / ww[m].sum()
                est = f(w)
                se = np.nan if reps is None else np.sqrt(4 / 240 * sum((f(reps[:, i]) - est) ** 2 for i in range(240)))
                rows.append(dict(ref_year=yr, subgroup=sub, age_band=name,
                                 measure=f"pooled_{meas}_dist_per100", estimate=round(est, 2),
                                 se=None if np.isnan(se) else round(se, 2), n=int(m.sum())))
L = pd.DataFrame(rows)
L.to_csv(os.path.join(OUT, "sipp_bridge_long.csv"), index=False)
pd.set_option("display.width", 200)
print(L.pivot_table(index=["subgroup", "measure", "age_band"], columns="ref_year", values="estimate").to_string())
print(L.pivot_table(index=["subgroup", "measure", "age_band"], columns="ref_year", values="se").to_string())
