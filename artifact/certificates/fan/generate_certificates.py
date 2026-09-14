#!/usr/bin/env python3
"""Generate exact rational fan witnesses; these are bounds, not full-LP optima."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def atoms(k: int) -> dict[str,F]:
    eps=F(1,k**3); r=1-F(1,2*k*k)
    return {f'{v:03b}': (1-eps)*r**v.bit_count()*(1-r)**(3-v.bit_count())+(eps if v==0 else 0) for v in range(8)}

def record(k: int) -> dict:
    p=atoms(k); eps=F(1,k**3); sigma=F(1,2*k*k)
    m=sum(v for s,v in p.items() if s[0]=='0'); z=p['000']
    # Safe analytic passing bound, independently checked by the verifier.
    passing=1+k//2
    # The quadratic is increasing up to its vertex. On this interval find
    # the first positive integer using exact bisection, without sqrt or floats.
    def violation(t: int) -> F:
        return t*z-m-F(t*(t-1),2)*m*m
    vertex=(z/(m*m)+F(1,2)).numerator//(z/(m*m)+F(1,2)).denominator
    if violation(vertex)<=0:
        raise ArithmeticError('No certified positive fan value at integer vertex')
    lo,hi=1,vertex
    while hi-lo>1:
        mid=(lo+hi)//2
        if violation(mid)>0: hi=mid
        else: lo=mid
    gap=z*z-m**3
    ratio=(m*z-m**3)/gap
    return {'k':k,'epsilon':str(eps),'sigma':str(sigma),
            'atoms':{s:str(v) for s,v in p.items()},
            'm':str(m),'z':str(z),'finner_gap':str(gap),
            'passing_order':passing,'t_min_lower_bound':passing+1,
            'fan_rejecting_order':hi,'fan_violation':str(violation(hi)),
            'previous_fan_violation':str(violation(hi-1)),
            'second_moment_rejecting_order':ratio.numerator//ratio.denominator+1,
            'witness':{'form':'sum_k T_k - A - (1/2) sum_{k!=l} B_k C_l <= 0',
                       'coefficient_T':'1','coefficient_A':'-1',
                       'coefficient_cross_ordered':'-1/2',
                       'rectangular_root_copy_counts':[1,1,hi]}}

def main() -> None:
    ks=[4,5,6,8,10,16,32,64,128,256,512,1024,4096,65536]
    output={'schema':'triangle-fan-witness-v1',
            'repository_revision':'768d404c631659574d9fad232c028df4f63fbc3b',
            'arithmetic':'exact integers and fractions',
            'claim':'Passing and rejecting bounds only; not first rejection of the complete LP',
            'records':[record(k) for k in ks]}
    path=HERE/'certificates.json'
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(f'Wrote {path.name}: {len(ks)} rational targets')

if __name__=='__main__': main()
