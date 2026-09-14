from fractions import Fraction as F
from itertools import product
import math
# 1. pointwise fan inequality (9): for all A,B_k,C_k in {0,1}, sum_k A B_k C_k <= A + 1/2 sum_{k!=l} B_k C_l
for t in range(1,8):
    for A in (0,1):
        for bits in product((0,1),repeat=2*t):
            B=bits[:t]; C=bits[t:]
            lhs=sum(A*B[k]*C[k] for k in range(t))
            rhs=F(A)+F(1,2)*sum(B[k]*C[l] for k in range(t) for l in range(t) if k!=l)
            if lhs>rhs: raise SystemExit(f"pointwise fails t={t} A={A} B={B} C={C}")
print("pointwise fan inequality (9): exhaustively verified for t<=7")
# 2. P_eps sandwich
def fam(k):
    e=F(1,k**3); s=F(1,2*k*k)
    m=e+(1-e)*s; z=e+(1-e)*s**3
    return e,s,m,z
def v(t,m,z): return t*z-m-F(t*(t-1),2)*m*m
for k in (4,6,8,10,16,32,128,1024):
    e,s,m,z=fam(k)
    assert z*z>m**3
    tp=1+k//2                      # passes for t <= 1 + eps^{-1/3}/2 = 1 + k/2
    assert (tp-1)*e<=s              # Bernoulli passing certificate
    assert v(tp,m,z)<=0             # fan cannot reject at a passing order (consistency)
    t=tp
    while v(t,m,z)<=0: t+=1
    print(f"k={k:5d} eps=k^-3: passes t<={tp}, fan rejects at t={t}; eps^(1/3)*t={t/k:.4f}")
e,s,m,z=fam(4); print("v_4 at eps=1/64 =", v(4,m,z), "(claimed 6969/2097152)", v(4,m,z)==F(6969,2097152))
# 3. R_p: order 2 rejection by fan: 2z <= a + bc with a=b=c=z=p
p=F(1,3); print("R_p fan at t=2:", 2*p, "<=", p+p*p, "?", 2*p<=p+p*p)
# 4. Theorem 3 numeric check with mpmath
import mpmath as mp; mp.mp.dps=40
c0=mp.mpf(2)**(-1.5); d0=1-c0; h=d0/7
def Pe(eps):
    s=eps**(mp.mpf(2)/3)/2
    P={}
    for w in product('01',repeat=3):
        w=''.join(w); nz=w.count('0'); P[w]=(1-eps)*s**nz*(1-s)**(3-nz)+(eps if w=='000' else 0)
    return P
def Qe(eps):
    s=eps**(mp.mpf(2)/3)/2; u=s+(c0+h)*eps; pb=mp.sqrt(u); pf=h*eps
    # sources X,Y,Z each: base bit (prob pb), flag (prob pf); A=0 iff (Xb and Zb) or Xf or Zf ; B: X,Y ; C: Z,Y
    Q={''.join(w):mp.mpf(0) for w in product('01',repeat=3)}
    for xb,yb,zb,xf,yf,zf in product((0,1),repeat=6):
        pr=1
        for bit,pp in ((xb,pb),(yb,pb),(zb,pb),(xf,pf),(yf,pf),(zf,pf)): pr*= pp if bit else (1-pp)
        A=0 if ((xb and zb) or xf or zf) else 1
        B=0 if ((xb and yb) or xf or yf) else 1
        C=0 if ((zb and yb) or zf or yf) else 1
        Q[f"{A}{B}{C}"]+=pr
    return Q
for eps in [mp.mpf(10)**-k for k in (3,4,5,6)]:
    P=Pe(eps); Q=Qe(eps)
    tv=sum(abs(P[w]-Q[w]) for w in P)/2; l2=mp.sqrt(sum((P[w]-Q[w])**2 for w in P))
    print(f"eps=1e-{int(-mp.log10(eps))}: TV/eps={float(tv/eps):.6f} (d0={float(d0):.6f}), l2/eps={float(l2/eps):.6f} (sqrt(8/7)d0={float(mp.sqrt(mp.mpf(8)/7)*d0):.6f}), residual/eps^(4/3)={float((tv-d0*eps)/eps**(mp.mpf(4)/3)):.3f}")
