import csv
import statistics
import matplotlib.pyplot as plt


import numpy as np

validation_data = np.genfromtxt('hw2q2validation.csv',delimiter=",")
validation_x = validation_data[:,0]
validation_y = validation_data[:,1]

training_data = np.genfromtxt('hw2q2training.csv',delimiter=",")
training_x = training_data[:,0]
training_y = training_data[:,1]


sse_list_v = []
sse_list =[]
sse_total_list =[]
degree_list = []

for i in range(1,20):
    currrent_degree = i
    fit = np.polyfit(training_x,training_y,i)
    p = np.poly1d(fit)
    if i == 11:
        print(p)

    sse = 0.0
    sse_v = 0.0
    sse_tota =0.0

    for i in range(len(training_x)):
        y_h = p(training_x[i])
        y = training_y[i]
        sse += (y_h -y)**2
        
        y_h_v = p(validation_x[i])
        y_v = validation_y[i]
        sse_v +=(y_h_v -y_v)**2
        

    sse_tota = sse + sse_v
    sse_list.append(sse)
    sse_list_v.append(sse_v)
    sse_total_list.append(sse_tota)
    degree_list.append(currrent_degree)

plt.figure()
plt.plot(degree_list,sse_list,'-',label='Training',color = 'gray')
plt.plot(degree_list,sse_list_v,'--',label='Validation',color = 'gray')
#plt.plot(degree_list,sse_total_list,'-',label='Total_SSE',color = 'gray')

plt.legend()
plt.show()
print("polynomial degree order")
print(sse_list_v.index(min(sse_list_v))+1)

print("the validation set, recorded at order 5")
print(sse_list_v)
