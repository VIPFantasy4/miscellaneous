# -*- coding: utf-8 -*-
"""
Created on Thu May 16 18:54:17 2019

@author: s4403711
"""


Profit = {1:152, 2:166, 3:169}

Pr ={1:[0.00, 0.15, 0.20, 0.36, 0.21, 0.08],
         2:[0.13, 0.21, 0.31, 0.20, 0.15, 0.00],
         3:[0.00, 0.13, 0.19, 0.35, 0.22, 0.11]}

def Demand(p1,p2,p3):
    return Pr[1][p1]*Pr[2][p2]*Pr[3][p3]
D=range(len(Pr[1]))
C2={}
def V(t,s1,s2,s3):
    if t==4:
        return (0,0,0,0)
    if (t,s1,s2,s3) not in C2:
        C2[t,s1,s2,s3]=max((sum(Demand(d1,d2,d3)*(Profit[1]*min(s1+a1,d1)+Profit[2]*min(s2+a2,d2)+Profit[3]*min(s3+a3,d3)
                       +V(t+1,max(0, s1+a1-d1),max(0, s2+a2-d2),max(0, s3+a3-d3))[0]) 
                        for d1 in D for d2 in D for d3 in D)-30*(s1+a1+s2+a2+s3+a3),a1,a2,a3) 
                        for a1 in range(0,5-s1+1) for a2 in range(0,5-s2+1) for a3 in range(0,5-s3+1))
    return C2[t,s1,s2,s3]
print("from the optimum strategy, our profit is:",V(0,0,0,0)[0])