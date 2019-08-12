def sum_to_n(t: list, n: int):
    res = []
    while len(t) > 0:
        if not isinstance(t[0], int):
            print('Invalid iter')
            return
        temp = t.pop(0)
        if temp > n: continue
        d = n - temp
        if d in t:
            res.append((temp, d) if temp < d else (d, temp))  # Redundant but pretty formatted
            t.remove(d)
    return res


# print(sum_to_n([1, 6, 1, 6, 7, 6], 7))
############################################

import matplotlib.pyplot as plt
import pandas as pd
import requests

import numpy as np
from pandas import DataFrame, Series

# FULL_IRIS = [
#     c.split(',')
#     for c in requests.get('http://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data').text.split()
# ]
# SEPAL_LENGTH_DATA = [float(d[0]) for d in FULL_IRIS]
# print(SEPAL_LENGTH_DATA)

# # 添加成绩表
# plt.style.use("ggplot")
# plt.rcParams['axes.unicode_minus'] = False
# plt.rcParams['font.sans-serif'] = ['SimHei']
# #
# # 新建一个空的DataFrame
# df = pd.DataFrame()
# # 添加成绩单，最后显示成绩单表格
# df["成绩分布"] = [40, 53, 53, 61, 63, 65, 67, 67, 69, 69, 69, 70, 70, 71, 74, 75, 75, 76, 77, 78, 79, 80, 81, 81, 81, 81,
#               82, 84, 85, 86, 87, 87, 87, 88, 89, 90, 91, 91, 94, 95, 100, 30]

# 用matplotlib来画出箱型图
# plt.boxplot(x=df.values,labels=df.columns,whis=1.5)
# plt.show()
#
#
# # 用pandas自带的画图工具更快
# df = pd.DataFrame()
# df['sepal_length'] = SEPAL_LENGTH_DATA
# df.boxplot()
# plt.show()
# print(len([sl for sl in SEPAL_LENGTH_DATA if sl > 6.40 or sl < 5.10]))


# df = DataFrame(np.random.randn(10, 2), columns=['Col1', 'Col2'])
# bp = df.boxplot(return_type='dict')
# print(bp['medians'][0].get_data())
# plt.show()

############################################

# import matplotlib.pyplot as plt
# import pandas as pd
# import requests
#
#
# FULL_IRIS = [
#     c.split(',')
#     for c in requests.get('http://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data').text.split()
# ]
# SEPAL_LENGTH_DATA = [float(d[0]) for d in FULL_IRIS]
# df = pd.DataFrame()
# df['sepal_length'] = SEPAL_LENGTH_DATA
# y_min, y_max = df.boxplot(return_type='dict')['boxes'][0].get_ydata()[1:3]
# print(y_min, y_max)
# print(len([sl for sl in SEPAL_LENGTH_DATA if sl < y_min or sl > y_max]))

############################################
# import pandas as pd
# from matplotlib import pyplot as plt
#
# hw1mystery = pd.read_csv('hw1mystery.csv')
# print(hw1mystery)
# bp = hw1mystery.boxplot(return_type='dict')
# plt.show()

from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots(1, 1)
x = np.linspace(norm.ppf(0.01), norm.ppf(0.99), 100)
ax.plot(x, norm.pdf(x), 'r-', lw=5, alpha=0.6, label='norm pdf')
plt.show()