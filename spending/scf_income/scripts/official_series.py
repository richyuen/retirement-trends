"""Official/administrative series on income sources and retirement funding of older Americans.

Downloads (all reachable from project threads):
  BLS CPS labor force participation (annual average of monthly, not seasonally adjusted), BLS public API v1:
    LNU01300097 = 65 and over, LNU01300095 = 55-64     https://api.bls.gov/publicAPI/v1/timeseries/data/
  BEA NIPA via FRED: W823RC1 Social Security benefits to persons ($bn, annual avg of SAAR),
    PI personal income                                   https://fred.stlouisfed.org/series/W823RC1
  Federal Reserve Distributional Financial Accounts by age: DB and DC pension entitlements
    https://www.federalreserve.gov/releases/z1/dataviz/download/zips/dfa.zip  (dfa-age-levels.csv, $ millions)
Writes output/official_*.csv. Hand-entered published tables are in output/official_published_figures.csv
(each row carries its source and table).
Run: python3 spending/scf_income/scripts/official_series.py
"""
from pathlib import Path
import io, json, subprocess, time, zipfile, urllib.request
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "output"
UA = {"User-Agent": "Mozilla/5.0 (research script)"}


def get(url, data=None, headers=None):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception:
            if data is None:  # FRED sometimes drops urllib connections; curl over HTTP/1.1 works
                try:
                    return subprocess.run(["curl", "-sS", "--http1.1", "-m", "120", url], check=True,
                                          capture_output=True).stdout
                except Exception:
                    pass
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"download failed: {url}")


def bls_lfpr():
    rows = []
    for a, b in [(1986, 1995), (1996, 2005), (2006, 2015), (2016, 2025)]:
        body = json.dumps({"seriesid": ["LNU01300097", "LNU01300095"], "startyear": str(a), "endyear": str(b)}).encode()
        r = json.loads(get("https://api.bls.gov/publicAPI/v1/timeseries/data/", body, {"Content-type": "application/json"}))
        for s in r["Results"]["series"]:
            for d in s["data"]:
                if d["period"] < "M13" and d["value"] not in ("-", ""):
                    rows.append((s["seriesID"], int(d["year"]), float(d["value"])))
        time.sleep(2)
    df = pd.DataFrame(rows, columns=["series", "year", "value"])
    a = df.groupby(["series", "year"]).value.agg(["mean", "size"]).reset_index()
    w = a.pivot(index="year", columns="series", values="mean").round(1)
    w = w.rename(columns={"LNU01300097": "lfpr_65plus", "LNU01300095": "lfpr_55_64"})
    w["months_averaged"] = a.pivot(index="year", columns="series", values="size").min(axis=1)
    w["note"] = ""
    w.loc[w.months_averaged < 12, "note"] = "October 2025 not published (federal shutdown); 11-month average"
    w.to_csv(OUT / "official_bls_lfpr.csv")
    return w


def fred_annual(sid):
    raw = get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&fq=Annual&fam=avg")
    d = pd.read_csv(io.BytesIO(raw))
    d["year"] = d.iloc[:, 0].str[:4].astype(int)
    return d.set_index("year")[sid]


def bea_ss():
    ss, pi = fred_annual("W823RC1"), fred_annual("PI")
    d = pd.DataFrame({"ss_benefits_bn": ss, "personal_income_bn": pi}).dropna()
    d["ss_pct_of_personal_income"] = (100 * d.ss_benefits_bn / d.personal_income_bn).round(2)
    d.to_csv(OUT / "official_bea_ss_benefits.csv")
    return d


def dfa_age():
    z = zipfile.ZipFile(io.BytesIO(get("https://www.federalreserve.gov/releases/z1/dataviz/download/zips/dfa.zip")))
    d = pd.read_csv(z.open("dfa-age-levels.csv"))
    d = d[d.Date.str.endswith("Q4") | (d.Date == d.Date.max())].copy()
    d["year"] = d.Date.str[:4].astype(int)
    rows = []
    for _, r in d.iterrows():
        a = r["Assets"]
        rows.append(dict(date=r.Date, year=r.year, group=r.Category,
                         assets_bn=a / 1e3, networth_bn=r["Net worth"] / 1e3,
                         pct_assets_db=100 * r["DB pension entitlements"] / a,
                         pct_assets_dc=100 * r["DC pension entitlements"] / a,
                         pct_assets_realestate=100 * r["Real estate"] / a,
                         pct_assets_equities_mf=100 * r["Corporate equities and mutual fund shares"] / a,
                         pct_assets_business=100 * r["Unincorporated businesses"] / a,
                         pct_assets_other=100 * (r["Other assets"] + r["Consumer durables"]) / a,
                         dc_share_of_db_plus_dc=100 * r["DC pension entitlements"] / (r["DB pension entitlements"] + r["DC pension entitlements"])))
    out = pd.DataFrame(rows).round(2)
    out.to_csv(OUT / "official_fed_dfa_pensions_by_age.csv", index=False)
    return out


if __name__ == "__main__":
    import sys
    if "--skip-bls" not in sys.argv:
        print(bls_lfpr().tail(8))
    print(bea_ss().tail(3))
    x = dfa_age()
    print(x[x.group.isin(["age70plus", "age55to69"])].iloc[::8])
