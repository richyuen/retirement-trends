import pandas as pd,numpy as np,glob
def wq(x,w,q):
    o=np.argsort(x);x=x[o];w=w[o];c=np.cumsum(w)/w.sum();return x[np.searchsorted(c,q)]
rows=[]
for f in sorted(glob.glob('c20*.parquet')):
    d=pd.read_parquet(f);y=int(d.ref_year.iloc[0])
    w=d[(d.TAGE.between(18,64))&(d.EARN_YR>0)&(d.n_months==12)].copy();W=w.WPFINWGT
    has=w.EMJOB_401==1; con=w.ESCNTYN_401==1; er=w.EECNTYN_401==1
    ira=w.ESCNTYN_IRA==1
    c=w[con&(w.EARN_YR>=1000)&w.TSCNTAMT_401.notna()]
    pct=(c.TSCNTAMT_401/c.EARN_YR*100).clip(upper=100).values
    epct=(c.TECNTAMT_401.fillna(0)/c.EARN_YR*100).clip(upper=100).values
    rows.append(dict(year=y,n=len(w),has_dc_main=100*W[has].sum()/W.sum(),contrib_dc=100*W[con].sum()/W.sum(),
      contrib_among_has=100*W[con&has].sum()/W[has].sum(), employer_contrib=100*W[er].sum()/W.sum(),
      contrib_emp_ira=100*W[ira].sum()/W.sum(), n_contrib=len(c),
      med_own_pct=wq(pct,c.WPFINWGT.values,.5), med_er_pct=wq(epct,c.WPFINWGT.values,.5),
      agg_own_pct_contrib=100*(c.TSCNTAMT_401*c.WPFINWGT).sum()/(c.EARN_YR*c.WPFINWGT).sum(),
      agg_er_pct_contrib=100*(c.TECNTAMT_401.fillna(0)*c.WPFINWGT).sum()/(c.EARN_YR*c.WPFINWGT).sum(),
      own_pct_all_wages=100*(w.TSCNTAMT_401.where(con,0).fillna(0)*W).sum()/(w.EARN_YR*W).sum(),
      er_pct_all_wages=100*(w.TECNTAMT_401.where(er,0).fillna(0)*W).sum()/(w.EARN_YR*W).sum()))
r=pd.DataFrame(rows).round(1);print(r.T.to_string());r.to_csv('out.csv',index=False)
