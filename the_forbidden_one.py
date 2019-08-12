# import re
# import pandas as pd
#
# pattern = re.compile('^(\S+)\s*\[(\S+?)\s*\]\[(\S+?)\s*\](.*)$')
#
#
# def parse_access_log():
#     with open('base_test.log', encoding='utf-8') as f:
#         for line in f:
#             for m in pattern.finditer(line):
#                 yield m.groups()
#
#
# df = pd.DataFrame(parse_access_log(), columns=['time', 'tag', 'type', 'content'])
# df.astype(str)
# df.time = pd.to_datetime('2019-03-05 ' + df.time, format='%Y-%m-%d %X', exact=False)
# df.to_csv('access_log.csv', index=False)
############################################
# import pandas as pd
#
# df1 = pd.read_csv('access_log.csv', parse_dates=['time'])
# df2 = df1.set_index('time')
# df3 = df2['2019-03-05 10:00:00':'2019-03-05 12:00:00']
# print(df3.resample('10S').size())
############################################
# import sqlalchemy
# import pandas as pd
#
# engine = sqlalchemy.create_engine('sqlite:///sample.db')
# query = '''
# SELECT substr(time, 1, 10) time, count(*) count
# FROM access_log
# WHERE time BETWEEN '2019-03-05 10:00:00' AND '2019-03-05 12:00:00'
# GROUP BY 1 ORDER BY 1
# '''
#
# print(pd.read_sql(query, engine))
############################################
# import pandas as pd
#
# df1 = pd.read_excel(u'贩卖.xlsx', u'贩卖历史')
# df2 = pd.read_excel(u'贩卖.xlsx', u'商品')
# df3 = pd.merge(df1, df2, on=u'商品ID')
#
# print(df3)
# print(df3.pivot_table(u'金额', [u'店铺ID', u'商品名'], u'发售日', aggfunc='sum'))
# print(pd.read_clipboard())
#
#
# def category(row):
#     return {101: u'食品'}.get(row[u'商品ID'], u'其他')
#
#
# df1[u'商品类别'] = df1.apply(category, axis=1)
# print(df1)
# '''
# postgres=# SELECT date_trunc('month', "发售日")::DATE AS "发售日",
#                 "店铺ID",
#                 "商品ID",
#                 "顾客ID",
#                 sum("金额") AS "金额"
#             FROM "贩卖历史"
#             GROUP BY 1, 2, 3, 4;
# '''
############################################
# import sqlalchemy
# import pandas as pd
#
# '''
# vertical_table(vtable)
#    uid key  value
# 0  101  c1     11
# 1  101  c2     12
# 2  101  c3     13
# 3  102  c1     11
# 4  102  c2     12
# 5  102  c3     13
# '''
# '''
# horizontal_table(htable)
#    uid  c1  c2  c3
# 0  101  11  12  13
# 1  102  21  22  23
# '''
# '''
# postgres=# SELECT uid,
#                 sum(CASE WHEN key = 'c1' THEN value END) AS c1,
#                 sum(CASE WHEN key = 'c2' THEN value END) AS c2,
#                 sum(CASE WHEN key = 'c3' THEN value END) AS c3
#             FROM vtable;
# '''
# '''
# postgres=# SELECT uid, 'c1' AS key, c1 AS value FROM htable
#             UNION ALL
#             SELECT uid, 'c2' AS key, c2 AS value FROM htable
#             UNION ALL
#             SELECT uid, 'c3' AS key, c3 AS value FROM htable;
# '''
# '''
# postgres=# SELECT t1.uid, t2.key, t2.value FROM htable t1
#             CROSS JOIN unnest(
#                 array['c1', 'c2', 'c3'],
#                 array[c1, c2, c3]
#             ) t2 (key, value);
# '''
# engine = sqlalchemy.create_engine('sqlite:///sample.db')
# query = 'SELECT uid, key, sum(value) value FROM vtable GROUP BY 1, 2'
# vtable = pd.read_sql(query, engine)
# print(vtable.pivot('uid', 'key', 'value'))
# print(vtable.pivot_table('value', 'uid', 'key', aggfunc='sum'))
# htable = pd.DataFrame([[101, 11, 12, 13], [102, 21, 22, 23]], columns=['uid', 'c1', 'c2', 'c3'])
# print(htable.melt('uid', var_name='key', value_name='value'))
############################################
import pandas as pd
import sqlalchemy

pd.options.display.float_format = '{:,.0f}'.format  # 4444 -> 4,444
