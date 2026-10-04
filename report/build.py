"""Concatenate report/parts -> output/Retirement account withdrawal trends.html (standalone)."""
import os
base=os.path.dirname(os.path.abspath(__file__)); root=os.path.dirname(base)
parts=[open(os.path.join(base,'parts',f),encoding='utf-8').read() for f in ['10-head.html','20-body.html','30-script.html']]
head,rest=parts[0],'\n'.join(parts[1:])
standalone=('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
 '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
 '<style>[hidden]{display:none!important}body{margin:0}img{max-width:100%}</style>\n'
 +head+'</head>\n<body>\n'+rest+'\n</body>\n</html>\n')
out=os.path.join(root,'output','Retirement account withdrawal trends.html')
os.makedirs(os.path.dirname(out),exist_ok=True)
open(out,'w',encoding='utf-8').write(standalone); print('built',len(standalone),'bytes ->',out)
# Artifact body (no doctype; the Artifact host wraps it). Publish this file to the live artifact URL.
body=os.path.join(base,'index.html')
open(body,'w',encoding='utf-8').write(head+'\n'+rest+'\n'); print('built',body)
