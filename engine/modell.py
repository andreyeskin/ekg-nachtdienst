# -*- coding: utf-8 -*-
"""Wellenmodell + Regel-Klassifikatoren für Kurs A (Lektionen 8–12).
Alles, was gezeichnet wird, kommt aus diesen Funktionen — und dieselben Daten
werden von den Klassifikatoren nach den Buchregeln bewertet (assert beim Bau)."""
import math
def F(x): return f'{x:.1f}'
def hump(t,t0,d,a): return a*math.sin(math.pi*(t-t0)/d) if t0<=t<=t0+d else 0.0
QN=[(0,0),(12,-0.1),(40,1.0),(68,-0.3),(90,0)]
QB=[(0,0),(25,0.3),(55,0.2),(95,0.85),(135,-0.25),(165,0)]
def qrs(t,t0,breit=False):
    P=QB if breit else QN
    if t<t0 or t>t0+P[-1][0]: return 0.0
    for i in range(1,len(P)):
        if t-t0<=P[i][0]:
            a,c=P[i-1],P[i]; return a[1]+(c[1]-a[1])*(t-t0-a[0])/(c[0]-a[0])
    return 0.0
def kurve(t,ps,qs,breit=False,pneg=None,tlag=None,pamp=0.2):
    v=0.0
    for i,p in enumerate(ps):
        neg = pneg[i] if pneg else False
        v+=hump(t,p,90,-pamp*0.8 if neg else pamp)
    for q in qs:
        v+=qrs(t,q,breit)
        if breit: v+=hump(t,q+230,200,-0.3)
        else: v+=hump(t,q+(tlag if tlag else 220),180,0.28)
    return v

# ---------- Regel-Klassifikatoren (Buchregeln) ----------
def sinus_befund(pp):                   # Lektion 8
    diff=max(pp)-min(pp); f=60000/(sum(pp)/len(pp))
    unreg = diff>120
    if f<50: return 'Sinusbradyarrhythmie' if unreg else 'Sinusbradykardie'
    if f>100: return 'Sinustachyarrhythmie' if unreg else 'Sinustachykardie'
    return 'normofrequente Sinusarrhythmie' if unreg else 'regulärer Sinusrhythmus'
def sa_befund(pp):                      # Lektion 9 (+8 für Sinusarrhythmie)
    srt=sorted(pp); med=srt[len(srt)//2]
    rest=[x for x in pp if x!=max(pp)]
    if not rest: return 'regulärer Sinusrhythmus'
    # Typ II: eine Pause = Vielfaches des (sonst konstanten) Grundintervalls
    if max(rest)-min(rest)<=20:
        r=max(pp)/min(rest)
        if r>=1.9 and abs(r-round(r))<0.06: return 'SA-Block II°, Typ II (Mobitz)'
    # Typ I: PP vor der Pause werden zunehmend kürzer, Pause < Summe der zwei vorangehenden
    i=pp.index(max(pp))
    if i>=2 and pp[i-2]>pp[i-1] and max(pp)<pp[i-1]+pp[i-2]: return 'SA-Block II°, Typ I (Wenckebach)'
    return 'Sinusarrhythmie' if max(pp)-min(pp)>120 else 'regulärer Sinusrhythmus'
def av_befund(pqs, dissoziiert=False):  # Lektion 10
    if dissoziiert: return 'AV-Block III°'
    if None not in pqs: return 'AV-Block I°' if min(pqs)>200 and max(pqs)-min(pqs)<=10 else ('normale AV-Überleitung' if max(pqs)<=200 else '?')
    blk=[i for i,x in enumerate(pqs) if x is None]
    if len(pqs)>=4 and all(pqs[i] is None for i in range(1,len(pqs),2)) and all(pqs[i] is not None for i in range(0,len(pqs),2)):
        return 'fortgeschrittener AV-Block II° (2:1)'
    i=blk[0]; vor=[x for x in pqs[:i] if x is not None]
    if len(vor)>=2 and all(vor[k]<vor[k+1] for k in range(len(vor)-1)): return 'AV-Block II°, Typ I (Wenckebach)'
    if len(vor)>=2 and max(vor)-min(vor)<=10: return 'AV-Block II°, Typ II (Mobitz)'
    return '?'
def av3_ort(rr, breit):                  # Lektion 10: proximal 40–60/min schmal, distal <40/min breit
    f=60000/rr
    if (not breit) and 40<=f<=60: return 'proximal (AV-Knoten)'
    if breit and f<40: return 'distal (His-Bündel/Schenkel)'
    return '?'
def pwelle_mess(ra,la,dt=0.5):           # Lektion 12: Messung an der Summenkurve (Abl. II)
    ts=[i*dt for i in range(int(260/dt))]
    v=[hump(t,ra[0],ra[1],ra[2])+hump(t,la[0],la[1],la[2]) for t in ts]
    amp=max(v); on=[t for t,x in zip(ts,v) if x>0.004]
    return amp, on[-1]-on[0], v, ts
def p_befund(amp,dauer):
    hoch=amp>0.25; breit=dauer>100
    return {(False,False):'normale P-Welle',(True,False):'P-dextroatriale',(False,True):'P-sinistroatriale',(True,True):'P-biatriale'}[(hoch,breit)]
