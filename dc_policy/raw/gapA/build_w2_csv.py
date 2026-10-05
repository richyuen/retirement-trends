import pandas as pd,re
def blocks(df):
    out=[];cur=None
    for i in range(len(df)):
        c0=df.iloc[i,0]
        s=str(c0) if not pd.isna(c0) else ''
        m=re.search(r'Table 3\.[AC]\..*Tax Year (\d{4})',s.replace('\n',' '))
        if m: cur={'year':int(m.group(1)),'rows':[]}; out.append(cur); continue
        if cur is None: continue
        v=df.iloc[i,1]
        if s.startswith('[') or s.startswith('NOTE') or s.startswith('SOURCE'): 
            continue
        try: tot=float(v)
        except: continue
        if pd.isna(tot): continue
        lab=s.strip() or 'All taxpayers with wage income'
        if lab=='Total': continue
        vals=[df.iloc[i,j] for j in range(1,14)]
        if any(isinstance(x,str) for x in vals): continue
        cur['rows'].append((lab,vals))
    return out
res=[]
src={'w2_0818.xls':'https://www.irs.gov/pub/irs-soi/18inallw2.xls','w2_19_03.xlsx':'https://www.irs.gov/pub/irs-soi/19in03w2all.xlsx','w2_20_03.xlsx':'https://www.irs.gov/pub/irs-soi/20in03w2all.xlsx'}
for f,u in src.items():
    for tab,dim in [('Table 3.C','age'),('Table 3.A','wage income size')]:
        df=pd.read_excel(f,sheet_name=tab,header=None)
        for b in blocks(df):
            for lab,v in b['rows']:
                tot=v[0]; nc_noer,nc_er,c_noer,c_er,anyx,er=v[1],v[3],v[5],v[7],v[9],v[11]
                res.append(dict(year=b['year'],dimension=dim if lab!='All taxpayers with wage income' else 'all',group=lab.replace('\n',' '),taxpayers_with_wages=int(tot),
                  with_elective_deferral=int(er),pct_with_elective_deferral=round(100*er/tot,1),
                  rp_box_checked=int(c_noer+c_er),pct_rp_box_checked=round(100*(c_noer+c_er)/tot,1),
                  rp_box_or_deferral=int(anyx),pct_rp_box_or_deferral=round(100*anyx/tot,1),
                  pct_box_checked_without_deferral=round(100*c_noer/tot,1),
                  source=f'IRS SOI Form W-2 statistics, {tab} (TY{b["year"]}), {u}'))
r=pd.DataFrame(res).drop_duplicates(['year','dimension','group'])
r=r.sort_values(['dimension','group','year'])
r.to_csv('w2_parsed.csv',index=False)
print(r[r.dimension=='all'].to_string())
print(r[r.dimension=='age'].pivot(index='year',columns='group',values='pct_with_elective_deferral').to_string())
print(r[r.dimension=='wage income size'].group.unique())
