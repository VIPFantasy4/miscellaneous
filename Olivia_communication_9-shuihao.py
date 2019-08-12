#!/usr/bin/env python
# coding: utf-8

# In[3]:


from gurobipy import *

Store = ["S0","S1","S2","S3","S4","S5","S6","S7","S8","S9"]
Distn_Centre = ["DC0","DC1","DC2","DC3","DC4","DC5","DC6"]
Labour = ['full-time','part-time','casual']
# Add in 5 Surge Demands 
Scenario = ['Standard','Scenario 0','Scenario 1','Scenario 2','Scenario 3','Scenario 4']
# Number of weeks each of the scenarios appears
Weeks = [31, 6, 5, 2, 4, 4]

Scenario_Weeks_Search = {Scenario[i]:Weeks[i] for i in range(len(Scenario))}

S = range(len(Store))
D = range(len(Distn_Centre))
I = range(len(Scenario))
J = [3,4,5,6]
K = [0,1,2]
L = range(len(Labour))
#Data
# Cost coloumn represents [s] store, row represent [d] Distn_Centre

Costs = [
       [3149, 3761, 1498, 3592, 3950, 2385, 2522, 2976, 3691,  616],
            [2895, 2548, 1685, 3055, 2782,  993,  755, 2323, 2412, 2454],
            [1406, 1653, 1767, 1566, 1780, 1493, 1664,  878, 1497, 2608],
        [2420, 2364, 1202, 2633, 2562,  656,  741, 1860, 2202, 2085],
            [3157, 3563, 1149, 3616, 3670, 1958, 1934, 2872, 3410, 1006],
            [1552,  830, 3111, 1118,  610, 2526, 2646, 1469,  991, 3881],
            [1953, 2207, 1194, 2196, 2301, 1247, 1466, 1479, 1997, 2068]
        ]

# Labour Costs / The cost of full time, part time team and casual worker per week
Labour_Costs = {'full-time': 4500, 'part-time':2750, 'casual': 2741}


 # The number of truckload a full time, part time and casual worker
Labour_Load ={'full-time': 9, 'part-time':5, 'casual':1}


# Demand of each store
# Standard Demand of each store
Demand =  [12, 14, 6, 20, 14, 15, 7, 16, 8,  7]
# Surge demand process in surge weeks
surge_demand = [[12, 38, 6, 20, 14, 15, 7, 16, 8, 12],
            [12, 14, 6, 20, 14, 34, 7, 16, 8,  7],
            [12, 32, 6, 20, 14, 15, 7, 16, 8,  7],
            [12, 14, 6, 20, 14, 26, 7, 16, 8, 22],
            [12, 17, 6, 20, 14, 15, 7, 37, 8,  7]]

Weeks_demand = {'Standard': Demand, 'Scenario 0': surge_demand[0], 'Scenario 1' : surge_demand[1], 'Scenario 2' : surge_demand[2], 'Scenario 3' : surge_demand[3], 'Scenario 4': surge_demand[4]}


# Limited capacity of distribution centre
Capacity = [50, 50, 73, 49, 27, 77, 74]

#Model
m = Model("Wonder Market")

#Decision Variables
X = {} # Porportion of truckloads distributed to
Y = {} # Binary variable indicates which new DC will be built e.g. [0 0 1 0]
Z = {} # Binary variable indicates which old DC will be shut down e.g. [1 1 0]

for d in D:
    for s in S:
        X[d,s] = m.addVar(vtype = GRB.BINARY, lb = 0)

for j in J:
    Y[j] = m.addVar(vtype = GRB.BINARY, lb = 0)
for k in K:
    Z[k] = m.addVar(vtype = GRB.BINARY, lb = 0)

# Label assign (w,d,l)  w means week/scenario, d means different distribution, l means differen't label type
L = {}
for d in D:
    for l in Labour:
        for w in Scenario:
            L[w,d,l] = m.addVar(vtype = GRB.INTEGER, lb = 0)


#Objective Function = Transport Cost + Labour Cost
m.setObjective(quicksum(Costs[d][s]*X[d,s]*Weeks_demand[w][s]*Scenario_Weeks_Search[w] for s in S for d in D for w in Scenario)
               + quicksum(L[w,d,l] * Labour_Costs[l] * Scenario_Weeks_Search[w] for l in Labour for d in D for w in Scenario),GRB.MINIMIZE)



