import json,os,subprocess,sys,zipfile
import pandas as pd, numpy as np
D=os.path.dirname(os.path.abspath(__file__)); RAW=D+'/raw'; os.makedirs(RAW,exist_ok=True)
B='https://www2.census.gov/programs-surveys/sipp/data/datasets/{y}/{f}'
WANT=['SSUID','PNUM','MONTHCODE','WPFINWGT','TAGE','RMESR','EMJOB_401','ESCNTYN_401','EECNTYN_401','TSCNTAMT_401','TECNTAMT_401',
 'EMJOB_IRA','ESCNTYN_IRA','EECNTYN_IRA','TSCNTAMT_IRA','TECNTAMT_IRA','EPENSNYN','EINCPENS','TSCNTAMT','TECNTAMT','EOWN_THR401','EOWN_IRAKEO',
 'TSCNT401_MED','TECNT401_MED']
MON=['TPEARN']
for y in [int(a) for a in sys.argv[1:]]:
    out=f'{D}/c{y}.parquet'
    if os.path.exists(out): continue
    sp=f'{RAW}/pu{y}_schema.json'
    if not os.path.exists(sp): subprocess.run(['curl','-sS','-f','-o',sp,B.format(y=y,f=f'pu{y}_schema.json')],check=True)
    sch=json.load(open(sp)); names={v['name'] for v in sch}
    dt={v['name']:('object' if v['dtype']=='string' else 'float64') for v in sch}
    cols=set(c for c in WANT+MON if c in names); print(y,'missing',[c for c in WANT+MON if c not in names],flush=True)
    zp=f'{RAW}/pu{y}_csv.zip'
    if not os.path.exists(zp):
        subprocess.run(['curl','-sS','-f','--retry','5','-o',zp+'.part',B.format(y=y,f=f'pu{y}_csv.zip')],check=True); os.rename(zp+'.part',zp)
    z=zipfile.ZipFile(zp); n=[x for x in z.namelist() if x.lower().endswith('.csv')][0]
    parts=[];ms=[]
    for ch in pd.read_csv(z.open(n),sep='|',usecols=lambda c:c.upper() in cols,dtype=str,chunksize=200000):
        ch.columns=[c.upper() for c in ch.columns]; ch=ch.astype({c:dt[c] for c in ch.columns})
        ms.append(ch.groupby(['SSUID','PNUM'])['TPEARN'].agg(['sum','count']).reset_index())
        parts.append(ch[ch.MONTHCODE==12].drop(columns=['TPEARN']))
    df=pd.concat(parts,ignore_index=True)
    m=pd.concat(ms).groupby(['SSUID','PNUM']).sum().reset_index(); m.columns=['SSUID','PNUM','EARN_YR','n_months']
    df=df.merge(m,on=['SSUID','PNUM'],how='left'); df['ref_year']=y-1
    df.to_parquet(out,index=False); os.remove(zp); print(y,'rows',len(df),flush=True)
