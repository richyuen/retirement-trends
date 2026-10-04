"""Tabulate retirement-account withdrawal incidence and rates from the SIPP extract.

Usage: python3 sipp/scripts/tabulate.py [REPS_DIR]   (REPS_DIR default /tmp/sipp/reps, written by extract.py)
Input : sipp/data/sipp_persons_dec.parquet (+ REPS_DIR/rwYYYY_dec.parquet for standard errors)
Output: sipp/output/sipp_estimates_long.csv   every cell, with Fay-BRR standard errors (240 replicates, 4/240 factor)
        sipp/output/sipp_headline_wide.csv    headline table (person level, year-end holders), ref years as columns
        sipp/output/sipp_rmd_single_age.csv   IRA withdrawal incidence by single year of age 68-76 (RMD-age check)
If REPS_DIR is missing, SEs are left blank.
"""
import os, sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data', 'sipp_persons_dec.parquet')
OUT = os.path.join(HERE, '..', 'output')
REPS = sys.argv[1] if len(sys.argv) > 1 else '/tmp/sipp/reps'
NREP, FAY = 240, 4.0 / 240.0
BANDS = {'55-59': (55, 59), '60-64': (60, 64), '65-69': (65, 69), '70-74': (70, 74), '75-79': (75, 79),
         '80+': (80, 200), '60+': (60, 200), '65+': (65, 200), '60-69': (60, 69), '70+': (70, 200)}
os.makedirs(OUT, exist_ok=True)


# ---------------------------------------------------------------- data
def load():
    d = pd.read_parquet(DATA)
    d = d[(d.WPFINWGT > 0) & (d.TAGE_EHC >= 15)].copy()
    d['age'] = d.TAGE_EHC
    d['w'] = d.WPFINWGT
    z = lambda c: d[c].fillna(0).clip(lower=0)
    d['ira_bal'], d['dc_bal'] = z('TIRAKEOVAL'), z('TTHR401VAL')
    d['ira_own'], d['dc_own'] = d.EOWN_IRAKEO.eq(1), d.EOWN_THR401.eq(1)
    d['ira_ye'] = d.ira_own & (d.ira_bal > 0)          # year-end holder (balance > 0 on Dec 31 of ref year)
    d['dc_ye'] = d.dc_own & (d.dc_bal > 0)
    d['ira_wd'] = d.ira_own & d.EIRA_INC_YN.eq(1)
    d['dc_wd'] = d.dc_own & d.ETHR_INC_YN.eq(1)
    d['ira_amt'] = np.where(d.ira_wd, z('TIRA_INC_AMT'), 0.0)
    d['dc_amt'] = np.where(d.dc_wd, z('TTHR_INC_AMT'), 0.0)
    d['any_own'] = d.ira_own | d.dc_own
    d['any_ye'] = d.ira_ye | d.dc_ye
    d['any_wd'] = d.ira_wd | d.dc_wd
    d['any_amt'] = d.ira_amt + d.dc_amt
    # Topcoding sensitivity: topcoded withdrawal amounts carry the mean of the topcoded values (one group per file
    # for TIRA_INC_AMT and TTHR_INC_AMT, identified as the file maximum). Variant: replace by the published median of
    # the topcoded values (TIRA_INC_MED / TTHR_INC_MED).
    for a, v, med in (('ira', 'TIRA_INC_AMT', 'TIRA_INC_MED'), ('dc', 'TTHR_INC_AMT', 'TTHR_INC_MED')):
        top = d.groupby('sipp_year')[v].transform('max')
        tc = d[v].eq(top) & d[v].notna() & d[a + '_wd']
        d[a + '_tc'] = tc
        d[a + '_amtm'] = np.where(tc, d.groupby('sipp_year')[med].transform('max'), d[a + '_amt'])
    d['any_amtm'] = d.ira_amtm + d.dc_amtm
    d['any_tc'] = d.ira_tc | d.dc_tc
    d['any_bal'] = d.ira_bal + d.dc_bal
    # SIPP 2021 (ref 2020) asked the withdrawal items only of owners the instrument classed as retired (NOW_RET=1,
    # which equals EEVERET=1 on the file); other owners are blank. 'asked' = item answered or not applicable.
    d['ira_asked'] = ~(d.ira_own & d.EIRA_INC_YN.isna())
    d['dc_asked'] = ~(d.dc_own & d.ETHR_INC_YN.isna())
    d['any_asked'] = d.ira_asked & d.dc_asked
    d['retired'] = d.EEVERET.eq(1)
    # DC lump sums are asked earlier (programs section) and excluded from ETHR_INC_YN ("excluding any lump sum
    # payments reported earlier"). Sensitivity: add a pension/retirement-plan lump sum that was not rolled over.
    d['lump_nr'] = d.ELMPTYP1YN.eq(1) & ~d.EROLLOVR1.eq(1)
    d['dcl_wd'] = d.dc_wd | (d.dc_own & d.lump_nr)
    # Pre-2021 combined item (SIPP 2018-2020 only; asked of account/pension holders aged 59+ in December)
    d['br_wd'] = d.ERET_LUMPSUM.isin([1, 2, 3])
    d['br_amt'] = d.TDRAW_AMT.fillna(0).clip(lower=0)
    # status flags: 0 not in universe, 1 as reported, 2-8 imputed (hot deck, logical, model, cold deck, range)
    d['imp_ira'] = d.AIRA_INC_YN.fillna(0).gt(1)
    d['imp_dc'] = d.ATHR_INC_YN.fillna(0).gt(1)
    return d


def attach_reps(d):
    parts = []
    for y in sorted(d.sipp_year.unique()):
        p = os.path.join(REPS, f'rw{y}_dec.parquet')
        if not os.path.exists(p):
            return None
        r = pd.read_parquet(p)
        r['sipp_year'] = y
        parts.append(r)
    r = pd.concat(parts, ignore_index=True)
    reps = [f'REPWGT{i}' for i in range(1, NREP + 1)]
    m = d[['SSUID', 'PNUM', 'sipp_year']].merge(r[['SSUID', 'PNUM', 'sipp_year', 'REPWGT0'] + reps],
                                                on=['SSUID', 'PNUM', 'sipp_year'], how='left')
    assert len(m) == len(d)
    miss = m.REPWGT0.isna().mean()
    print(f'replicate weights attached; missing for {miss:.4%} of rows; REPWGT0 vs WPFINWGT max abs diff',
          float(np.nanmax(np.abs(m.REPWGT0.values - d.w.values))))
    R = np.array(m[reps].to_numpy(dtype='float64'), copy=True)
    R[np.isnan(R)] = 0.0
    return R


def household(d, R):
    """Household = SSUID+ERESIDENCEID in December; reference person (ERELRPE 1/2) supplies age and weights."""
    d = d.copy()
    d['hh'] = d.SSUID.astype(str) + '_' + d.ERESIDENCEID.astype(str) + '_' + d.sipp_year.astype(str)
    agg = {c: 'max' for c in ['ira_own', 'dc_own', 'ira_ye', 'dc_ye', 'ira_wd', 'dc_wd', 'any_own', 'any_ye',
                              'any_wd', 'dcl_wd', 'br_wd']}
    agg.update({c: 'min' for c in ['ira_asked', 'dc_asked', 'any_asked']})
    agg.update({c: 'sum' for c in ['ira_bal', 'dc_bal', 'any_bal', 'ira_amt', 'dc_amt', 'any_amt', 'br_amt',
                                   'ira_amtm', 'dc_amtm', 'any_amtm']})
    agg.update({c: 'max' for c in ['ira_tc', 'dc_tc', 'any_tc']})
    h = d.groupby('hh').agg(agg)
    ref = d.ERELRPE.isin([1, 2])
    rp = d.loc[ref, ['hh', 'age', 'w', 'sipp_year', 'ref_year', 'retired']].drop_duplicates('hh')
    idx = np.flatnonzero(ref.to_numpy())
    idx = idx[~d.loc[ref, 'hh'].duplicated().to_numpy()]
    hh = rp.merge(h, left_on='hh', right_index=True, how='left').reset_index(drop=True)
    RH = R[idx] if R is not None else None
    return hh, RH


