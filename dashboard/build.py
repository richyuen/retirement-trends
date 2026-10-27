"""Build the Retirement Trends dashboard data files from the report's chart data.

Reads report/parts/30-script.html (CH object, read-only), writes one JSON file of
rows {year, series, value} per indicator to dashboard/data/, plus
dashboard/datasets.json (titles, descriptions) and dashboard/marks.json (latest and
base cells used by index.html). Run: python dashboard/build.py
"""
import json, os, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(HERE, '..', 'report', 'parts', '30-script.html')
REPORT = 'https://claude.ai/artifact/JTfbBBXQfUrpabgjxiGdqT'


def load_ch():
    lines = open(PARTS, encoding='utf-8').read().split('\n')
    # helpers (pct, usd0, usd1, Y) are lines 8-11; SEG4 and CH run from 180 to the '};' at 442
    end = next(i for i in range(181, len(lines)) if lines[i] == '};')
    js = '\n'.join(lines[7:11] + lines[179:end + 1])
    js += '\nrequire("fs").writeFileSync(process.argv[2], JSON.stringify(CH));\n'
    with tempfile.TemporaryDirectory() as d:
        src, out = os.path.join(d, 'ch.js'), os.path.join(d, 'ch.json')
        open(src, 'w').write(js)
        subprocess.run(['node', src, out], check=True)
        return json.load(open(out))


