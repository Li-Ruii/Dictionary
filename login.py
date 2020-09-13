"""
    login模块
    实现login方法以及register方法
"""
import time


# 注册功能sql语句
def register(table, user_name, passwd):
    sql = 'insert into %s (name, passwd) values ("%s", "%s");' % (table, user_name, passwd)
    return sql


# 查找功能sql语句
def login(table, user_name, passwd):
    sql = 'select * from %s where name="%s" and passwd="%s";' % (table, user_name, passwd)
    return sql


# 记录历史记录
def insert_history(user_name, word):
    tm = time.ctime()
    sql = 'insert into history (name, word, time) values ("%s", "%s", "%s");' % (user_name, word, tm)
    return sql


# 查单词
def query(word):
    sql = 'select mean from words where word="%s";' % word
    return sql


# 查历史记录
def history(user_name):
    sql = 'select * from history where name="%s" order by id desc limit 10;' % user_name
    return sql
