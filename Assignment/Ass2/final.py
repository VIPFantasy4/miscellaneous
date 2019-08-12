from gurobipy import *

# Sets
Quarter = ["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8"]
Port= ["Brisbane","Sydney","Melbourne"]
Q = range(len(Quarter))
P = range(len(Port))
ShipHold = 5
BigShipHold = 8
H = range(ShipHold)
H2 = range(BigShipHold)

# Data
C = [65,99,96,66,70,61,66,89] 
C2 = [50,43,75,77,70,69,50,73] 

D  = [[1460, 1080, 950],
      [830, 990, 1170],
      [940, 960, 1430],
      [1240, 1120, 1810],
      [830, 1060, 1410],
      [1590, 1030, 1750],
      [1450, 960, 1590],
      [1110, 1410, 890]]

D2 = [[545, 510, 550],
      [500, 745, 760],
      [565, 485, 835],
      [550, 495, 715],
      [465, 410, 725],
      [580, 550, 615],
      [495, 565, 840],
      [535, 775, 545]]
      
InitAmount = [1500, 2100, 1800]  
InitAmount2 = [700, 600, 900]
StoreCap = [1500, 3400, 2300] 

ShipCost = 20000
BigShipCost = 28000
PortCost = 8000
StorePrice = 1.5

HoldCap = 1000
ShipCap = ShipHold * HoldCap
BigShipCap = BigShipHold * HoldCap


# Model
m = Model()

# Variables 
I = {(q, p): m.addVar() for p in P for q in Q}
S = {(q, p): m.addVar() for p in P for q in Q}
I2 = {(q, p): m.addVar() for p in P for q in Q}
S2 = {(q, p): m.addVar() for p in P for q in Q}

Z = {(q, p): m.addVar(vtype=GRB.BINARY) for p in P for q in Q} 
X = {q: m.addVar(vtype=GRB.BINARY) for q in Q}
Y = {q: m.addVar(vtype=GRB.BINARY) for q in Q}
X2 = {(q, h): m.addVar(vtype=GRB.BINARY) for h in H for q in Q}
Y2 = {(q, h): m.addVar(vtype=GRB.BINARY) for h in H2 for q in Q}
     
# Objective 
m.setObjective(quicksum(C[q] * I[q, p] + C2[q] * I2[q, p] 
                        + StorePrice * (S[q, p] + S2[q, p]) 
                        + Z[q, p] * PortCost for p in P for q in Q)
               + quicksum(X[q] * ShipCost +Y[q] * BigShipCost for q in Q), GRB.MINIMIZE)
     
# Constraints
for p in P:
    m.addConstr(S[7, p] == InitAmount[p]) #17
    m.addConstr(S2[7, p] == InitAmount2[p]) #18
    
for q in Q:
    for h in H:
        m.addConstr(X[q] - X2[q, h] >= 0) #12
    for h in H2:
        m.addConstr(Y[q] - Y2[q, h] >= 0) #13
    if q < 7:
        m.addConstr(Y[q] + Y[q+1] <= 1) #16
        
    m.addConstr(X[q] + Y[q] <= 1) #1
    
    m.addConstr(quicksum((I[q, p] + I2[q, p]) * Z[q, p] for p in P) 
    <= ShipCap * X[q] + BigShipCap * Y[q]) #2
    
    m.addConstr(1000*quicksum(X2[q, h] for h in H)  + 1000*quicksum(Y2[q, h] for h in H2) 
                >= quicksum(I[q, p] for p in P)) #14
    
    m.addConstr(1000*(5*X[q] + 8*Y[q] - quicksum(X2[q, h] for h in H) - quicksum(Y2[q, h] for h in H2)) 
                >= quicksum(I2[q, p] for p in P)) #15

for q in Q:
    for p in P:
        m.addConstr(I[q, p] + I2[q, p] 
                    <=  Z[q, p] * (ShipCap  * X[q] + BigShipCap * Y[q])) #11
        
        m.addConstr(S[q, p] <= StoreCap[p]) #19
        m.addConstr(S2[q, p] <= StoreCap[p]) #20
        
        m.addConstr(I[q, p] >= 0) #7
        m.addConstr(I2[q, p] >= 0) #8
        m.addConstr(S[q, p] >= 0) #9
        m.addConstr(S2[q, p] >= 0) #10
        if q >= 1:
            m.addConstr(S[q, p] == I[q, p] + S[q-1, p] - D[q][p]) #3 
            m.addConstr(S2[q, p] == I2[q, p] + S2[q-1, p] - D2[q][p]) #4
        else:
            m.addConstr(S[0, p] == InitAmount[p] + I[0, p] - D[0][p])  #5
            m.addConstr(S2[0, p] == InitAmount2[p] + I2[0, p] - D2[0][p])  #6
   


m.optimize()

print("\nOptimal value is ", round(m.objVal))

print("\nImported amount for diammonium phosphate")
for q in Q:
    print([round(I[q, p].x) for p in P]) 

print("\nImported amount for urea ")
for q in Q:
    print([round(I2[q, p].x) for p in P]) 

print("\nStored amount for diammonium phosphate")
for q in Q:
    print([round(S[q, p].x) for p in P])

print("\nStored amount for urea")
for q in Q:
    print([round(S2[q, p].x) for p in P])
    
print("\nX values")
for q in Q:
    print(round(X[q].x))
    
print("\nY values")
for q in Q:
    print(round(Y[q].x))
    
print("\nZ values")
for q in Q:
    print([round(Z[q, p].x) for p in P])

#com7
print("\nX2 value")
for q in Q:
    print([round(X2[q, h].x) for h in H])

print("\nY2 value")
for q in Q:
    print([round(Y2[q, h].x) for h in H2])
        
print("\n sum Imp1 value")
for q in Q:
    print(round(sum(I[q, p].x for p in P)))
    
print("\n sum Imp2 value")
for q in Q:
    print(round(sum(I2[q, p].x for p in P)))
