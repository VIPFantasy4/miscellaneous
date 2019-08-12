from gurobipy import *

# Data
profit = [10, 6, 8, 4, 11, 9, 3]
P = range(len(profit)) # Products

n = [4, 2, 3, 1, 1]
M = range(len(n)) # Machines

# usage[P][M]
usage = [
    [0.5, 0.1, 0.2, 0.05, 0.00],
    [0.7, 0.2, 0.0, 0.03, 0.00],
    [0.0, 0.0, 0.8, 0.00, 0.01],
    [0.0, 0.3, 0.0, 0.07, 0.00],
    [0.3, 0.0, 0.0, 0.10, 0.05],
    [0.2, 0.6, 0.0, 0.00, 0.00],
    [0.5, 0.0, 0.6, 0.08, 0.05]
    ]

T = range(6) # Months

# maintenance[T][M]
maint = [
    [1, 0, 0, 0, 0],
    [0, 0, 2, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 1, 0, 1]
    ]

# market[P][T]
market = [
    [ 500, 600, 300, 200,   0, 500],
    [1000, 500, 600, 300, 100, 500],
    [ 300, 200,   0, 400, 500, 100],
    [ 300,   0,   0, 500, 100, 300],
    [ 800, 400, 500, 200,1000,1100],
    [ 200, 300, 400,   0, 300, 500],
    [ 100, 150, 100, 100,   0,  60]
    ]

MaxStore = 100
StoreCost = 0.5
FinalStore = 50
MonthHours = 16*24

fp = Model("Factory Planning")

# Variables
X = {(p,t): fp.addVar(vtype=GRB.INTEGER) for p in P for t in T}
Y = {(p,t): fp.addVar(vtype=GRB.INTEGER,ub=market[p][t]) for p in P for t in T}
S = {(p,t): fp.addVar(vtype=GRB.INTEGER,ub=MaxStore) for p in P for t in T}
# Z[t,m] is # of machines m to maintain in month t (for Question 2)
Z = {(t,m): fp.addVar(vtype=GRB.INTEGER) for t in T for m in M}

# Objective
fp.setObjective(quicksum(profit[p]*Y[p,t] for p in P for t in T) -
            quicksum(StoreCost*S[p,t] for p in P for t in T), GRB.MAXIMIZE)

# Usage constraint, including maintenance
for m in M:
    for t in T:
        fp.addConstr(quicksum(usage[p][m]*X[p,t] for p in P) <= 
                              MonthHours*(n[m] - Z[t,m]))
for p in P:
    S[p,-1] = 0
    fp.addConstr(S[p,5] >= FinalStore)
    for t in T:
    	# Market and storage constraints can be added as upper bounds to Y and S
        # fp.addConstr(S[p,t] <= MaxStore)
        # fp.addConstr(Y[p,t] <= market[p][t])
        fp.addConstr(S[p,t] == S[p,t-1] + X[p,t] - Y[p,t])

# Make sure variable maintenance still does original amounts
for m in M:
    fp.addConstr(quicksum(Z[t,m] for t in T) == sum(maint[t][m] for t in T))

# Extension: Try to smooth maintenance by limiting it to 2 machines per month
for t in T:
    fp.addConstr(quicksum(Z[t,m] for m in M) <= 2)
            
fp.optimize()

print("\nProfit = $",fp.objVal)
print("\nSales")
for p in P:
    print(p+1, [int(Y[p,t].x) for t in T])

print("\nProduction")
for p in P:
    print(p+1, [int(X[p,t].x) for t in T])

print("\nStorage")
for p in P:
    print(p+1, [int(S[p,t].x) for t in T])

print("\nMaintenance")
for m in M:
    print(m+1, [int(Z[t,m].x) for t in T])






