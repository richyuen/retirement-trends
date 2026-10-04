"""Extract SIPP 1996-2008 panel data for combined IRA/Keogh/401(k) withdrawals and balances.

For each Assets & Liabilities topical module wave w, a person's 12-month window is the
reference months of core waves w-2, w-1 and w. Withdrawals = sum of monthly TPPNDIST
(ISS code 42: distributions from IRAs, Keogh and 401k plans). Balances = TALRB + TALKB +
TALTB from the topical module ("as of the last day of the reference period", i.e. the end
of the window). Weights: topical-module WPFINWGT; replicate weights: core-wave rw file,
reference month 4.

Usage: python3 extract.py [RAW_DIR]   (downloads ~1 GB of zips to RAW_DIR, default /tmp/sipph/raw)
Writes ../data/sipp_hist_persons.parquet and /tmp/sipph/reps_*.parquet.
"""
import io, os, re, sys, subprocess, zipfile
import pandas as pd

B = "https://www2.census.gov/programs-surveys/sipp/data/datasets"
RAW = sys.argv[1] if len(sys.argv) > 1 else "/tmp/sipph/raw"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data")
os.makedirs(RAW, exist_ok=True); os.makedirs(OUT, exist_ok=True)

# panel -> (year dir, core dictionary path, core zip pattern, [(asset wave, tm zip, tm dict)])
PANELS = {
    1996: ("1996", "1996/w1/sip96w1d.asc", "1996/w{w}/l96puw{w}.zip",
           [(w, f"1996/w{w}/tm96puw{w}.zip", f"1996/w{w}/tm96pw{w}d.asc") for w in (3, 6, 9, 12)], 108),
    2001: ("2001", "2001/w1/l01puw1d.txt", "2001/w{w}/l01puw{w}.zip",
           [(3, "2001/w3/p01putm3.zip", "2001/w3/p01ptm3d.txt"), (6, "2001/w6/p01putm6.zip", "2001/w6/p01ptm6d.txt"),
            (9, "2001/w9/p01putm9.zip", "2001/w9/p01tm9d.txt")], 108),
    2004: ("2004", "2004/w1/l04puw1d.txt", "2004/w{w}/l04puw{w}.zip",
           [(3, "2004/w3/p04putm3.zip", "2004/w3/p04tm3d.txt"), (6, "2004/w6/p04putm6.zip", "2004/w6/p04tm6d.txt")], 120),
    2008: ("2008", "2008/w1/l08puw1d.txt.old2", "2008/w{w}/l08puw{w}.zip",
           [(w, f"2008/w{w}/p08putm{w}.zip", f"2008/w{w}/p08tm{w}d.txt") for w in (4, 7, 10)], 120),
}
L96 = {"SSUID": (5, 12), "SWAVE": (21, 2), "SREFMON": (24, 1), "RHCALMN": (25, 2), "RHCALYR": (27, 4),
       "EPPPNUM": (513, 4), "EPOPSTAT": (519, 1), "TAGE": (572, 2), "TPPNDIST": (657, 5)}
CORE_VARS = ["SSUID", "EPPPNUM", "SWAVE", "SREFMON", "RHCALMN", "RHCALYR", "TAGE", "EPOPSTAT", "TPPNDIST"]
TM_VARS = ["SSUID", "EPPPNUM", "WPFINWGT", "TAGE", "TALRB", "TALKB", "TALTB"]


def fetch(rel):
    p = os.path.join(RAW, rel.replace("/", "_"))
    if not os.path.exists(p):
        subprocess.run(["curl", "-sS", "--retry", "4", "-o", p, f"{B}/{rel}"], check=True)
    return p


def layout(dict_path, names):
    pos = {}
    for line in open(dict_path, encoding="latin-1"):
        m = re.match(r"^D (\S+)\s+(\d+)\s+(\d+)", line)
        if m and m.group(1) in names and m.group(1) not in pos:
            pos[m.group(1)] = (int(m.group(3)) - 1, int(m.group(2)))
    missing = set(names) - set(pos)
    assert not missing, (dict_path, missing)
    return pos


def read_fixed(zip_path, pos, keep=None):
    cols = {k: [] for k in pos}
    with zipfile.ZipFile(zip_path) as z:
        name = [n for n in z.namelist() if not n.endswith("/")][0]
        with z.open(name) as f:
            for raw in io.TextIOWrapper(f, encoding="latin-1"):
                if keep is not None and not keep(raw):
                    continue
                for k, (s, l) in pos.items():
                    cols[k].append(raw[s:s + l])
    df = pd.DataFrame(cols)
    for k in df.columns:
        if k != "SSUID":
            df[k] = pd.to_numeric(df[k].str.strip(), errors="coerce")
    return df