# id, chart key, series kept {report name: short name}, headline short name,
# base year for "from", min year, breaks (years after which lines don't join),
# unit, dataset title, description, report section id and title
IND = [
    dict(id='ira_incidence', key='agegrp', part='Withdrawals and rollovers',
         series={'RMD age or older': 'RMD age or older', 'Aged 60 to RMD age': '60 to RMD age', 'Aged 18 to 59': '18 to 59'},
         head='RMD age or older', base=None, unit='%',
         title='IRA withdrawal incidence by age',
         desc='Share of traditional IRA investors taking a withdrawal in the year, by age group. ICI IRA Investor Database, Figure A.11; the sample changed in 2017.',
         q='Who takes money out of IRAs?', sec=('s-who', 'IRA withdrawals: who takes them')),
    dict(id='ira_rate', key='dwrate', part='Withdrawals and rollovers',
         series={'Aged 70 or older': '70 or older', 'Aged 60 to 69': '60 to 69', 'All ages': 'All ages'},
         head='70 or older', base='2019', unit='%',
         title='IRA withdrawal rate by age',
         desc='IRA withdrawals as a share of the same age group’s prior year-end balance, all IRA types, dollar-weighted. IRS Statistics of Income Table 4 (computed); 2022-2023 are a new IRS series.',
         q='How much do they take out?', sec=('s-rate', 'IRA withdrawals: how much')),
    dict(id='rollover_share', key='rollshare', part='Withdrawals and rollovers',
         series={'Traditional IRA rollovers ÷ all DC plan outflows (BEA)': 'Rollovers ÷ all DC outflows (BEA)',
                 'Traditional IRA rollovers ÷ private DC plan benefits (Form 5500)': 'Rollovers ÷ private DC benefits (Form 5500)'},
         head='Rollovers ÷ all DC outflows (BEA)', base='1996', unit='%', breaks=['2021'],
         title='Rollovers vs DC plan outflows',
         desc='Rollovers into traditional IRAs (IRS Statistics of Income) as a share of money paid out of DC plans (BEA) and of private DC plan benefits (Form 5500). A ratio of two sources, not a true rollover share; the IRS method changed in 2022.',
         q='Is less money leaving plans for IRAs?', sec=('s-roll', 'Rollovers')),
    dict(id='dc_participation', key='aespread', part='Saving for retirement',
         series={'Private workers participating in a DC plan': 'Participating in a DC plan', 'Private workers with access to a DC plan': 'With access to a DC plan'},
         head='Participating in a DC plan', base='2010', unit='%',
         title='DC plan access and participation',
         desc='Private-industry workers with access to, and participating in, an employer defined contribution plan, March of each year. BLS National Compensation Survey (DC plans only, not the all-plans rate that includes DB).',
         q='Are more workers in a DC plan?', sec=('s-laws', 'Do the laws work?')),
    dict(id='dc_contributions', key='dcwages', part='Saving for retirement',
         series={'DC plans, employer + employee (Form 5500)': 'Total', 'DC plans, employee (Form 5500)': 'Employee', 'DC plans, employer (Form 5500)': 'Employer'},
         head='Total', base='1999', unit='%',
         title='DC contributions vs wages',
         desc='Employer and employee contributions to private DC plans (excluding rollovers) as a share of all private wages and salaries. DOL Form 5500 abstracts divided by BEA private wages (computed).',
         q='How much goes into DC plans?', sec=('s-contrib', 'How much goes in: contribution trends')),
    dict(id='nrri', key='nrri', part='Saving for retirement',
         series={'Version 2.0 (2024)': 'Version 2.0 (2024)', 'Original method (2018)': 'Original method (2018)'},
         head='Version 2.0 (2024)', base='2004', unit='%',
         title='Households at risk (NRRI)',
         desc='Share of working-age households projected to fall more than 10% short of the income needed to keep their consumption in retirement. Center for Retirement Research NRRI; the two methods are not comparable and are never joined.',
         q='Are workers on track?', sec=('s-ready', 'Are workers ready for retirement?')),
    dict(id='income_shares', key='incshare', part='Income in retirement',
         series={'Social Security': 'Social Security', 'Earnings': 'Earnings', 'Defined benefit pensions': 'DB pensions', 'Retirement account withdrawals': 'Account withdrawals'},
         head='Social Security', base=None, extra=['Earnings', 'DB pensions', 'Account withdrawals'], unit='%', breaks=['2013'],
         title='Income sources, 65 or older',
         desc='Share of the aggregate income of people 65 or older by source, CPS ASEC public-use files tabulated for the report. Income years 1997-2013 (traditional questions) and 2016-2025 (redesigned) are separate series; compare levels only within one.',
         q='Where does retirees’ income come from?', sec=('s-income', 'Where retirees’ income comes from')),
    dict(id='ss_runway', key='runway', part='Income in retirement',
         series={'Years until the combined trust funds are projected to run out': 'Years to trust fund depletion'},
         head='Years to trust fund depletion', base='1985', unit='years',
         title='Social Security trust fund runway',
         desc='Years from each Trustees Report to the year the combined OASI and DI trust funds are projected to run out, intermediate assumptions. 2026 Trustees Report Table VI.B1 (computed).',
         q='How long until Social Security’s trust funds run out?', sec=('s-ss', 'Social Security’s finances')),
    dict(id='db_participation', key='dbpart', part='Income in retirement',
         series={'Form 5500 active DB participants ÷ private wage and salary workers': 'Form 5500', 'BLS employer survey, private industry': 'BLS survey'},
         head='Form 5500', base='1980', unit='%',
         title='Private DB pension participation',
         desc='Active participants in private defined benefit plans as a share of private wage and salary workers: Form 5500 (DOL Table E7 over CPS workers, computed) and the BLS employer surveys.',
         q='How many workers still earn a pension?', sec=('s-db', 'The decline of defined benefit pensions')),
    dict(id='annuity_ownership', key='annuity', part='Income in retirement',
         series={'65 or older: any annuity': '65+, any annuity', '55–64: any annuity': '55–64, any annuity', '65 or older: income annuity (no cash value)': '65+, income annuity'},
         head='65+, any annuity', base='2004', unit='%',
         title='Annuity ownership by age',
         desc='Share of households owning an annuity outside an employer pension, by age of the household head. Survey of Consumer Finances 2004-2022, tabulated for the report.',
         q='Do retirees buy lifetime income?', sec=('s-annuity', 'Annuities and lifetime income')),
    dict(id='life_expectancy', key='le65', part='Living longer and working longer',
         series={'Women': 'Women', 'Men': 'Men'},
         head='Women', base=None, extra=['Men'], unit='years',
         title='Life expectancy at 65',
         desc='Period life expectancy at 65 in years, by sex. NCHS Health, United States (1980-2017) and United States Life Tables (2018-2024).',
         q='How long does the money have to last?', sec=('s-long', 'How long the money has to last')),
    dict(id='older_lfpr', key='lfpr', part='Living longer and working longer',
         series={'Aged 62 to 64': '62 to 64', 'Aged 65 to 69': '65 to 69', 'Aged 70 to 74': '70 to 74'},
         head='65 to 69', base='1976', unit='%',
         title='Labor force participation, 62+',
         desc='Labor force participation rate by age, annual averages. BLS Current Population Survey; the 1994 redesign raised measured participation at 65+ by about a point.',
         q='Are people working longer?', sec=('s-work', 'Working longer')),
    dict(id='work_after_claiming', key='workret', part='Living longer and working longer',
         series={'Worked at any time in the previous year': 'Worked in prior year', 'Employed, usually part time': 'Employed part time', 'Employed, usually full time': 'Employed full time'},
         head='Employed part time', base='2010', extra=['Employed full time'], unit='%',
         title='Work after claiming Social Security',
         desc='Retired-worker Social Security beneficiaries 62 or older: share employed in the March survey week by usual hours, and share who worked in the previous year. CPS ASEC public-use files, tabulated for the report.',
         q='Do retirees keep working?', sec=('s-work', 'Working longer')),
    dict(id='medicare_premium', key='premium', part='Living longer and working longer',
         series={'Part B standard premium': 'Part B standard premium'}, minyear=1990,
         head='Part B standard premium', base='1990', unit='%',
         title='Medicare Part B premium burden',
         desc='Standard Medicare Part B premium as a percentage of the average Social Security retired-worker benefit. 2026 Medicare Trustees Report (computed).',
         q='How much of Social Security goes to Medicare premiums?', sec=('s-health', 'Health care costs')),
    dict(id='older_debt', key='olddebt', part='Older households’ finances',
         series={'Head aged 75 or older': '75 or older', 'Head aged 65–74': '65 to 74', 'Head aged 55–64': '55 to 64'},
         head='75 or older', base='1989', unit='%',
         title='Older households with debt',
         desc='Share of households with any debt, by age of the household head. Survey of Consumer Finances 1989-2022, tabulated for the report; matches the Fed’s historical tables.',
         q='Are more older households in debt?', sec=('s-debt', 'Debt and housing wealth in later life')),
    dict(id='poverty_65', key='spm65', part='Older households’ finances',
         series={'Supplemental Poverty Measure': 'Supplemental Poverty Measure', 'Official measure': 'Official measure'},
         head='Supplemental Poverty Measure', base=None, extra=['Official measure'], unit='%', breaks=['2012', '2016', '2018'],
         title='Poverty at 65 or older',
         desc='Poverty rate of people 65 or older on the Supplemental Poverty Measure and the official measure. Census P60-290 and earlier reports; lines break where Census changed questions, processing or SPM method.',
         q='How many older people are poor?', sec=('s-poverty', 'Poverty among older Americans')),
]


