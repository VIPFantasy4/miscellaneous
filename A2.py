from gurobipy import *

# sets
Fruit = ['Apple', 'Mango', 'Orange', 'Pineapple', 'Passionfruit', 'Guava', 'Strawberry']
Juice = ['OJ', 'OM', 'BJ', 'TJ', 'GD', 'OM', 'SS']

T = range(8)  # quarters
J = range(len(Juice))
F = range(len(Fruit))

# data
market = [[738, 1300, 1309, 1065, 599, 1032, 1309, 1134],
          [263, 493, 501, 492, 252, 419, 562, 528],
          [538, 997, 1187, 1042, 504, 765, 1201, 958],
          [353, 771, 900, 679, 398, 492, 883, 778],
          [271, 485, 588, 305, 285, 413, 531, 359],
          [1166, 642, 649, 787, 1020, 638, 660, 802],
          [536, 723, 524, 443, 679, 750, 498, 421]]

orange = [1400, 2400, 2850, 2450, 1250, 2000, 3100, 2600]

blend = [[0, 0, 1, 0, 0, 0, 0],
         [0, 0.1, 0.9, 0, 0, 0, 0],
         [0.55, 0.02, 0.15, 0.28, 0, 0, 0],
         [0.65, 0, 0.04, 0.3, 0.01, 0, 0],
         [0.8, 0, 0, 0.1, 0, 0.1, 0],
         [0.5, 0.05, 0.45, 0, 0, 0, 0],
         [0.9, 0, 0, 0, 0, 0.02, 0.08]]

cost = [620, 1300, 977, 800, 1500, 710, 1370]

m = Model("Pure Fresh Juice")
m.setParam("MIPGap", 0)

# variables
X = {(f, t): m.addVar() for f in F for t in T}  # fruit
Y = {(j, t): m.addVar() for j in J for t in T}  # juice
Z = {(f, t): m.addVar(vtype=GRB.INTEGER) for f in F for t in T}
S = {}
for j in J:
    for t in T:
        S[j, t] = m.addVar(vtype=GRB.BINARY)

# objective
m.setObjective(quicksum(1500 * Y[j, t] for j in J for t in T) -
               quicksum(cost[f] * X[f, t] for f in F for t in T), GRB.MAXIMIZE)

# constraints
left = {}
for t in T:
    m.addConstr(X[2, t] <= orange[t])  # orange limit

for f in F:
    for t in T:
        left[f, t] = m.addConstr(quicksum(blend[j][f] * Y[j, t] for j in J) <= X[f, t])  # fruit limit
        if f != 2:
            m.addConstr(X[f, t] == 10 * Z[f, t])  # ship limit

for j in J:
    for t in T:
        m.addConstr(Y[j, t] <= S[j, t] * market[j][t])  # market limit

for t in T:
    # gourmet limit
    m.addConstr(quicksum(S[j, t] for j in J if j > 3) <= 2)

for t in T:
    for j in J:
        if t > 0 and j > 3:
            m.addConstr(S[j, t] + S[j, t - 1] >= 1)

m.optimize()

for f in F:
    print([(X[f, t].x) for t in T])

print("left")
for f in F:
    print([left[f, t].slack for t in T])
