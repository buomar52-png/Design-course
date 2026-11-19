import numpy as np, wave, sys
from scipy.signal import butter, sosfilt
SR=48000; DUR=21.6; N=int(SR*DUR)
rng=np.random.default_rng(3)
L=np.zeros(N); Rch=np.zeros(N)
def bp(x,lo,hi): return sosfilt(butter(2,[lo,hi],btype='band',fs=SR,output='sos'),x)
def lp(x,f): return sosfilt(butter(2,f,btype='low',fs=SR,output='sos'),x)
def hp(x,f): return sosfilt(butter(2,f,btype='high',fs=SR,output='sos'),x)
def add(t,sig,gain_db=0,pan=0.0):
    g=10**(gain_db/20); i=int(t*SR); n=min(len(sig),N-i)
    if n<=0: return
    pl=np.cos((pan+1)*np.pi/4); pr=np.sin((pan+1)*np.pi/4)
    if sig.ndim==1: L[i:i+n]+=sig[:n]*g*pl*1.41; Rch[i:i+n]+=sig[:n]*g*pr*1.41
    else: L[i:i+n]+=sig[0,:n]*g; Rch[i:i+n]+=sig[1,:n]*g
def norm(x): return x/ (np.max(np.abs(x))+1e-9)
def whoosh(d=0.7,peak=0.6,lo=250,hi=4500):
    n=int(d*SR); t=np.linspace(0,1,n); w=rng.standard_normal(n)
    bands=[bp(w,lo,lo*2.5),bp(w,lo*2.5,lo*6),bp(w,lo*6,hi)]
    out=np.zeros(n)
    for k,b in enumerate(bands):
        c=peak-0.18+k*0.18; out+=norm(b)*np.exp(-((t-c)/0.22)**2)*(1-0.25*k)
    env=np.where(t<peak,(t/peak)**2,np.exp(-(t-peak)/(1-peak)*4))
    s=norm(out*env); pan=np.linspace(-0.7,0.7,n)
    return np.vstack([s*np.cos((pan+1)*np.pi/4)*1.41,s*np.sin((pan+1)*np.pi/4)*1.41])
def scratch(d=0.9,density=40):
    n=int(d*SR); w=hp(bp(rng.standard_normal(n),1800,7000),1500)
    env=np.zeros(n); k=0
    while k<n:
        g=int(SR*rng.uniform(0.008,0.03)); e=np.hanning(min(g,n-k))*rng.uniform(0.3,1)
        env[k:k+len(e)]+=e; k+=int(SR/density*rng.uniform(0.5,1.5))
    fade=np.minimum(1,np.minimum(np.arange(n)/(0.05*SR),(n-np.arange(n))/(0.12*SR)))
    return norm(w*env*fade)
def tick(f=900):
    n=int(0.12*SR); t=np.arange(n)/SR
    s=np.sin(2*np.pi*f*t)*np.exp(-t*55)+0.6*np.sin(2*np.pi*f*2.3*t)*np.exp(-t*90)
    c=bp(rng.standard_normal(n),2000,6000)*np.exp(-t*300)*0.8
    return norm(s+c)
def thud():
    n=int(0.7*SR); t=np.arange(n)/SR; f=45+80*np.exp(-t*18)
    s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)
    c=lp(rng.standard_normal(n),900)*np.exp(-t*40)*0.6
    return norm(s+c)
def boom(d=2.0):
    n=int(d*SR); t=np.arange(n)/SR
    s=np.sin(2*np.pi*48*t)*np.exp(-t*2.2)*np.minimum(1,t/0.02)
    s+=lp(rng.standard_normal(n),220)*np.exp(-t*3)*0.5
    return norm(s)
def swell(d=0.9):
    n=int(d*SR); t=np.linspace(0,1,n)
    s=bp(rng.standard_normal(n),180,1400)*(t**2)*np.exp(-np.maximum(0,t-0.85)*30)
    return norm(s)
def paper(d=0.35):
    n=int(d*SR); t=np.linspace(0,1,n)
    s=bp(rng.standard_normal(n),1200,9000)*np.sin(np.pi*t)**1.5
    return norm(s)

# ---- الجدول الزمني ----
add(0.00,boom(1.6),-15)
add(0.02,paper(0.4),-24,0.2)
add(0.80,tick(760),-22,-0.1); add(1.28,tick(980),-21,0.1)
add(1.55,whoosh(0.75,0.55),-14)
add(1.95,swell(0.9),-24,0.6)
add(1.88,tick(1200),-24)
add(3.00,scratch(0.6),-27,-0.1)
add(3.40,tick(1300),-23)
add(3.70,tick(700),-19,0.35); add(3.75,scratch(0.8),-27,0.3)
add(6.72,tick(820),-19,-0.35); add(6.78,scratch(0.7),-27,-0.3)
add(7.85,whoosh(0.7,0.5),-14)
add(8.10,swell(1.1),-23,0.4)
add(8.25,scratch(0.9),-25,0)
add(9.40,scratch(0.6),-27,0)
add(9.90,tick(1400),-22)
add(12.60,tick(900),-24)
add(12.72,whoosh(0.75,0.55),-14)
add(15.22,whoosh(0.75,0.55),-14)
add(15.45,swell(0.8),-24,0.5)
add(15.55,scratch(0.6),-26)
add(16.15,whoosh(0.45,0.8,900,7000),-20,0.5)
add(16.55,thud(),-19)
add(17.92,whoosh(0.9,0.55),-13)
add(18.25,boom(2.4),-16)
add(18.05,swell(1.0),-22,0.5)
add(18.40,scratch(1.9,60),-23,0.45)
add(18.55,tick(900),-21); add(18.90,tick(1150),-20)
add(19.60,tick(680),-18); add(19.70,scratch(0.7),-24,-0.2)
add(20.55,whoosh(0.8,0.45,600,8000),-18)
add(21.15,tick(1500),-24)

# نسيم رياح
w=np.cumsum(rng.standard_normal(N)); w=hp(w,40); w=lp(w,700); w=norm(w)
w2=np.cumsum(rng.standard_normal(N)); w2=lp(hp(w2,40),700); w2=norm(w2)
t=np.arange(N)/SR
lfo=0.6+0.4*np.sin(2*np.pi*0.13*t+1)*np.sin(2*np.pi*0.07*t)
lvl=np.where(t<18.0,10**(-34/20),10**(-27/20))
lvl=np.convolve(lvl,np.ones(SR)/SR,mode='same')
fade=np.minimum(1,np.minimum(t/1.0,(DUR-t)/0.9))
L+=w*lfo*lvl*fade; Rch+=w2*lfo*lvl*fade
# تلاشي ختامي
fo=np.minimum(1,(DUR-t)/0.9); L*=fo; Rch*=fo
pk=max(np.abs(L).max(),np.abs(Rch).max()); print('peak',pk)
st=np.vstack([L,Rch]).T; st=st/max(1,pk/0.89)
with wave.open(sys.argv[1],'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((st*32767).astype(np.int16).tobytes())