rows = []
for panel, (ydir, cdict, cpat, assets, nrep) in PANELS.items():
    cpos0 = layout(fetch(cdict), CORE_VARS)
    need = sorted({w - k for w, _, _ in assets for k in (2, 1, 0)})
    core = {}
    for w in need:
        cache = f"/tmp/sipph/core_{panel}_w{w}.parquet"
        if os.path.exists(cache):
            core[w] = pd.read_parquet(cache); continue
        # The 1996 core files Census now serves are the re-edited longitudinal "l96puw" files, whose layout is not
        # the one in Census's sip96wXd.asc dictionaries. Positions below are from NBER's sip96l1.dct (identical for
        # waves 1-12: data.nber.org/sipp/1996/), checked against the data (person numbers, ages, population status).
        cpos = L96 if panel == 1996 else cpos0
        z = fetch(cpat.format(w=w))
        d = read_fixed(z, cpos)
        assert (d.SWAVE == w).all(), (panel, w, d.SWAVE.unique()[:5])
        assert d.EPPPNUM.min() >= 101, (panel, w, d.EPPPNUM.min())
        d = d[d.EPOPSTAT == 1]
        core[w] = d.groupby(["SSUID", "EPPPNUM"]).agg(
            nmon=("SREFMON", "size"), wd=("TPPNDIST", "sum"), nwd=("TPPNDIST", lambda s: (s > 0).sum()),
            ym_min=("RHCALYR", lambda s: 0), ).reset_index()
        # months covered, for labelling the window
        d["ym"] = d.RHCALYR * 12 + d.RHCALMN - 1
        mm = d.groupby(["SSUID", "EPPPNUM"]).ym.agg(["min", "max"]).reset_index()
        core[w] = core[w].drop(columns="ym_min").merge(mm, on=["SSUID", "EPPPNUM"])
        core[w].to_parquet(cache)
        os.remove(z)
        print(panel, "core wave", w, len(d), "person-months", flush=True)
    rpos = {"SSUID": (0, 12), "SWAVE": (16, 2), "SREFMON": (18, 1), "EPPPNUM": (19, 4)}
    rpos.update({f"R{i}": (23 + (i - 1) * 10, 10) for i in range(1, nrep + 1)})
    for w, tmzip, tmdict in assets:
        tpos = layout(fetch(tmdict), TM_VARS)
        z = fetch(tmzip)
        tm = read_fixed(z, tpos)
        os.remove(z)
        tm = tm[tm.TAGE >= 15]
        win = None
        for k in (2, 1, 0):
            c = core[w - k][["SSUID", "EPPPNUM", "nmon", "wd", "nwd", "min", "max"]].rename(
                columns={"nmon": f"n{k}", "wd": f"wd{k}", "nwd": f"nwd{k}", "min": f"mn{k}", "max": f"mx{k}"})
            win = c if win is None else win.merge(c, on=["SSUID", "EPPPNUM"], how="inner")
        p = tm.merge(win, on=["SSUID", "EPPPNUM"], how="left")
        p["months"] = p[["n0", "n1", "n2"]].sum(axis=1, min_count=1)
        p["wd12"] = p[["wd0", "wd1", "wd2"]].sum(axis=1, min_count=1)
        p["wdmonths"] = p[["nwd0", "nwd1", "nwd2"]].sum(axis=1, min_count=1)
        p["win_start"] = p.mn2; p["win_end"] = p.mx0
        p["panel"] = panel; p["wave"] = w
        keep = ["panel", "wave", "SSUID", "EPPPNUM", "WPFINWGT", "TAGE", "TALRB", "TALKB", "TALTB",
                "months", "wd12", "wdmonths", "win_start", "win_end"]
        rows.append(p[keep])
        rz = fetch(f"{ydir}/w{w}/rw{str(panel)[2:]}w{w}.zip")
        rw = read_fixed(rz, rpos, keep=lambda r: r[18] == "4")
        os.remove(rz)
        rw = rw.drop(columns=["SWAVE", "SREFMON"])
        rw.to_parquet(f"/tmp/sipph/reps_{panel}_w{w}.parquet")
        print(panel, "asset wave", w, len(tm), "persons;", int(p.months.eq(12).sum()), "with 12 months;",
              len(rw), "replicate rows", flush=True)
    del core

out = pd.concat(rows, ignore_index=True)
out.to_parquet(os.path.join(OUT, "sipp_hist_persons.parquet"), index=False)
print("wrote", len(out))
