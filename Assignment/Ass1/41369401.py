from gurobipy import *

# Sets
Quarter = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"]
Port = ["Brisbane", "Sydney", "Melbourne"]
Q = range(len(Quarter))
P = range(len(Port))

# Data
C = [65, 99, 96, 66, 70, 61, 66, 89]  # cost
D = [[1460, 1080, 950],
     [830, 990, 1170],
     [940, 960, 1430],
     [1240, 1120, 1810],
     [830, 1060, 1410],
     [1590, 1030, 1750],
     [1450, 960, 1590],
     [1110, 1410, 890]]
InitAmount = [1500, 2100, 1800]  # Initial store amount
StorePrice = 1.5
ShipCap = 5000
StoreCap = [1500, 3400, 2300]  # additional store capacity

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
    m.addConstr(S[7, p] == InitAmount[p])

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
