#!/usr/bin/env python3
"""Independent exact verifier. No imports from generator; no optimizable asserts.

The pointwise inequality is checked by exhaustive assignments and, separately,
by counts of all four (B_k,C_k) types. The mathematical all-t proof is in REPORT.md.
"""
from __future__ import annotations
from fractions import Fraction
from pathlib import Path
from itertools import product
from copy import deepcopy
import json
import math

ROOT=Path(__file__).resolve().parent
F=Fraction

def require(test: bool, message: str) -> None:
    if not test: raise ValueError(message)

def verify_record(row: dict) -> None:
    k=row['k']; e=F(row['epsilon']); sig=F(row['sigma'])
    require(isinstance(k,int) and k>=4,'k')
    require(e==F(1,k**3) and sig==F(1,2*k*k),'family parameters')
    # A second atom formula: number of ZERO bits, not number of ONE bits.
    p={word: (1-e)*sig**word.count('0')*(1-sig)**word.count('1')
        +(e if word=='000' else 0) for word in map(''.join,product('01',repeat=3))}
    require(p=={w:F(v) for w,v in row['atoms'].items()},'target atoms')
    require(sum(p.values())==1 and min(p.values())>0,'positive normalized law')
    marg=[sum(v for w,v in p.items() if w[i]=='0') for i in range(3)]
    require(marg[0]==marg[1]==marg[2],'marginal symmetry')
    m=marg[0]; z=p['000']; gap=z*z-m**3
    require(F(row['m'])==m and F(row['z'])==z,'m,z')
    require(F(row['finner_gap'])==gap and gap>0,'Finner separation')
    tp=row['passing_order']; tr=row['fan_rejecting_order']
    require(tp==1+k//2 and row['t_min_lower_bound']==tp+1,'passing order')
    # Bernoulli's inequality plus an exact endpoint calculation certifies
    # r <= (1-epsilon)^(tp-1) without constructing huge denominators.
    require((tp-1)*e<=sig,'exact Bernoulli passing certificate')
    if k<=1024:
        require(1-sig <= (1-e)**(tp-1),'direct rational passing check')
    # Every displayed first fan rejection is independently checked by the
    # integer quadratic numerator. It is NOT asserted first complete-LP rejection.
    numerator_scale=2*z.denominator*m.denominator*m.denominator
    def v(t: int) -> F:
        return F(t)*z-m-F(math.comb(t,2))*m*m
    require(isinstance(tr,int) and tr>=2,'rejecting integer')
    require(v(tr)>0 and v(tr-1)<=0,'first fan crossing')
    require(v(tr)==F(row['fan_violation']),'fan margin')
    require(v(tr-1)==F(row['previous_fan_violation']),'preceding margin')
    require(tr*z>m+F(tr*(tr-1),2)*m*m,'target violates valid fan inequality')
    s=row['second_moment_rejecting_order']
    require(s*gap>m*z-m**3,'second moment rejection')
    require((s-1)*gap<=m*z-m**3,'second moment floor convention')
    w=row['witness']
    require(F(w['coefficient_T'])==1 and F(w['coefficient_A'])==-1 and
            F(w['coefficient_cross_ordered'])==F(-1,2),'witness coefficients')
    require(w['rectangular_root_copy_counts']==[1,1,tr],'root box')

def pointwise_exhaustive() -> int:
    count=0
    for t in range(1,9):
        for a in (0,1):
            for bits in product((0,1),repeat=2*t):
                b=bits[:t]; c=bits[t:]; s=sum(x*y for x,y in zip(b,c))
                cross=sum(b)*sum(c)-s
                # Double the slack to use only integer arithmetic.
                require(2*a+cross-2*a*s>=0,'exhaustive symmetric fan inequality')
                # The square certificate (lambda=3/2) is tested independently.
                require(9*a+4*cross-8*a*s>=0,'second moment square witness')
                count+=1
    return count

def compressed_counts() -> int:
    count=0
    for t in range(1,41):
        for n11 in range(t+1):
            for n10 in range(t-n11+1):
                for n01 in range(t-n11-n10+1):
                    n00=t-n11-n10-n01
                    b=n11+n10; c=n11+n01
                    for a in (0,1):
                        require(2*a+b*c-n11-2*a*n11>=0,'count-orbit inequality')
                        count+=1
    return count

def ancestry_audit() -> int:
    n=0
    for t in range(2,21):
        for k in range(t):
            for ell in range(t):
                if k==ell: continue
                ancestors_b={('X',0),('Y',k)}
                ancestors_c={('Z',0),('Y',ell)}
                require(ancestors_b.isdisjoint(ancestors_c),'cross-pair ancestral independence')
                # Complete partial permutations sending B to diagonal slot 0
                # and C to slot 1. X and Z permutations are independent.
                def extend(src_to_dst: dict[int,int]) -> dict[int,int]:
                    unused_src=[i for i in range(t) if i not in src_to_dst]
                    unused_dst=[i for i in range(t) if i not in src_to_dst.values()]
                    out={**src_to_dst,**dict(zip(unused_src,unused_dst))}
                    require(set(out)==set(range(t)) and set(out.values())==set(range(t)), 'permutation')
                    return out
                px=extend({0:0}); pz=extend({0:1}); py=extend({k:0,ell:1})
                require((px[0],py[k])==(0,0) and (pz[0],py[ell])==(1,1),'diagonal projections')
                n+=1
    return n

def negative_controls(records: list[dict]) -> list[str]:
    mutations=[]
    edits=[('changed epsilon',lambda r:r.__setitem__('epsilon',str(F(r['epsilon'])+F(1,100000)))),
           ('changed atom',lambda r:r['atoms'].__setitem__('000',str(F(r['atoms']['000'])+F(1,1000)))),
           ('wrong rejection order',lambda r:r.__setitem__('fan_rejecting_order',1)),
           ('sign reversal',lambda r:r['witness'].__setitem__('coefficient_cross_ordered','1/2')),
           ('zero violation margin',lambda r:r.__setitem__('fan_violation','0')),
           ('overstated passing order',lambda r:r.__setitem__('passing_order',r['k'])),
           ('wrong root box',lambda r:r['witness'].__setitem__('rectangular_root_copy_counts',[1,1,1]))]
    for name,edit in edits:
        row=deepcopy(records[5]); edit(row)
        try: verify_record(row)
        except ValueError: mutations.append(name)
        else: raise ValueError('Mutation survived: '+name)
    # The tempting wrong inclusion of diagonal k=ell into bc has a one-bit
    # obstruction. Its ancestors share Y and cannot use a product marginal.
    require(not {('X',0),('Y',0)}.isdisjoint({('Z',0),('Y',0)}),'collision negative control')
    mutations.append('diagonal pair cannot be assigned bc')
    return mutations

def symbolic_all_t_certificate() -> dict:
    """Check an all-t integer polynomial certificate for the fan inequality.

    Variables r,b,c are nonnegative integers, where b=n10 and c=n01.
    The five cases partition A in {0,1}, s=n11 in nonnegative integers.
    Every resulting slack polynomial has only nonnegative coefficients.
    """
    def const(x): return {(0,0,0):x} if x else {}
    def add(p,q):
        out=dict(p)
        for e,v in q.items(): out[e]=out.get(e,0)+v
        return {e:v for e,v in out.items() if v}
    def scale(p,k): return {e:k*v for e,v in p.items() if k*v}
    def mul(p,q):
        out={}
        for e,v in p.items():
            for f,w in q.items():
                g=tuple(x+y for x,y in zip(e,f)); out[g]=out.get(g,0)+v*w
        return {e:v for e,v in out.items() if v}
    r={(1,0,0):1}; b={(0,1,0):1}; c={(0,0,1):1}
    result={}
    for a,base,variable in [(0,0,False),(0,1,True),(1,0,False),(1,1,False),(1,2,True)]:
        s=add(const(base),r if variable else {})
        # Double slack: 2*A + (sum B)(sum C) - S - 2*A*S.
        slack=add(add(const(2*a),mul(add(s,b),add(s,c))),scale(s,-1-2*a))
        require(all(v>=0 for v in slack.values()),'symbolic nonnegative coefficient certificate')
        result[f'A={a}, S={base}'+('+r' if variable else '')]={','.join(map(str,e)):v for e,v in sorted(slack.items())}
    require(len(result)==5,'all nonnegative-integer S cases covered')
    return result

def main() -> None:
    data=json.loads((ROOT/'certificates.json').read_text())
    require(data['schema']=='triangle-fan-witness-v1','schema')
    for row in data['records']: verify_record(row)
    report={'status':'PASS','targets_verified':len(data['records']),
            'all_t_nonnegative_polynomial_cases':symbolic_all_t_certificate(),
            'pointwise_assignments':pointwise_exhaustive(),
            'count_orbits':compressed_counts(),'NW_cross_pair_embeddings':ancestry_audit(),
            'negative_controls_rejected':negative_controls(data['records']),
            'scope':'Exact passing/rejecting certificates; no full-LP first-rejection claim',
            'rows':[{key:row[key] for key in ['k','passing_order','t_min_lower_bound','fan_rejecting_order','second_moment_rejecting_order']} for row in data['records']]}
    (ROOT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
