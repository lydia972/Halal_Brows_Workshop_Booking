import cv2,json,sys
cap=cv2.VideoCapture(sys.argv[1]);fps=cap.get(5)
cc=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
out=[];i=0
while True:
    ok,f=cap.read()
    if not ok:break
    if i%6==0:
        g=cv2.cvtColor(cv2.resize(f,(960,540)),cv2.COLOR_BGR2GRAY)
        fs=cc.detectMultiScale(g,1.1,5,minSize=(100,100))
        if len(fs):
            x,y,w,h=max(fs,key=lambda r:r[2]*r[3]); out.append([round(i/fps,2),int((x+w/2)*2),int((y+h/2)*2),int(w*2),int(h*2)])
        else: out.append([round(i/fps,2),None,None,None,None])
    i+=1
json.dump(out,open('face.json','w'))
import statistics as st
v=[o for o in out if o[1]]
print(len(out),len(v)); print('x',min(o[1] for o in v),st.median(o[1] for o in v),max(o[1] for o in v)); print('y',min(o[2] for o in v),st.median(o[2] for o in v),max(o[2] for o in v)); print('w',st.median(o[3] for o in v))
for o in out[::25]: print(o)
