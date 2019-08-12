# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 14:04:48 2019

@author: s4403711
"""

from gurobipy import *

# Sets
Quarter = ["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8"]
Friut= ["Orange","Apple","Mango","Pineapple","Passionfruit","Guava","Strawberry"]
Juice=["Orange Juice","Orange and Mango Juice","Breakfast Juice",
       "Tropical Juice","Guava Delight","Orchard Medley","Strawberry Surprise"]


Q = range(len(Quarter))
F = range(len(Friut))
J =range(len(Juice))

# Data
C = [901,620,1300,800,1500,710,1370] #cost
#Pr= [1500,1500,1500,1500,1500,1500,1500]#price for each juice
I = [[1,0,0,0,0,0,0],
      [0.90,0,0.10,0,0,0,0],
      [0.15,0.55,0.02,0.28,0,0,0],
      [0.04,0.65,0,0.30,0.01,0,0],
      [0,0.80,0,0.10,0,0.10,0],
      [0.45,0.50,0.05,0,0,0,0],
      [0,0.90,0,0,0,0.02,0.08]]  #Ingredient of each juice    
SMAX = [1400,1850,2950,2100,1750,2300,3150,2900]

 #SMAX = [[1400,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY],
  #      [1850,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY],
    #    [2950,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY],
      #  [1750,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY],
        #[2300,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY],
        #[3150,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY],
        #[2900,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY,GRB.INFINITY]]
        #The amount of fruit could be supplied each quarter
D=[[669,859,1340,955,787,933,1689,1404],
   [286,387,593,400,377,401,611,601],
   [466,746,1266,900,571,757,1121,1054],
   [455,531,802,671,499,620,946,946],
   [316,462,508,375,306,464,509,417],
   [1197,808,603,995,1111,760,632,800],
   [677,714,548,323,622,786,489,407]]


#D = [[669,286,466,455,316,1197,677],
#      [859,387,746,531,462,808,714],
 #     [1340,593,1266,802,508,603,548],
  #    [955,400,900,671,375,995,323],
   #   [787,377,571,499,306,1111,622],
    #  [933,401,757,620,464,760,786],
     # [1689,611,1121,946,509,632,489],
      #[1404,601,1054,946,417,800,407]]#Amount of demand each quarter
# Model
m = Model("Pure Fresh Juice")
# m.setParam("MIPGap", 0)
#        


# Amount of juice produce each quarter 
X = {(f,q): m.addVar() for f in F for q in Q}#fruit
Y = {(j,q): m.addVar() for j in J for q in Q} #juice 
Z = {(f,q): m.addVar(vtype=GRB.INTEGER) for f in F for q in Q}
S = {}
for j in J:
    for q in Q:
        S[j,q] = m.addVar(vtype=GRB.BINARY)
# Objective is to maximize the profit
m.setObjective(quicksum(1500*Y[j,q] for j in J for q in Q) -
            quicksum(C[f]*X[f,q] for f in F for q in Q), GRB.MAXIMIZE)
     
# Constraints
left = {}
for q in Q:
    m.addConstr(X[0,q] <=  SMAX[q]) #orange limit
    
        
    
    
for f in F:
    for q in Q:
        left[f,q] = m.addConstr(quicksum(I[j][f]*Y[j,q] for j in J)<=X[f,q])  #fruit limit
        if f != 0:
            m.addConstr(X[f,q]==10*Z[f,q])  #truck limit


for j in J:
    for q in Q:
        m.addConstr(Y[j,q] <=D[j][q]) #market limit

for q in Q:
#gourmet limit
    m.addConstr(quicksum(S[j,q] for j in J if j > 3)<=2)
for q in Q:
    for j in J:
        if q>0 and j>3:
            m.addConstr(S[j,q]+S[j,q-1] >=1)

#for q in Q:
#gourmet limit
#    md.addConstr(quicksum(S[j,q] for j in J if j > 3)<=2)
    
#for q in Q:
  #  for j in J:
    #    if q>0 and j>3:
      #      md.addConstr(S[j,q]+S[j,q-1] >=1)
m.optimize()

print('---------------------------')
for j in J:
        print([Y[j,q].x for q in Q])
        


