import json,re
from score import audio,sr
from pocketsphinx import Decoder
segs=json.load(open('segments.json'))
# corrected display text per segment index (None = cut: filler/noise)
T={0:"You want it so bad.",1:"You want this.",2:"Independence.",
3:"Having your own money, be able to buy the stuff you want, traveling,",
4:"take care of your of your loved one, and you know that the only way to do it is",
5:"thanks to starting your own business.",6:"Maybe you are terrified,",7:"and this situation",
8:"is blocking you, is stopping you at the moment, and you feel like",
9:"you need to do something, you need some help",10:"to jump, because on yourself,",11:"you cannot.",
12:"You are stuck, you are freezing, and you're just starting to think like, maybe it's not a good idea if I'm scared.",
13:None,14:"But it's not always true. Being scared of starting doesn't mean it's a bad thing.",
15:"Being scared",16:"is just your nervous system",17:"panicking because it doesn't know what's going to happen. And this is",
18:"terrifying.",19:"Because we never know if it's going to work or not.",20:None,
21:"Nobody on this platform can tell you your business is going to work",22:"or not. The only thing we can promise is",
23:"telling you all the things you should do and you have to do to make it work.",24:"But when?",25:"This is not up to us.",
26:"How much?",27:"I can't tell you.",28:"This is not me, this is above.",29:"He knows.",
30:"But the only thing we can do is to start and keep going.",31:"Keep posting.",32:"Keep learning.",
33:"Keep looking for clients, keep working on your dream.",34:"I'm telling you a big thing.",
35:"So know, you can start being scared, starting something new.",36:"You will never wake up one morning",
37:"and feel ready.",38:"It's never gonna happen, it never happened to anyone.",39:"All the ones you have seen here, me included.",
40:"I started with the fear.",41:"We all start with this.",42:"It's part of the game."}
def norm(w): return re.sub(r"[^a-z']","",w.lower())
words=[]
for i,s in enumerate(segs):
    t=T[i]
    if t is None: continue
    a=max(0,s['start']-0.2); b=min(len(audio)/sr,s['end']+0.2)
    disp=t.split()
    d=Decoder(bestpath=False,loglevel='FATAL'); d.set_align_text(' '.join(norm(w) for w in disp))
    d.start_utt(); d.process_raw(audio[int(a*sr):int(b*sr)].tobytes(),full_utt=True); d.end_utt()
    al=[x for x in d.seg() if x.word not in('<sil>','(NULL)','<s>','</s>') and not x.word.startswith('+')]
    if len(al)!=len(disp): print("MISMATCH",i,len(al),len(disp),[x.word for x in d.seg()]); 
    for w,x in zip(disp,al):
        words.append({'text':w,'start':round(a+x.start_frame/100,3),'end':round(a+(x.end_frame+1)/100,3),'seg':i})
json.dump(words,open('words.json','w'),indent=0)
for w in words: print(w['seg'],w['start'],w['end'],w['text'])