def main():
    ch = load_ch()
    os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
    meta = []
    for ind in IND:
        c = ch[ind['key']]
        rows = []
        for s in c['series']:
            if s['name'] not in ind['series']:
                continue
            short = ind['series'][s['name']]
            for x, v in zip(c['x'], s['values']):
                if v is None or int(x) < ind.get('minyear', 0):
                    continue
                rows.append({'year': x, 'series': short, 'value': v})
        missing = set(ind['series']) - {s['name'] for s in c['series']}
        assert not missing, (ind['id'], missing)
        json.dump(rows, open(os.path.join(HERE, 'data', ind['id'] + '.json'), 'w'), ensure_ascii=False)

        def latest(name):
            r = [r for r in rows if r['series'] == name]
            return r[-1]
        head = latest(ind['head'])
        base = None
        if ind.get('base'):
            base = next(r for r in rows if r['series'] == ind['head'] and r['year'] == ind['base'])
        meta.append(dict(id=ind['id'], part=ind['part'], q=ind['q'], unit=ind['unit'], sec=ind['sec'],
                         order=list(ind['series'].values()), breaks=ind.get('breaks', []),
                         head=head, base=base, extra=[latest(e) for e in ind.get('extra', [])],
                         title=ind['title'], desc=ind['desc']))
    json.dump(meta, open(os.path.join(HERE, 'marks.json'), 'w'), ensure_ascii=False, indent=1)
    print('\n'.join(f"{m['id']}: {m['head']} base={m['base']}" for m in meta))


if __name__ == '__main__':
    main()
