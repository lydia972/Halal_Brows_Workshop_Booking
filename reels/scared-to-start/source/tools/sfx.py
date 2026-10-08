import numpy as np,soundfile as sf
SR=48000;rng=np.random.default_rng(7)
OUT='../hf/reel-scared-business/assets/sfx/'
def norm(x,db):
    x=x/np.max(np.abs(x)); return x*10**(db/20)
def fade(x,a=0.004,r=0.02):
    n=len(x);e=np.ones(n);ia=int(a*SR);ir=int(r*SR)
    e[:ia]=np.linspace(0,1,ia);e[-ir:]=np.linspace(1,0,ir);return x*e
def onepole_lp(x,fc):
    # time-varying cutoff array allowed
    fc=np.broadcast_to(fc,x.shape);y=np.zeros_like(x);s=0.0
    a=np.exp(-2*np.pi*fc/SR)
    for i in range(len(x)): s=(1-a[i])*x[i]+a[i]*s;y[i]=s
    return y
def stereo(x,pan=None):
    return np.stack([x,x],1)
# whoosh: noise through sweeping lowpass+highpass, bell envelope
n=int(0.5*SR);t=np.arange(n)/SR
noise=rng.standard_normal(n)
fc=300+3500*np.sin(np.pi*t/0.5)**2
lp=onepole_lp(onepole_lp(noise,fc),fc)
hp=lp-onepole_lp(lp,120)
env=np.sin(np.pi*np.clip(t/0.5,0,1))**2.2
w=fade(hp*env)
sf.write(OUT+'whoosh.wav',stereo(norm(w,-9)),SR)
# soft whoosh short
n=int(0.3*SR);t=np.arange(n)/SR;noise=rng.standard_normal(n)
fc=500+5000*np.sin(np.pi*t/0.3)**2;lp=onepole_lp(onepole_lp(noise,fc),fc);hp=lp-onepole_lp(lp,200)
sf.write(OUT+'swish.wav',stereo(norm(fade(hp*np.sin(np.pi*t/0.3)**2),-12)),SR)
# impact: sub drop sine + soft body, no click
n=int(0.7*SR);t=np.arange(n)/SR
f=48+70*np.exp(-t*18);ph=2*np.pi*np.cumsum(f)/SR
body=np.sin(ph)*np.exp(-t*5.5)
thump=onepole_lp(rng.standard_normal(n),900)*np.exp(-t*40)*0.6
x=fade(body+thump,0.002,0.05)
sf.write(OUT+'impact.wav',stereo(norm(x,-6)),SR)
# pop: short sine blip downward
n=int(0.12*SR);t=np.arange(n)/SR
f=900*np.exp(-t*9)+300;x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*38)
sf.write(OUT+'pop.wav',stereo(norm(fade(x,0.002,0.02),-12)),SR)
# tick/ding for checklist: two partial bell
n=int(0.45*SR);t=np.arange(n)/SR
x=(np.sin(2*np.pi*1320*t)+0.4*np.sin(2*np.pi*2640*t)+0.2*np.sin(2*np.pi*3960*t))*np.exp(-t*11)
sf.write(OUT+'ding.wav',stereo(norm(fade(x,0.002,0.05),-15)),SR)
# riser: filtered noise rising 1.2s
n=int(1.2*SR);t=np.arange(n)/SR;noise=rng.standard_normal(n)
fc=200+6000*(t/1.2)**2;lp=onepole_lp(onepole_lp(noise,fc),fc);hp=lp-onepole_lp(lp,150)
x=fade(hp*(t/1.2)**1.6,0.01,0.03)
sf.write(OUT+'riser.wav',stereo(norm(x,-14)),SR)
print('ok')
