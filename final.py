# -*- coding: utf-8 -*-
"""
Created on Thu May 16 18:54:17 2019

@author: s4403711
"""

Profit = [152, 166, 169]

Demand = [[0.00, 0.15, 0.20, 0.36, 0.21, 0.08],
          [0.13, 0.21, 0.31, 0.20, 0.15, 0.00],
          [0.00, 0.13, 0.19, 0.35, 0.22, 0.11]]

D = range(len(Demand[0]))


def profit_storage_Alaska(t, s):
    if t == 4:
        return 0, 0
    return max((sum(Demand[0][d] * (Profit[0] * min(s + a, d) + profit_storage_Alaska(t + 1, max(0, s + a - d))[0])
                    for d in D) - 30 * (s + a), a) for a in range(0, 6 - s))


def profit_storage_Elsa(t, s):
    if t == 4:
        return 0, 0
    return max((sum(Demand[1][d] * (Profit[1] * min(s + a, d) + profit_storage_Elsa(t + 1, max(0, s + a - d))[0])
                    for d in D) - 30 * (s + a), a) for a in range(0, 6 - s))


def profit_storage_Lumi(t, s):
    if t == 4:
        return 0, 0
    return max((sum(Demand[2][d] * (Profit[2] * min(s + a, d) + profit_storage_Lumi(t + 1, max(0, s + a - d))[0])
                    for d in D) - 30 * (s + a), a) for a in range(0, 6 - s))


# print(profit_storage_Alaska(0, 0)[0] + profit_storage_Elsa(0, 0)[0] + profit_storage_Lumi(0, 0)[0])
print(profit_storage_Alaska(3, 0)[0])


# def encapsulate(t, s):
#     if t == 4:
#         return 0
#     for a in range(0, 6 - s):
#         return max(encapsulate(t, s))
