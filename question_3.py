# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 00:39:50 2019

@author: 水濠
"""

from gurobipy import *

# Sets
Quarter = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"]
Port = ["Brisbane", "Melbourne", "Adelaide"]
Q = range(len(Quarter))
P = range(len(Port))

# Data
C = [890, 972, 978, 882, 865, 815, 826, 979]  # cost
D = [[1400, 1900, 2500],
     [1850, 2700, 2200],
     [2950, 2550, 850],
     [2100, 1450, 2300],
     [1750, 2900, 2850],
     [2300, 3400, 2150],
     [3150, 2500, 1200],
     [2900, 1450, 2300]]
InitAmount = [3200, 4000, 3800]  # Initial store amount
StorePrice = 35
ShipCap = 10000
LeastAmount = [3000, 3000, 3000]
StoreCap = [3700, 4300, 4500]  # additional store capacity
# Model
m = Model()

# Variables for import and store amount
I = {(q, p): m.addVar() for p in P for q in Q}
S = {(q, p): m.addVar() for p in P for q in Q}

# Objective is to minise the cost
m.setObjective(quicksum(C[q] * I[q, p] for p in P for q in Q)
               + quicksum(StorePrice * S[q, p] for p in P for q in Q), GRB.MINIMIZE)

# Constraints
# Constraint on  1,2,3 (refer to report)
for q in Q:
    for p in P:
        if q >= 1:
            m.addConstr(S[q, p] == I[q, p] + S[q - 1, p] - D[q][p])
            m.addConstr(S[q - 1, p] + I[q, p] >= D[q][p])
        else:
            m.addConstr(S[0, p] == InitAmount[p] + I[0, p] - D[0][p])  # Constraint for stored amount after 1st quater

# Constraint on ship capacity (refer constraint 4 on report)
for q in Q:
    m.addConstr(quicksum(I[q, p] for p in P) <= ShipCap)

# Constraint on additional constraint 1 (refer to report)

for p in P:
    m.addConstr(S[7, p] >= LeastAmount[p])
# Constraint on store capacity (refer to addtional constriant 2 on report)
for q in Q:
    for p in P:
        m.addConstr(S[q, p] <= StoreCap[p])

m.optimize()

print("\nThe objected value is ", m.objVal)

print("\nImported Amount")
for q in Q:
    print([I[q, p].x for p in P])

print("\nStored Amount")
for q in Q:
    print([S[q, p].x for p in P])
