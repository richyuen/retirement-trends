"""Combined tax-data view: IRA contributions + W-2 elective deferrals, TY2008-2020 (years where both exist).

Reads output/ira_contributions_by_type.csv, output/w2_deferrals_totals.csv, output/w2_deferrals_by_plan_type.csv,
output/f1040_ira_keogh_deduction_long.csv. Writes output/combined_ira_w2_contributions.csv.
Run after f1040_long.py, limits.py, ira_contributions.py, w2_deferrals.py:  python3 -I combined.py
"""
import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'output')

def main():
    ira = pd.read_csv(os.path.join(OUT, 'ira_contributions_by_type.csv'))
    piv = ira.pivot(index='year', columns='ira_type', values='contributions_k')
    cnt = ira.pivot(index='year', columns='ira_type', values='contributors')
    w2 = pd.read_csv(os.path.join(OUT, 'w2_deferrals_totals.csv')).set_index('year')
    pt = pd.read_csv(os.path.join(OUT, 'w2_deferrals_by_plan_type.csv'))
    code = lambda prefix: pt[pt.plan_type.str.startswith(prefix)].set_index('year').amount_k
    f = pd.read_csv(os.path.join(OUT, 'f1040_ira_keogh_deduction_long.csv')).set_index('year')
    yrs = sorted(set(w2.index) & set(piv.index))
    d = pd.DataFrame(index=pd.Index(yrs, name='year'))
    d['trad_roth_ira_k'] = piv['Traditional'] + piv['Roth']
    d['sep_ira_k'] = piv['SEP']; d['simple_ira_k'] = piv['SIMPLE']
    d['w2_elective_deferrals_k'] = w2.deferrals_k
    d['w2_code_F_sep_k'] = code('408(k)(6) SEP'); d['w2_code_S_simple_k'] = code('408(p) SIMPLE')
    d['gross_wages_proxy_k'] = w2.box1_wages_k + w2.pretax_deferrals_k
    d['f1040_wages_k'] = f.wages_k
    d['combined_core_k'] = d.trad_roth_ira_k + d.w2_elective_deferrals_k
    d['combined_broad_k'] = d.combined_core_k + d.sep_ira_k + d.simple_ira_k - d.w2_code_F_sep_k - d.w2_code_S_simple_k
    for c in ('trad_roth_ira_k', 'w2_elective_deferrals_k', 'combined_core_k', 'combined_broad_k'):
        d[c.replace('_k', '') + '_pct_gross_wages'] = (100 * d[c] / d.gross_wages_proxy_k).round(3)
    d['ira_share_of_core_pct'] = (100 * d.trad_roth_ira_k / d.combined_core_k).round(2)
    d['pct_taxpayers_trad_or_roth_ira'] = None
    tt = ira[ira.ira_type == 'All IRA types'].set_index('year')
    d['pct_all_taxpayers_any_ira'] = tt.pct_all_taxpayers_contributing
    d['pct_wage_earners_deferring'] = w2.pct_wage_earners_deferring
    d = d.drop(columns='pct_taxpayers_trad_or_roth_ira')
    d['source'] = ('IRA: IRS SOI IRA Table 1 (YYin01ira); deferrals and wages: IRS SOI Form W-2 statistics Tables 2.A, 5.A/4.B, 7.A/4.D (18inallw2.xls, 19in0Xw2all.xlsx, 20in0Xw2all.xlsx). '
                   'See component CSVs for per-year URLs.')
    d['note'] = ('combined_core = traditional + Roth IRA contributions + all W-2 elective deferrals (employee only; no employer match/nonelective contributions, which are not on the W-2). '
                 'combined_broad adds SEP and SIMPLE IRA contributions (Table 1, which include employer contributions) less W-2 codes F and S to avoid double counting the salary-reduction part. '
                 'Gross wages proxy = W-2 box-1 wages of all W-2 taxpayers on filed returns + pre-tax deferrals. IRA contributions include those of non-wage earners. '
                 'People cannot be de-duplicated across the two sources, so no combined participation rate is computed. TY2003 IRA and TY2021+ W-2 data unavailable.')
    d.reset_index().to_csv(os.path.join(OUT, 'combined_ira_w2_contributions.csv'), index=False)
    show = d[['trad_roth_ira_k', 'w2_elective_deferrals_k', 'trad_roth_ira_pct_gross_wages', 'w2_elective_deferrals_pct_gross_wages', 'combined_core_pct_gross_wages',
              'combined_broad_pct_gross_wages', 'ira_share_of_core_pct', 'pct_all_taxpayers_any_ira', 'pct_wage_earners_deferring']].copy()
    show[['trad_roth_ira_k', 'w2_elective_deferrals_k']] = (show[['trad_roth_ira_k', 'w2_elective_deferrals_k']] / 1e6).round(1)
    print(show.rename(columns={'trad_roth_ira_k': 'IRA$bn', 'w2_elective_deferrals_k': 'W2$bn'}).to_string())

if __name__ == '__main__':
    main()