# Constraint 1: The sum of truckload for each store is 1.
# Each distribution center is assigned to at least one store
C_Fit_Stores = {}
for s in S:
    C_Fit_Stores[s] = m.addConstr(quicksum(X[d,s] for d in D) >= 1)

C_Capacity_of_Centre = {}
# Constraint 2/3: Capacity of distribution center d in D: 
for w in Scenario:
    for d in D:
        C_Capacity_of_Centre[w,d] = m.addConstr(quicksum(X[d,s] * Weeks_demand[w][s] for s in S) <= Capacity[d])

# Constraint 4: 
# At most two more new DC will be built 
C_two_new_DC = m.addConstr(quicksum(Y[j] for j in J) <= 2)

# Constraint 5: 
# The lower bound is that at least one store is assigned to one distribution
# center and the upper bound is 10 stores can all assign to one DC

C_closed_dc = {}
for j in J:
    C_closed_dc[j] = m.addConstr(quicksum(X[j,s] for s in S) <= 10*Y[j])
for k in K:
    C_closed_dc[k] = m.addConstr(quicksum(X[k,s] for s in S) <= 10*Z[k])


# Constraint 6: If two more distribution centre is built, one DC will be closed
# The total number of DC is smaller than 4.
C_total_DC = m.addConstr((quicksum(Y[j] for j in J) + quicksum(Z[k] for k in K))<=4)



# Constraint 7/8: the number of truckload processed by each Fulltime and Part-time
# team must satisfy the demand caused by surge weeks
C_labour_capacity = {}
for w in Scenario:
    for d in D:
        C_labour_capacity[w,d] = m.addConstr(quicksum(X[d,s] * Weeks_demand[w][s] for s in S) <= quicksum(L[w,d,l] * Labour_Load[l] for l in Labour))


# Constraint 9: the company employ a set number of Full-time and Part-time teams
# in a year. Causual workers are only employed in surge weeks.
for w in Scenario:
    for d in D:
        m.addConstr(L['Standard',d,'full-time'] == L[w,d,'full-time'])
        m.addConstr(L['Standard',d,'part-time'] == L[w,d,'part-time'])


# Optimize
m.optimize()

# Print out the objective value
print("-----------------------------------------------------\n\n\n\n")
# Print out the total cost
print("Objective is: $", m.objVal)


# Output the Labour cost
print('Labour Cost: ', end='')
print(sum([L[w,d,l].x * Labour_Costs[l] * Scenario_Weeks_Search[w] for l in Labour for d in D for w in Scenario]))

# Output the Transport cost
print('Transport Cost: ', end='')
print(sum([Costs[d][s]*X[d,s].x*Weeks_demand[w][s]*Scenario_Weeks_Search[w] for s in S for d in D for w in Scenario]))


# Print out how each store is assigned to each DC
print("The number of truckloads deliever from each distribution center to each store.")
print("  ", "\t".join(Store))
for d in D:
    print("DC"+str(d), "\t".join(str(int(X[d,s].x*Demand[s])) for s in S))
print('\n\n')




# output the management of Labour for the standard demand and the 5 surge demand
for w in Scenario:
    print("Number of Full-time, Part-time teams and Casual workers employ for  {}:".format(w))
    print("   ", "\t".join(Labour))
    for d in D:
        print("DC"+str(d), "\t\t".join(str(int(L[w,d,l].x)) for l in Labour))
    print('\n\n')



#sensitivity analysis

# print('Sensitivity Analysis on variables')
# for d in D:
#     for s in S:
#         print("'{},{}'".format(d,s),'\t', str( "{:.1%}".format(X[d,s].x)),'\t', round(X[d,s].RC,2),'\t',Costs[d][s],'\t', round(X[d,s].Obj,2),'\t',round(X[d,s].SAObjLow,2), '\t', round(X[d,s].SAObjUp,2))


# In[13]:


Frequency =[6, 5, 2, 4, 4]

Surge_Weeks = [p for p,i in enumerate(Frequency) for k in range(i)]


# In[14]:


print(Surge_Weeks)


# In[ ]:




