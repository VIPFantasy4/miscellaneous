# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 11:16:37 2019

@author: s4403711
"""

from gurobipy import *

# sets
Stores = ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9']
Distribution_Centres = ['DC0', 'DC1', 'DC2']
New_Distribution_Centres = ['DC3', 'DC4', 'DC5', 'DC6']

I = range(len(Stores))
J = range(len(Distribution_Centres))
N = range(len(New_Distribution_Centres))

# data
demand = [12, 14, 6, 20, 14, 15, 7, 16, 8, 7]
Scenario = [[12, 38, 6, 20, 14, 15, 7, 16, 8, 12],
            [12, 14, 6, 20, 14, 34, 7, 16, 8, 7],
            [12, 32, 6, 20, 14, 15, 7, 16, 8, 7],
            [12, 14, 6, 20, 14, 26, 7, 16, 8, 22],
            [12, 17, 6, 20, 14, 15, 7, 37, 8, 7]]
S = range(len(Scenario))
cost = [[3149, 3761, 1498, 3592, 3950, 2385, 2522, 2976, 3691, 616, ],
        [2895, 2548, 1685, 3055, 2782, 993, 755, 2323, 2412, 2454, ],
        [1406, 1653, 1767, 1566, 1780, 1493, 1664, 878, 1497, 2608, ]]
new_cost = [[2420, 2364, 1202, 2633, 2562, 656, 741, 1860, 2202, 2085],
            [3157, 3563, 1149, 3616, 3670, 1958, 1934, 2872, 3410, 1006],
            [1552, 830, 3111, 1118, 610, 2526, 2646, 1469, 991, 3881],
            [1953, 2207, 1194, 2196, 2301, 1247, 1466, 1479, 1997, 2068]]

capacity = [50, 50, 73]
new_capacity = [49, 27, 77, 74]

# model
m = Model("transporting")
# variables
X = {(j, i): m.addVar(vtype=GRB.BINARY) for j in J for i in I}
Y = {(n, i): m.addVar(vtype=GRB.BINARY) for n in N for i in I}
Z = {n: m.addVar(vtype=GRB.BINARY) for n in N}
# Objective
m.setObjective(
    quicksum(X[j, i] * cost[j][i] * demand[i] for j in J for i in I) + quicksum(
        new_cost[n][i] * Y[n, i] * demand[i] * Z[n] for n in N for i in I), GRB.MINIMIZE)

# constraints
m.addConstr(quicksum(Z[n] for n in N) == 1)

# constraint1
for i in I:
    m.addConstr(quicksum(X[j, i] for j in J) + quicksum(Y[n, i] * Z[n] for n in N) == 1)

# constraint2&3
for j in J:
    m.addConstr(quicksum(X[j, i] * demand[i] for i in I) <= capacity[j])
for n in N:
    m.addConstr(quicksum(Y[n, i] * demand[i] * Z[n] for i in I) <= new_capacity[n])

# constraint4
for s in S:
    for j in J:
        m.addConstr(quicksum(X[j, i] * Scenario[s][i] for i in I) <= capacity[j])
    for n in N:
        m.addConstr(quicksum(Y[n, i] * Scenario[s][i] * Z[n] for i in I) <= new_capacity[n])

m.optimize()
print(m.objVal)
