# -*- coding: utf-8 -*-
"""
Created on Thu May 16 18:54:17 2019

@author: s4403711
"""
import time
import itertools
start= time.time()
Profit = {1:152, 
          2:166, 
          3:169}

Pr ={1:[0.00, 0.15, 0.20, 0.36, 0.21, 0.08],
     2:[0.13, 0.21, 0.31, 0.20, 0.15, 0.00],
     3:[0.00, 0.13, 0.19, 0.35, 0.22, 0.11]}


D1=list(range(1, 6))
D2=list(range(0, 5))
D3=list(range(1, 6))
C3={}

def V(t,s1,s2,s3):
    if t==4:
        return (0,0,0,0)
    if s1>5: 
        return (0,0,0,0)
    if s2>4: 
        return (0,0,0,0)
    if s3>5: 
        return (0,0,0,0)        
    if (t,s1,s2,s3) not in C3:
        C3[t,s1,s2,s3]=max(
            (round(sum(Pr[1][d1] * Pr[2][d2] * Pr[3][d3]
                 *(Profit[1] * min(s1+a1, d1) + Profit[2] * min(s2+a2, d2) + Profit[3] * min(s3+a3, d3)
                     +V(t+1, max(0, s1+a1-d1), max(0, s2+a2-d2), max(0, s3+a3-d3))[0]) 
                 for d1,d2,d3 in itertools.product(range(1,6),range(0,5),range(1,6)))
        -30*(s1+a1+s2+a2+s3+a3) - 150*(((-0.1+a1+a2+a3)//7)+1),2), a1, a2, a3) 
        for a1 in range(min(len(Pr[1]), 8-s1+1)) 
        for a2 in range(min(len(Pr[2]), 14-a1+1, 8-s2+1)) 
        for a3 in range(min(len(Pr[3]), 14-a1-a2+1, 8-s3+1)))
    return C3[t, s1, s2, s3]

print("from the optimum strategy, our profit is:",V(0, 0, 0, 0)[0])
end= time.time()        




keys = list(C3.keys())
keys.sort()
print('{')
for key in keys:
    print(' ' * 4, end='')
    print(key, end='')
    print(': ', end='')
    v = list(C3[key])
    print(round(v[0], 2), '-> ', end='')
    del(v[0])
    print(v, end='')
    print(',')
print('}')
print(end-start)
#RAW = []
#for key in C3.keys():
#    RAW.append((key, C3[key]))
#sort_by_p = lambda x: x[1][0]
#sort_by_o = lambda x: x[0]
#RAW.sort(key=sort_by_o)
#RAW.sort(key=sort_by_p, reverse=True)
#print(RAW)




