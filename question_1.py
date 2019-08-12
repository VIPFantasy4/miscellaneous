# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 22:57:11 2019

@author: 水濠
"""

from gurobipy import *

# Sets
Quarters = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"]
Ports = ["Brisbane", "Melbourne", "Adelaide"]
r_quarters = range(len(Quarters))
r_ports = range(len(Ports))

# Data
Cost = [890, 972, 978, 882, 865, 815, 826, 979]  # cost
Demands = [[1400, 1900, 2500],
           [1850, 2700, 2200],
           [2950, 2550, 850],
           [2100, 1450, 2300],
           [1750, 2900, 2850],
           [2300, 3400, 2150],
           [3150, 2500, 1200],
           [2900, 1450, 2300]]
Bases = [3200, 4000, 3800]  # Initial stored amount
StorePrice = 35
ShipCap = 10000

# Model
m = Model()

# Variables for import and store amount
I = {(q, p): m.addVar() for p in r_ports for q in r_quarters}
S = {(q, p): m.addVar() for p in r_ports for q in r_quarters}

# Objective is to minise the cost
m.setObjective(quicksum(Cost[q] * I[q, p] for p in r_ports for q in r_quarters)
               + quicksum(StorePrice * S[q, p] for p in r_ports for q in r_quarters), GRB.MINIMIZE)

# Constraints
# Constraint on  1,2,3 (refer to report)
for q in r_quarters:
    for p in r_ports:
        if q >= 1:
            m.addConstr(S[q, p] == I[q, p] + S[q - 1, p] - Demands[q][p])
            m.addConstr(S[q - 1, p] + I[q, p] >= Demands[q][p])  # Ensure the demand of next quarter
        else:
            m.addConstr(S[0, p] == Bases[p] + I[0, p] - Demands[0][p])  # Constraint for stored amount after 1st quater

# Constraint on ship capacity (refer constraint 4 on report)
for q in r_quarters:
    m.addConstr(quicksum(I[q, p] for p in r_ports) <= ShipCap)

# Constraint on additional constraint 1 (refer to report)

# Constraint on store capacity (refer to addtional constriant 2 on report)
m.optimize()

print("\nThe objected value is ", m.objVal)

print("\nImported Amount")
for q in r_quarters:
    print([I[q, p].x for p in r_ports])

print("\nStored Amount")
for q in r_quarters:
    print([S[q, p].x for p in r_ports])
