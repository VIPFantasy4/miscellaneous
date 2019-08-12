from gurobipy import *

# Sets
Quarter = ["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8"]
Port= ["Brisbane","Sydney","Melbourne"]
Q = range(len(Quarter))
P = range(len(Port))

# Data
C = [65,99,96,66,70,61,66,89] #cost
C2 = [50,43,75,77,70,69,50,73] #com6

D  = [[1460, 1080, 950],
      [830, 990, 1170],
      [940, 960, 1430],
      [1240, 1120, 1810],
      [830, 1060, 1410],
      [1590, 1030, 1750],
      [1450, 960, 1590],
      [1110, 1410, 890]]
#com6  
D2 = [[545, 510, 550],
      [500, 745, 760],
      [565, 485, 835],
      [550, 495, 715],
      [465, 410, 725],
      [580, 550, 615],
      [495, 565, 840],
      [535, 775, 545]]
      
InitAmount = [1500, 2100, 1800] #Initial store amount 
InitAmount2 = [700, 600, 900] #com6 
StorePrice = 1.5
ShipCap = 5000
StoreCap = [1500, 3400, 2300] #additional store capacity
StoreCap2 = [1500, 3400, 2300] #com6
#ass 2 com4
ShipCost = 20000
PortCost = 8000

#com5
BigShipCap = 8000
BigShipCost = 28000

# Model
m = Model()

# Variables for import and store amount
I = {(q, p): m.addVar() for p in P for q in Q}
S = {(q, p): m.addVar() for p in P for q in Q}

#com6
I2 = {(q, p): m.addVar() for p in P for q in Q}
S2 = {(q, p): m.addVar() for p in P for q in Q}

#ass 2 com4
X = {q: m.addVar(vtype=GRB.BINARY) for q in Q}
Y = {(q, p): m.addVar(vtype=GRB.BINARY) for p in P for q in Q} 


#com5
Z = {q: m.addVar(vtype=GRB.BINARY) for q in Q}
     
# Objective is to minise the cost
m.setObjective(quicksum(C[q] * I[q, p] + C2[q] * I2[q, p] for p in P for q in Q)
                + quicksum(StorePrice * (S[q, p] + S2[q, p]) for p in P for q in Q) #com6
                + quicksum(X[q] * ShipCost for q in Q)
                + quicksum(Z[q] * BigShipCost for q in Q) #com 5
                #+ quicksum(Y[q, p] * PortCost for p in P for q in Q)
                + quicksum(Y[q, p] * PortCost for p in P for q in Q), GRB.MINIMIZE)
     
# Constraints
for q in Q:
    m.addConstr(X[q] + Z[q] <= 1)
# Constraint on  1,2,3 (refer to report)
for q in Q:
    for p in P:
        m.addConstr(I[q, p] + I2[q, p] <=  Y[q, p] * (ShipCap  * X[q] + BigShipCap * Z[q]))#com 4 & 5
        #m.addConstr(I2[q, p] <=  Y2[q, p] * (ShipCap  * X[q] + BigShipCap * Z[q]))#com 6
        if q >= 1:
            m.addConstr(S[q, p] == I[q, p] + S[q-1, p] - D[q][p])
            m.addConstr(S[q-1, p] + I[q, p] >= D[q][p])
            #com6
            m.addConstr(S2[q, p] == I2[q, p] + S2[q-1, p] - D2[q][p])
            m.addConstr(S2[q-1, p] + I2[q, p] >= D2[q][p])
        else:
            m.addConstr(S[0, p] == InitAmount[p] + I[0, p] - D[0][p]) #Constraint for stored amount after 1st quater
            m.addConstr(S2[0, p] == InitAmount2[p] + I2[0, p] - D2[0][p]) #com6
# Constraint on ship capacity (refer constraint 4 on report)
for q in Q:
    m.addConstr(quicksum((I[q, p] + I2[q, p]) * Y[q, p] for p in P) 
        <= ShipCap * X[q] + BigShipCap * Z[q]) # com4 & 5
#    m.addConstr(quicksum(I2[q, p] * Y2[q, p] for p in P) 
#        <= (ShipCap * X[q] + BigShipCap * Z[q] )) # com6
      
# Constraint on additional constraint 1 (refer to report)
for p in P:
    m.addConstr(S[7, p] == InitAmount[p])
    m.addConstr(S2[7, p] == InitAmount2[p]) # com6

# Constraint on store capacity (refer to addtional constriant 2 on report)
for q in Q:
    for p in P:
        m.addConstr(S[q, p] <= StoreCap[p])
        m.addConstr(S2[q, p] <= StoreCap2[p])
        

    

m.optimize()

print("\nThe objected value is ", m.objVal)


print("\nImported Amount")
for q in Q:
    print([round(I[q, p].x) for p in P]) 

print("\nImported Amount2")
for q in Q:
    print([round(I2[q, p].x) for p in P]) 

print("\nStored Amount")
for q in Q:
    print([round(S[q, p].x) for p in P])

print("\nStored Amount2")
for q in Q:
    print([round(S2[q, p].x) for p in P])
    
print("\nX values")
for q in Q:
    print(X[q].x)
    
#com5
print("\nZ values")
for q in Q:
    print(Z[q].x)
    
print("\nY values")
for q in Q:
    print([Y[q, p].x for p in P])

print("\n sum Imp1 value")
for q in Q:
    print(round(sum(I[q, p].x for p in P)))
    
print("\n sum Imp2 value")
for q in Q:
    print(round(sum(I2[q, p].x for p in P)))


    