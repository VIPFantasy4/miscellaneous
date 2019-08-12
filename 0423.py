# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 11:16:37 2019

@author: s4403711
"""

from gurobipy import *

# In[Sets]:

Stores = ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9']
Distribution_Centres = ['DC0', 'DC1', 'DC2']
New_Distribution_Centres = ['DC3', 'DC4', 'DC5', 'DC6']

I = range(len(Stores))
J = range(len(Distribution_Centres))
N = range(len(New_Distribution_Centres))

# In[Data]:

demand = [12, 14, 6, 20, 14, 15, 7, 16, 8, 7]

cost = [[3149, 3761, 1498, 3592, 3950, 2385, 2522, 2976, 3691, 616],
        [2895, 2548, 1685, 3055, 2782, 993, 755, 2323, 2412, 2454],
        [1406, 1653, 1767, 1566, 1780, 1493, 1664, 878, 1497, 2608]]

new_cost = [[2420, 2364, 1202, 2633, 2562, 656, 741, 1860, 2202, 2085],
            [3157, 3563, 1149, 3616, 3670, 1958, 1934, 2872, 3410, 1006],
            [1552, 830, 3111, 1118, 610, 2526, 2646, 1469, 991, 3881],
            [1953, 2207, 1194, 2196, 2301, 1247, 1466, 1479, 1997, 2068]]

Scenario = [[12, 38, 6, 20, 14, 15, 7, 16, 8, 12],
            [12, 14, 6, 20, 14, 34, 7, 16, 8, 7],
            [12, 32, 6, 20, 14, 15, 7, 16, 8, 7],
            [12, 14, 6, 20, 14, 26, 7, 16, 8, 22],
            [12, 17, 6, 20, 14, 15, 7, 37, 8, 7]]

S = range(len(Scenario))
S2W = [6, 5, 2, 4, 4, ]
SW21 = [0 for i in range(6)] + [1 for i in range(5)] + [2 for i in range(2)] + [3 for i in range(4)] + [4 for i in
                                                                                                        range(4)]
capacity = [50, 50, 73]

new_capacity = [49, 27, 77, 74]

# In[Model]

m = Model("Wonder Market")

# In[Variables]:

X = {(j, i): m.addVar(vtype=GRB.BINARY) for j in J for i in I}
Y = {(n, i): m.addVar(vtype=GRB.BINARY) for n in N for i in I}
Z = {n: m.addVar(vtype=GRB.BINARY) for n in N}
A = {j: m.addVar(vtype=GRB.BINARY) for j in J}

FO = {j: m.addVar(vtype=GRB.INTEGER) for j in J}
FN = {n: m.addVar(vtype=GRB.INTEGER) for n in N}
PO = {j: m.addVar(vtype=GRB.INTEGER) for j in J}
PN = {n: m.addVar(vtype=GRB.INTEGER) for n in N}

CO = {(w, j): m.addVar(vtype=GRB.INTEGER) for j in J for w in range(21)}
CN = {(w, n): m.addVar(vtype=GRB.INTEGER) for n in N for w in range(21)}

# In[Objective]:

standard = quicksum(X[j, i] * cost[j][i] * demand[i] * A[j] for j in J for i in I) + quicksum(
    Y[n, i] * new_cost[n][i] * demand[i] * Z[n] for n in N for i in I) + quicksum(FO[j] * 4500 for j in J) + quicksum(
    FN[n] * 4500 for n in N) + quicksum(PO[j] * 2750 for j in J) + quicksum(PN[n] * 2750 for n in N)

surge = lambda w, s: quicksum(X[j, i] * cost[j][i] * Scenario[s][i] * A[j] for j in J for i in I) + quicksum(
    Y[n, i] * new_cost[n][i] * Scenario[s][i] * Z[n] for n in N for i in I) + quicksum(
    FO[j] * 4500 for j in J) + quicksum(FN[n] * 4500 for n in N) + quicksum(PO[j] * 2750 for j in J) + quicksum(
    PN[n] * 2750 for n in N) + quicksum(CO[w, j] * 2741 for j in J) + quicksum(CN[w, n] * 2741 for n in N)

m.setObjective(quicksum(surge(w, SW21[w]) for w in range(21)) + standard * 31, GRB.MINIMIZE)

# In[constraints0]:

m.addConstr(quicksum(Z[n] for n in N) == 2)
m.addConstr(quicksum(A[j] for j in J) == 2)

# In[constraint1]:

for i in I:
    m.addConstr(quicksum(X[j, i] * A[j] for j in J) + quicksum(Y[n, i] * Z[n] for n in N) == 1)

# In[constraint2&3]:

for j in J:
    m.addConstr(quicksum(X[j, i] * demand[i] for i in I) <= capacity[j])
    m.addConstr(quicksum(X[j, i] * demand[i] for i in I) <= FO[j] * 9 + PO[j] * 5)
for n in N:
    m.addConstr(quicksum(Y[n, i] * demand[i] for i in I) <= new_capacity[n])
    m.addConstr(quicksum(Y[n, i] * demand[i] for i in I) <= FN[n] * 9 + PN[n] * 5)

# In[ constraint4]:

# for s in S:
#     for i in range(0 if s == 0 else S2W[s - 1], sum(S2W[i] for i in range(s + 1))):
for i in range(21):
    s = SW21[i]
    for j in J:
        m.addConstr(quicksum(X[j, i] * Scenario[s][i] for i in I) <= capacity[j])
        m.addConstr(quicksum(X[j, i] * Scenario[s][i] for i in I) <= FO[j] * 9 + PO[j] * 5 + CO[i, j])
    for n in N:
        m.addConstr(quicksum(Y[n, i] * Scenario[s][i] for i in I) <= new_capacity[n])
        m.addConstr(quicksum(Y[n, i] * Scenario[s][i] for i in I) <= FN[n] * 9 + PN[n] * 5 + CN[i, n])

m.optimize()

print(m.objVal)

# In[ ]:
