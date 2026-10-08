import re,subprocess,json,numpy as np,soundfile as sf,sys
from moonshine_onnx import MoonshineOnnxModel, load_tokenizer
audio,sr=sf.read('audio16k.wav',dtype='float32')
dur=len(audio)/sr
out=subprocess.run(['ffmpeg','-i','audio16k.wav','-af','silencedetect=n=-35dB:d=0.25','-f','null','-'],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)]
en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]
sil=list(zip(st,en))
# speech segments
segs=[];prev=0.0
for s,e in sil:
    if s-prev>0.15: segs.append([prev,s])
    prev=e
if dur-prev>0.15: segs.append([prev,dur])
m=MoonshineOnnxModel(models_dir='package/dist/model/tiny/quantized',model_name='tiny')
tok=load_tokenizer()
res=[]
for a,b in segs:
    x=audio[int(max(0,a-0.1)*sr):int(min(dur,b+0.1)*sr)][None,:]
    t=tok.decode_batch(m.generate(x,max_len=int((b-a)*8)+10))[0]
    res.append({'start':round(a,3),'end':round(b,3),'text':t})
    print(f"{a:7.2f}-{b:7.2f} {t}",flush=True)
json.dump(res,open('segments.json','w'),indent=1)
