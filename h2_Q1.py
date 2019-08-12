import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import optimize


def y3(x, a):
    x3 = [5 * current_x for current_x in x]
    y = a * np.sin(x3)
    return y


x = [0, 0.5236, 1.0472, 1.5708, 2.0944, 2.618, 3.1416]
t = [0, 1.5, -2.5981, 3, -2.5981, 1.5, 0]
t_mean = np.sum(t) / len(t)

results = {}
coeffs_a = np.polyfit(x, t, 3)
p = np.poly1d(coeffs_a)

y = p(x)

ssreg_a = np.sum((y - t_mean) ** 2)
sstot_a = np.sum((t - t_mean) ** 2)
results_a = ssreg_a / sstot_a
print(results_a)
'''

coeffs_b = np.polyfit(x,t,10)
p_b=np.poly1d(coeffs_b)
yhat_b = p_b(x)

ssreg_b = np.sum((yhat_b-t_mean)**2)
sstot_b = np.sum((t - t_mean)**2)
results_b = ssreg_b / sstot_b
print(results_b)
'''
A = optimize.curve_fit(y3, x, t)[0]

y_c = y3(x, A)

ssreg_c = np.sum((y_c - t_mean) ** 2)
sstot_c = np.sum((t - t_mean) ** 2)
results_c = ssreg_c / sstot_c
print(results_c)
