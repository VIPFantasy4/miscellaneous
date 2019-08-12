import re
from xml.etree import ElementTree as ET

mtree = ET.parse('monster.xml')

m = [int(e.find('monster_name_i').text) for e in mtree.getroot().findall('data')]

ctree = ET.parse('chinese.xml')
c = {}
for e in ctree.getroot().findall('record'):
    try:
        c[int(e.find('id_i').text)] = e.find('content_s').text
    except:
        print(int(e.find('id_i').text))
# print(len(c))
#
# for mid in m:
#     if mid not in c:
#         print(mid)