# ---------------------------------------------------------------- estimators
def wmedian(x, w):
    if len(x) == 0 or w.sum() <= 0:
        return np.nan
    o = np.argsort(x)
    x, w = x[o], w[o]
    c = np.cumsum(w)
    return float(x[np.searchsorted(c, 0.5 * c[-1])])


def est(mask, num_fn, den_fn, w, R, kind='ratio', vals=None):
    """Return (estimate, se) for a ratio sum(w*num)/sum(w*den) or weighted median of vals, over rows in mask."""
    wm = w[mask]
    if kind == 'ratio':
        num, den = num_fn[mask], den_fn[mask]
        e = (wm * num).sum() / (wm * den).sum() if (wm * den).sum() > 0 else np.nan
        if R is None or np.isnan(e):
            return e, np.nan
        Rm = R[mask]
        er = (Rm * num[:, None]).sum(0) / np.where((Rm * den[:, None]).sum(0) > 0, (Rm * den[:, None]).sum(0), np.nan)
    else:
        v = vals[mask]
        e = wmedian(v, wm)
        if R is None or np.isnan(e):
            return e, np.nan
        Rm = R[mask]
        er = np.array([wmedian(v, Rm[:, k]) for k in range(Rm.shape[1])])
    se = np.sqrt(FAY * np.nansum((er - e) ** 2))
    return e, se


def cells(df, R, unit, rows):
    w = df.w.to_numpy(float)
    age = df.age.to_numpy(float)
    ry = df.ref_year.to_numpy()
    accts = {
        'ira': ('ira_ye', 'ira_own', 'ira_wd', 'ira_amt', 'ira_bal'),
        'dc': ('dc_ye', 'dc_own', 'dc_wd', 'dc_amt', 'dc_bal'),
        'any': ('any_ye', 'any_own', 'any_wd', 'any_amt', 'any_bal'),
    }
    A = {c: df[c].to_numpy() for c in df.columns if c not in ('hh', 'SSUID')}
    for y in sorted(np.unique(ry)):
        for band, (lo, hi) in BANDS.items():
            inb = (ry == y) & (age >= lo) & (age <= hi)
            for (acct, (ye, own, wd, amt, bal)), variant in [(a, v) for a in accts.items() for v in ('', '_retired')]:
                if y >= 2020:
                    asked = A[acct + '_asked'].astype(bool)
                    H, O = A[ye].astype(bool) & inb & asked, A[own].astype(bool) & inb & asked
                    if variant:
                        H, O = H & A['retired'].astype(bool), O & A['retired'].astype(bool)
                    WD, AMT, BAL = A[wd].astype(float), A[amt].astype(float), A[bal].astype(float)
                    AMTM, TC = A[acct + '_amtm'].astype(float), A[acct + '_tc'].astype(float)
                    if H.sum() == 0:
                        continue

                    def put(holder, measure, mask, kind='ratio', num=None, den=None, vals=None, scale=100.0):
                        e, s = est(mask, num, den, w, R, kind, vals)
                        rows.append(dict(ref_year=y, sipp_year=y + 1, unit=unit, account=acct, holders=holder + variant,
                                         age_band=band, measure=measure, estimate=e * scale, se=s * scale,
                                         n=int(mask.sum())))
                    one = np.ones(len(w))
                    put('yearend', 'holders_millions', H, num=one, den=one * 0 + 1, scale=1.0)
                    rows[-1]['estimate'] = w[H].sum() / 1e6
                    rows[-1]['se'] = np.sqrt(FAY * ((R[H].sum(0) - w[H].sum()) ** 2).sum()) / 1e6 if R is not None else np.nan
                    put('yearend', 'incidence_per100', H, num=WD, den=one)
                    put('anytime', 'incidence_per100', O, num=WD, den=one)
                    put('yearend', 'rate_all_holders_pct', H, num=AMT, den=BAL)
                    Wd = H & (WD > 0)
                    if Wd.sum() >= 1:
                        put('yearend', 'rate_withdrawers_dollar_pct', Wd, num=AMT, den=BAL)
                        put('yearend', 'rate_withdrawers_median_pct', Wd, kind='median', vals=AMT / np.maximum(BAL, 1))
                    if variant:
                        continue
                    put('yearend', 'rate_all_holders_topcode_median_pct', H, num=AMTM, den=BAL)
                    if Wd.sum() >= 1:
                        put('yearend', 'rate_withdrawers_dollar_topcode_median_pct', Wd, num=AMTM, den=BAL)
                        put('yearend', 'withdrawers_topcoded_amount_pct', Wd, num=TC, den=one)
                        put('yearend', 'median_withdrawal_usd', Wd, kind='median', vals=AMT, scale=1.0)
                        put('yearend', 'median_balance_withdrawers_usd', Wd, kind='median', vals=BAL, scale=1.0)
                    put('yearend', 'median_balance_holders_usd', H, kind='median', vals=BAL, scale=1.0)
                    put('yearend', 'withdrawals_billions', H, num=AMT, den=one, scale=1.0)
                    rows[-1]['estimate'] = (w[H] * AMT[H]).sum() / 1e9
                    rows[-1]['se'] = np.sqrt(FAY * (((R[H] * AMT[H][:, None]).sum(0) - (w[H] * AMT[H]).sum()) ** 2).sum()) / 1e9 if R is not None else np.nan
                    # emptied accounts: owners during year with zero year-end balance, share of withdrawers
                    Wo = O & (WD > 0)
                    if Wo.sum() >= 1:
                        put('anytime', 'withdrawers_zero_yearend_balance_pct', Wo, num=(BAL <= 0).astype(float), den=one)
                    if acct == 'dc':
                        put('yearend', 'incidence_incl_nonrolled_lumpsum_per100', H, num=A['dcl_wd'].astype(float), den=one)
                    if unit == 'person' and acct in ('ira', 'dc'):
                        imp = A['imp_' + acct].astype(float)
                        put('yearend', 'wd_item_imputed_pct', H, num=imp, den=one)
                elif acct == 'any' and lo >= 60 and not variant:
                    # SIPP 2018-2020 (ref 2017-2019): combined item ERET_LUMPSUM, all plan types incl. DB
                    H = A['any_ye'].astype(bool) & inb
                    one = np.ones(len(w))
                    for measure, num, den in [('bridge_any_plan_dist_per100', A['br_wd'].astype(float), one),
                                              ('bridge_tdraw_rate_pct', A['br_amt'].astype(float), A['any_bal'].astype(float))]:
                        if measure == 'bridge_tdraw_rate_pct' and y == 2017:
                            continue  # TDRAW_AMT not on the SIPP 2018 file
                        e, s = est(H, num, den, w, R)
                        rows.append(dict(ref_year=y, sipp_year=y + 1, unit=unit, account='any_incl_db', holders='yearend',
                                         age_band=band, measure=measure, estimate=e * 100, se=s * 100, n=int(H.sum())))


