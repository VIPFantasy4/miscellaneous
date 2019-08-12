# from bs4 import BeautifulSoup as BS
# import pandas as pd
#
# with open('suyunjin.txt', 'r', encoding='gbk') as f:
#     soup = BS(f.read(), 'html.parser')
#
# data = []
# div = soup.find('div', class_='tableContent')
# tr_list = div.table.find_all('tr')
# header = tr_list[0].find_all('th')
# for i in range(1, len(tr_list)):
#     for ii, td in enumerate(tr_list[i].find_all('td')):
#         for v in td.find_all('span', class_='jdt-box'):
#             d = v.span.string.split('/')
#             d.extend([header[ii].string, tr_list[i].td.text.strip()])
#             data.append(d)
#
# df = pd.DataFrame(data, columns=[u'某数据1', u'某数据2', u'某数据3', u'服务器名称', u'活动名称'])
# print(df)
# df.to_excel(u'苏韵锦你这里欠我的用什么还.xlsx', index=False)

import random

def fuck(s, c, b, t):
    r = []
    p = {}
    for i in range(c):
        if i < c // 2:
            x = random.randint(b, t)
            r.append(x)
            p[i] = x - s // c
        else:
            if i + 1 == c:
                r.append(s - sum(r))
                return r
            d = p[i - c // 2]
            r.append(random.randint(b, (s // c) - d) if d > 0 else random.randint((s // c) - d, t))
    return r

r = fuck(1200, 4, 100, 400)
print(r, sum(r))