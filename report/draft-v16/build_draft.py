"""Build the v16 reorganized draft (not published). Regenerate parts with scratch reorg.py."""
import os
d=os.path.dirname(os.path.abspath(__file__))
parts=[open(os.path.join(d,'parts',f),encoding='utf-8').read() for f in ['10-head.html','20-body.html','30-script.html']]
head,rest=parts[0],'\n'.join(parts[1:])
open(os.path.join(d,'preview.html'),'w',encoding='utf-8').write('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<style>[hidden]{display:none!important}body{margin:0}img{max-width:100%}</style>\n'+head+'</head>\n<body>\n'+rest+'\n</body>\n</html>\n')
open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(head+'\n'+rest+'\n'); print('built draft')
