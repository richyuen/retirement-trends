"""Extract the SIPP 2014 panel, waves 2-4 (reference years 2014-2016), December records, for the pooled
retirement-plan distribution item ERET_LUMPSUM ("receipt of any lump sum or regular distribution payments from a
retirement plan"; covers IRAs, 401k-type plans and DB pensions together; wave 1 does not have it).

Usage: python3 extract_2014.py [RAW_DIR]
Writes ../data/sipp2014_dec.parquet and /tmp/sipph/rw2014_w{w}_dec.parquet (replicate weights, kept out of the
shared folder).
"""
import os, sys, subprocess, zipfile
import pandas as pd

B = "https://www2.census.gov/programs-surveys/sipp/data/datasets/2014"
RAW = sys.argv[1] if len(sys.argv) > 1 else "/tmp/sipph/raw"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data")
os.makedirs(RAW, exist_ok=True)
COLS = ["SSUID", "PNUM", "MONTHCODE", "SWAVE", "WPFINWGT", "TAGE", "TAGE_EHC", "EOWN_IRAKEO", "EOWN_THR401",
        "EOWN_PENSION", "TIRAKEOVAL", "TTHR401VAL", "ERET_LUMPSUM", "ERETANY", "EEVERET"] + \
       [f"ERETTYP{i}YN" for i in range(1, 9)]


def get(name):
    p = os.path.join(RAW, name)
    if not os.path.exists(p):
        w = name.split("w")[-1][0]
        subprocess.run(["curl", "-sS", "--retry", "4", "-o", p, f"{B}/w{w}/{name}"], check=True)
    return p


frames = []
for w in (2, 3, 4):
    z = get(f"pu2014w{w}_csv.zip")
    with zipfile.ZipFile(z) as zz:
        with zz.open(zz.namelist()[0]) as f:
            parts = [c[c.MONTHCODE == 12] for c in
                     pd.read_csv(f, sep="|", usecols=COLS, chunksize=20_000, low_memory=False, dtype={"SSUID": str})]
    d = pd.concat(parts); d["sipp_wave"] = w; d["ref_year"] = 2012 + w
    frames.append(d); os.remove(z)
    r = get(f"rw14w{w}.csv.gz")
    reps = pd.concat([c[c.monthcode == 12] for c in pd.read_csv(r, sep="|", chunksize=200_000, dtype={"ssuid": str})])
    reps = reps.rename(columns={"ssuid": "SSUID"})
    reps[["SSUID", "PNUM"] + [f"repwt{i}" for i in range(1, 241)]].to_parquet(f"/tmp/sipph/rw2014_w{w}_dec.parquet")
    os.remove(r)
    print("2014 wave", w, len(d), "persons;", len(reps), "replicate rows", flush=True)
pd.concat(frames).to_parquet(os.path.join(OUT, "sipp2014_dec.parquet"), index=False)
print("wrote 2014")