def linked(d, R, rows):
    """Withdrawals in t / balance on Dec 31 of t-1, for people interviewed in both SIPP t and SIPP t-1 (same panel).
    Universe: year-end holders in t-1 who still report owning that account type at some time in t (includes those
    who emptied it in t). Weight: year-t final weight (not re-weighted for panel attrition)."""
    prev = d[['SSUID', 'PNUM', 'SPANEL', 'sipp_year', 'ira_ye', 'dc_ye', 'any_ye', 'ira_bal', 'dc_bal', 'any_bal']].copy()
    prev['sipp_year'] += 1
    prev.columns = [c if c in ('SSUID', 'PNUM', 'SPANEL', 'sipp_year') else 'p_' + c for c in prev.columns]
    d = d.reset_index(drop=True)
    m = d.merge(prev, on=['SSUID', 'PNUM', 'SPANEL', 'sipp_year'], how='left')
    assert len(m) == len(d)
    ok = m.p_any_bal.notna().to_numpy()
    w = m.w.to_numpy(float); age = m.age.to_numpy(float); ry = m.ref_year.to_numpy()
    for y in sorted(np.unique(ry[ok])):
        if y < 2020:
            continue
        for band, (lo, hi) in BANDS.items():
            inb = ok & (ry == y) & (age >= lo) & (age <= hi)
            for acct in ('ira', 'dc', 'any'):
                # also require ownership at some point in t (keeps accounts emptied in t; drops ownership-report churn,
                # where an owner in t-1 says 'no account' in t and is never asked the withdrawal item)
                H = (inb & m['p_' + acct + '_ye'].fillna(False).to_numpy(bool) & m[acct + '_asked'].to_numpy(bool)
                     & m[acct + '_own'].to_numpy(bool))
                if H.sum() == 0:
                    continue
                WD = m[acct + '_wd'].to_numpy(float); AMT = m[acct + '_amt'].to_numpy(float)
                PB = m['p_' + acct + '_bal'].to_numpy(float); one = np.ones(len(w))
                for measure, mask, kind, num, den, vals in [
                        ('incidence_per100', H, 'ratio', WD, one, None),
                        ('rate_all_holders_pct', H, 'ratio', AMT, PB, None),
                        ('rate_withdrawers_dollar_pct', H & (WD > 0), 'ratio', AMT, PB, None),
                        ('rate_withdrawers_median_pct', H & (WD > 0), 'median', None, None, AMT / np.maximum(PB, 1))]:
                    if mask.sum() == 0:
                        continue
                    e, s = est(mask, num, den, w, R, kind, vals)
                    rows.append(dict(ref_year=y, sipp_year=y + 1, unit='person', account=acct,
                                     holders='linked_prior_yearend', age_band=band, measure=measure,
                                     estimate=e * 100, se=s * 100, n=int(mask.sum())))


