from gurobipy import *

# Sets
Oils = ["Veg1","Veg2","Oil1","Oil2","Oil3"]
Months = ["Jan","Feb","Mar","Apr","May","Jun"]
I = range(len(Oils))
T = range(len(Months))

# Data
IsVeg = [True,True,False,False,False]
Cost = [
        [110,130,110,120,100,90],
        [120,130,140,110,120,100],
        [130,110,130,120,150,140],
        [110,90,100,120,110,80],
        [115,115,95,125,105,135]
        ]
        
Hardness = [8.8,6.1,2.0,4.2,5.0]
Sell = 150
MaxH = 6
MinH = 3
MaxVeg = 200
MaxNonveg = 250
StoreMax = 1000
StoreCost = 5
Initial = 500

# Model
m = Model("Oil Blending 2")

# Variables
X = {}
Y = {}
S = {}
for i in I:
    for t in T:
        X[i,t] = m.addVar()
        Y[i,t] = m.addVar()
        S[i,t] = m.addVar()
    
# Objective
m.setObjective(quicksum(Sell*X[i,t] for i in I for t in T) - 
    quicksum(Cost[i][t]*Y[i,t] for i in I for t in T) -
    quicksum(StoreCost*S[i,t] for i in I for t in T),GRB.MAXIMIZE)

# Constraints
for t in T:
    m.addConstr(quicksum(X[i,t] for i in I if IsVeg[i]) <= MaxVeg)
    m.addConstr(quicksum(X[i,t] for i in I if not IsVeg[i]) <= MaxNonveg)
    m.addConstr(quicksum((Hardness[i]-MinH)*X[i,t] for i in I) >= 0)
    m.addConstr(quicksum((Hardness[i]-MaxH)*X[i,t] for i in I) <= 0)

    for i in I:
        m.addConstr(S[i,t] <= StoreMax)
        if t == 0:
            m.addConstr(S[i,t] == Initial - X[i,t] + Y[i,t])
        else:
            m.addConstr(S[i,t] == S[i,t-1] - X[i,t] + Y[i,t])

# Initial solution buys almost no oils...
# Add a constraint to have the same amount in stock at the end
for i in I:
    m.addConstr(S[i,5] >= Initial)
    
m.optimize()

print("Refining")
for i in I:
    print(Oils[i],[round(X[i,t].x,1) for t in T])
print("Buying")
for i in I:
    print(Oils[i],[round(Y[i,t].x,1) for t in T])
print("Store")
for i in I:
    print(Oils[i],[round(S[i,t].x,1) for t in T])
print("Blend Hardness")
for t in T:
    print(Months[t],round(sum(Hardness[i]*X[i,t].x for i in I)/sum(X[i,t].x for i in I),1))
      
print("Total profit is",m.objVal)


