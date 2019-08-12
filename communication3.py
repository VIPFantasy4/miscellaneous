# -*- coding: utf-8 -*-
"""
Created on Thu May 16 18:54:17 2019

@author: s4403711
"""

import math
import datetime

Profit = {
    1: 152,
    2: 166,
    3: 169
}

Pr = {1: [0.00, 0.15, 0.20, 0.36, 0.21, 0.08],
      2: [0.13, 0.21, 0.31, 0.20, 0.15, 0.00],
      3: [0.00, 0.13, 0.19, 0.35, 0.22, 0.11]}

D = range(len(Pr[1]))
C3 = {}


def V(t, s1, s2, s3):
    if (t, s1, s2, s3) not in C3:
        C3[t, s1, s2, s3] = max(
            (round(sum(Pr[1][d1] * Pr[2][d2] * Pr[3][d3]
                 * (Profit[1] * min(s1 + a1, d1) + Profit[2] * min(s2 + a2, d2) + Profit[3] * min(s3 + a3, d3)
                    + (V(t + 1, max(0, s1 + a1 - d1), max(0, s2 + a2 - d2), max(0, s3 + a3 - d3))[0] if t < 3 else 0))
                 for d1 in D for d2 in D for d3 in D)
             - 30 * (s1 + a1 + s2 + a2 + s3 + a3) - 150 * math.ceil((a1 + a2 + a3) / 7), 2), a1, a2, a3)
            for a1 in range(min(len(Pr[1]), 8 - s1 + 1))
            for a2 in range(min(len(Pr[1]), 14 + 1 - a1, 8 - s2 + 1))
            for a3 in range(min(len(Pr[1]), 14 + 1 - a1 - a2, 8 - s3 + 1))
        )
    return C3[t, s1, s2, s3]


print(datetime.datetime.now())
print("from the optimum strategy, our profit is:", V(2, 0, 0, 0)[0])
# keys = list(C3.keys())
# keys.sort()
# print('{')
# for key in keys:
#     print(' ' * 4, end='')
#     print(key, end='')
#     print(': ', end='')
#     v = list(C3[key])
#     print(round(v[0], 2), '-> ', end='')
#     del(v[0])
#     print(v, end='')
#     print(',')
# print('}')

RAW = []
for key in C3.keys():
    RAW.append((key, C3[key]))

sort_by_p = lambda x: x[1][0]
sort_by_o = lambda x: x[0]

RAW.sort(key=sort_by_o)
print(RAW)

RAW.sort(key=sort_by_p, reverse=True)
print(RAW)
print(datetime.datetime.now())
