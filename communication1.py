# -*- coding: utf-8 -*-
"""
Created on Tue May 14 18:40:09 2019

@author: Admin
"""

Profit = [152, 166, 169]
Sales = [[0.0, 1.4, 2.4, 3.1, 3.2],
         [0.0, 0.8, 2.7, 3.1, 3.6],
         [0.0, 0.4, 2.9, 3.8, 4.1]]


def profit(type, sale):
    if type == 3:
        return (0, 0)
    ran = min(4, sale)
    return max((Profit[type] * Sales[type][a] + profit(type + 1, sale - a)[0], a) for a in range(ran + 1))

r = []
for x1 in range(5):
    for x2 in range(5):
        x3 = min(8 - x1 - x2, 4)
        x2 = 8 - x1 - x3
        r.append((152 * Sales[0][x1] + 166 * Sales[1][x2] + 169 * Sales[2][x3], (x1, x2, x3)))
print(max(r))


# def MaxProfitSoln():
#     s=8
#     for t in [0,1,2]:
#         v=profit(t,s)
#         print(v[1], 'refrigerators displayed for type',t)
#         s=s-v[1]

print(profit(0, 8)[0])
# print(MaxProfitSoln())
# profit(0,8)
# profit(1,8-3)
# profit(2,8-3-2)
# profit(3,8-3-2-3)
