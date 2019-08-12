from gurobipy import *

# Sets
cakes = ["Chocolate", "Plain"]
ingredients = ["Time", "Eggs", "Milk"]

C = range(len(cakes))
I = range(len(ingredients))

# Data
prices = [4, 2]
available = [480, 30, 5]
usage = [
    [20, 50],
    [4, 1],
    [0.25, 0.2]
]

m = Model("Farmer Joes")

X = {}
for c in C:
    X[c] = m.addVar(vtype=GRB.INTEGER)

m.setObjective(quicksum(prices[c] * X[c] for c in C), GRB.MAXIMIZE)

for i in I:
    m.addConstr(quicksum(usage[i][c] * X[c] for c in C) <= available[i])

m.optimize()

for c in C:
    print("Bake", X[c].x, cakes[c], "cakes")

print("Revenue is ", m.objVal)
