from gurobipy import *

# sets
Quarters = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8']
Q = range(len(Quarters))

# data
D = [3490, 2990, 3330, 4170, 3300, 4370, 4000, 3410] #total demands in each quarter
C = [65, 99, 96, 66, 70, 61, 66, 89] #cost in each quarter
ShipCap = 5000 #ship capacity
InitRem = 5400 #Initial remaining amount in total
StorePrice = 1.5

# Model
m = Model()

# Var
I = {i: m.addVar() for i in Q} #importing amount for each quarter

#Remaining amount for each quarter
R1 = InitRem + I[0] - D[0] #remaining amount after 1st quater
R2 = R1 + I[1] - D[1]
R3 = R2 + I[2] - D[2]
R4 = R3 + I[3] - D[3]
R5 = R4 + I[4] - D[4]
R6 = R5 + I[5] - D[5]
R7 = R6 + I[6] - D[6]
R8 = R7 + I[7] - D[7]
R = [R1,R2,R3,R4,R5,R6,R7,R8]
print(I[0] + 0)

#print (R1)
# Objective
TotalCost = quicksum(C[i]*I[i] + R[i] * StorePrice for i in Q)
m.setObjective(TotalCost, GRB.MINIMIZE)

# Constraints
for i in Q:
    m.addConstr(I[i] <= ShipCap)
    m.addConstr(R[i] >= D[i])



