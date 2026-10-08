import json,subprocess
W=json.load(open('words.json'))
# drop stutter: first "of your" in seg 4
drop=set()
for i,w in enumerate(W):
    if w['seg']==4 and w['text']=='of' and W[i+1]['text']=='your' and W[i+2]['text']=='of': drop|={i,i+1}
W=[w for i,w in enumerate(W) if i not in drop]
PRE,POST,MAXGAP=0.07,0.13,0.32
ranges=[]
for w in W:
    s,e=w['start']-PRE,w['end']+POST
    if ranges and (w['start']-ranges[-1]['last_end'])<MAXGAP and not w.get('force_cut'):
        ranges[-1]['e']=max(ranges[-1]['e'],e); ranges[-1]['last_end']=w['end']; ranges[-1]['words'].append(w)
    else:
        ranges.append({'s':max(0,s),'e':e,'last_end':w['end'],'words':[w]})
# special: stutter boundary — make the range before "of your loved" end right at end of "care"
# resolve overlaps between ranges (cut in the middle of the gap)
for a,b in zip(ranges,ranges[1:]):
    if a['e']>b['s']:
        m=(a['last_end']+b['words'][0]['start'])/2; a['e']=m; b['s']=m
for r in ranges:
    if r['words'][-1]['text']=='care': r['e']=9.975
    if r['words'][0]['text']=='of' and r['words'][0]['seg']==4: r['s']=10.32
FPS=30
def q(t): return round(t*FPS)/FPS
out=0;cuts=[];words=[]
for r in ranges:
    s,e=q(r['s']),q(r['e'])
    cuts.append({'src':s,'end':e,'out':round(out,4)})
    for w in r['words']:
        words.append({'text':w['text'],'start':round(out+w['start']-s,3),'end':round(out+w['end']-s,3),'src':w['start']})
    out+=e-s
print(len(cuts),'ranges, edited duration',round(out,2))
json.dump({'cuts':cuts,'duration':round(out,4)},open('cuts.json','w'),indent=0)
json.dump(words,open('words_out.json','w'),indent=0)
# ffmpeg
src='../hf/reel-scared-business/assets/source.mp4'
fc=[];n=len(cuts)
for i,c in enumerate(cuts):
    d=c['end']-c['src']
    f0,f1=round(c['src']*30),round(c['end']*30)
    fc.append(f"[0:v]trim=start_frame={f0}:end_frame={f1},setpts=PTS-STARTPTS[v{i}]")
    fc.append(f"[0:a]atrim=start_sample={f0*1470}:end_sample={f1*1470},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={max(0,d-0.015):.4f}:d=0.015[a{i}]")
fc.append(''.join(f"[v{i}][a{i}]" for i in range(n))+f"concat=n={n}:v=1:a=1[v][a]")
open('fc.txt','w').write(';\n'.join(fc))
