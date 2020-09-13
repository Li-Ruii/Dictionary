"""
    把dict.txt中的数据传入数据库
"""

import pymysql
import re

f = open('dict.txt', 'r')
db = pymysql.connect('localhost', 'root', '1030', 'dictionary')

cur = db.cursor()
sql = 'insert into words (word, mean) values (%s, %s)'
# 遍历每一行
for line in f:
    # 正则表达式获取单词内容
    tup = re.findall(r'(\w+)\s+(.*)', line)[0]

    try:
        cur.execute(sql, tup)
        db.commit()
    except Exception as e:
        print('Failed:', e)
        db.rollback()
f.close()
cur.close()
db.close()



