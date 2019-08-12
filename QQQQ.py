# -*- coding: utf-8 -*-
"""
Created on Thu May 16 18:54:17 2019

@author: s4403711
"""

Profit = [152, 166, 169]

Demand = [[0.00, 0.15, 0.20, 0.36, 0.21, 0.08],
          [0.13, 0.21, 0.31, 0.20, 0.15, 0.00],
          [0.00, 0.13, 0.19, 0.35, 0.22, 0.11]]


def Pr(x, y, z):
    return Demand[0][x] * Demand[1][y] * Demand[2][z]


D = range(len(Demand[0]))
_Optimal = {}


def OptimalProfit(t, s1, s2, s3):
    if t == 4:
        return (0, 0, 0, 0)
    if (t, s1, s2, s3) not in _Optimal:
        return max((sum(Pr(d1, d2, d3) * (
            Profit[0] * min(s1 + a1, d1) + Profit[1] * min(s2 + a2, d2) + Profit[2] * min(s3 + a3, d3) +
            OptimalProfit(t + 1, max(0, s1 + a1 - d1), max(0, s2 + a2 - d2), max(0, s3 + a3 - d3))[0]) for d1 in D for
                        d2 in
                        D for d3 in D) - 30 * (s1 + a1 + s2 + a2 + s3 + a3), a1, a2, a3) for a1 in range(0, 6 - s1) for
                   a2 in range(0, 6 - s2) for a3 in range(0, 6 - s3))


print(OptimalProfit(0, 0, 0, 0))

# def profit_storage_Alaska (t,s):
#    if t == 4:
#        return (0,0)
#    return max((sum(Demand[0][d] * (Profit[0]* min(s + a, d) + profit_storage_Alaska(t+1, max(0, s+a-d))[0] ) 
#                 for d in D) - 30* (s+a), a) for a in range(0,6-s))
#    
# def profit_storage_Elsa (t,s):
#    if t == 4:
#        return (0,0)
#    return max((sum(Demand[1][d] * (Profit[1]* min(s + a, d) + profit_storage_Elsa(t+1, max(0, s+a-d))[0] ) 
#                 for d in D) - 30* (s+a), a) for a in range(0,6-s))
#
# def profit_storage_Lumi (t,s):
#    if t == 4:
#        return (0,0)
#    return max((sum(Demand[2][d] * (Profit[2]* min(s + a, d) + profit_storage_Lumi(t+1, max(0, s+a-d))[0] ) 
#                 for d in D) - 30* (s+a), a) for a in range(0,6-s))
#    
# print(profit_storage_Alaska (0,0)[0]+profit_storage_Elsa (0,0)[0]+profit_storage_Lumi (0,0)[0])