def single_age(d, R):
    rows = []
    w = d.w.to_numpy(float); age = d.age.to_numpy(); ry = d.ref_year.to_numpy()
    for y in sorted(np.unique(ry)):
        if y < 2020:
            continue
        for a in range(68, 77):
            for acct in ('ira', 'any'):
                H = (ry == y) & (age == a) & d[acct + '_ye'].to_numpy(bool) & d[acct + '_asked'].to_numpy(bool)
                e, s = est(H, d[acct + '_wd'].to_numpy(float), np.ones(len(w)), w, R)
                rows.append(dict(ref_year=y, age=a, account=acct, incidence_per100=e * 100, se=s * 100, n=int(H.sum())))
    return pd.DataFrame(rows)


if __name__ == '__main__':
    d = load().reset_index(drop=True)
    R = attach_reps(d)
    rows = []
    cells(d, R, 'person', rows)
    linked(d, R, rows)
    hh, RH = household(d, R)
    cells(hh, RH, 'household', rows)
    long = pd.DataFrame(rows)
    long['estimate'] = long.estimate.round(4); long['se'] = long.se.round(4)
    long.to_csv(os.path.join(OUT, 'sipp_estimates_long.csv'), index=False)
    sa = single_age(d, R)
    sa.round(3).to_csv(os.path.join(OUT, 'sipp_rmd_single_age.csv'), index=False)

    # headline wide: person level, year-end holders
    mlist = ['incidence_per100', 'rate_all_holders_pct', 'rate_all_holders_topcode_median_pct',
             'rate_withdrawers_dollar_pct', 'rate_withdrawers_dollar_topcode_median_pct', 'rate_withdrawers_median_pct',
             'bridge_any_plan_dist_per100']
    sel = long[(long.unit == 'person') & (long.holders == 'yearend') & long.measure.isin(mlist)]
    order_m = {m: i for i, m in enumerate(mlist)}
    order_a = {'ira': 0, 'dc': 1, 'any': 2, 'any_incl_db': 3}
    est_w = sel.pivot_table(index=['measure', 'account', 'age_band'], columns='ref_year', values='estimate')
    se_w = sel.pivot_table(index=['measure', 'account', 'age_band'], columns='ref_year', values='se')
    se_w.columns = [f'se_{c}' for c in se_w.columns]
    wide = est_w.round(1).join(se_w.round(1)).reset_index()
    wide['_m'] = wide.measure.map(order_m); wide['_a'] = wide.account.map(order_a)
    wide['_b'] = wide.age_band.map({b: i for i, b in enumerate(BANDS)})
    wide = wide.sort_values(['_m', '_a', '_b']).drop(columns=['_m', '_a', '_b'])
    wide.to_csv(os.path.join(OUT, 'sipp_headline_wide.csv'), index=False)
    print(wide.to_string())
