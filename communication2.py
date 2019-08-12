# -*- coding: utf-8 -*-
"""
Created on Tue May 14 18:40:09 2019

@author: Admin
"""

Profit = [152, 166, 169]
Sales =[[0.0, 1.4, 2.4, 3.1,3.2],
         [0.0, 0.8, 2.7, 3.1, 3.6],
         [0.0,0.4, 2.9, 3.8, 4.1]]

Demand =[[0.00, 0.15, 0.20, 0.36, 0.21, 0.08],
                   [0.13, 0.21, 0.31, 0.20, 0.15, 0.00],
                   [0.00, 0.13, 0.19, 0.35, 0.22, 0.11]]

def profit(t,s):
    # t is type, s is sale
    if t==3:
        return (0,0)
    ran = min(4,s)
    return max((Profit[t]*Sales[t][a] + profit(t+1,s-a)[0], a) for a in range(0,ran+1))
    

D = range(6)
Demand_probability_Alaska = [0.00, 0.15, 0.20, 0.36, 0.21, 0.08]
Demand_probability_Elsa =[0.13, 0.21, 0.31, 0.20, 0.15, 0.00]
Demand_probability_Lumi =   [0.00, 0.13, 0.19, 0.35, 0.22, 0.11]

def profit_storage_Alaska (t,s):
    # t is week, s is storage, a number of order
    #s = int(s)
    if t == 4:
        return (0,0)
    # (130* min(s + a, d) + profit_storage(t+1, max(0, s=a-d)) )
    return max((sum(Demand_probability_Alaska[d] * (152* min(s + a, d) + profit_storage_Alaska(t+1, max(0, s+a-d))[0] ) 
                 for d in D) - 30* (s+a), a) for a in range(0,6-s))
    
def profit_storage_Elsa (t,s):
    # t is week, s is storage, a number of order
    #s = int(s)
    if t == 4:
        return (0,0)
    # (130* min(s + a, d) + profit_storage(t+1, max(0, s=a-d)) )
    return max((sum(Demand_probability_Elsa[d] * (166* min(s + a, d) + profit_storage_Elsa(t+1, max(0, s+a-d))[0] ) 
                 for d in D) - 30* (s+a), a) for a in range(0,6-s))

def profit_storage_Lumi (t,s):
    # t is week, s is storage, a number of order
    #s = int(s)
    if t == 4:
        return (0,0)
    # (130* min(s + a, d) + profit_storage(t+1, max(0, s=a-d)) )
    return max((sum(Demand_probability_Lumi[d] * (169* min(s + a, d) + profit_storage_Lumi(t+1, max(0, s+a-d))[0] ) 
                 for d in D) - 30* (s+a), a) for a in range(0,6-s))
    
#def profit_storage_c2(t,s):
#    if t == 4:
#        return (0,0)
#    # (130* min(s + a, d) + profit_storage(t+1, max(0, s=a-d)) )
#    return max((sum(Demand[type][d] * ((Profit[type] )* min(s + a, d) + profit_storage_c2(t+1, max(0, s+a-d))[0] ) 
#                 for d in D for type in range(3) ) - 30* (s+a), a) for a in range(0,7-s))