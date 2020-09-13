"""
    电子词典数据库处理代码
    env: python 3.6
"""

import pymysql
import login
import hashlib


# 创建类对用户注册和登录过程进行封装
# 定义方法实现用户注册，并把用户信息存入数据库
class Database:
    def __init__(self, host='localhost',
                 port=3306,
                 user='root',
                 password='1030',
                 database='dictionary',
                 charset='utf8', table='user'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.table = table
        self.connect_db()
        self.create_cur()

    # 创建链接数据库方法
    def connect_db(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  password=self.password,
                                  database=self.database,
                                  charset=self.charset)

    def create_cur(self):
        self.cur = self.db.cursor()

    # 创建结束函数
    def close(self):
        self.cur.close()
        self.db.close()

    def do_find_same(self, user_name, passwd):
        # 加密处理
        hash = hashlib.md5((user_name + "the-salt").encode())
        hash.update(passwd.encode())
        # 查询是否有相同的用户
        sql = login.login(self.table, user_name, hash.hexdigest())
        self.cur.execute(sql)
        p = self.cur.fetchone()  # 如果查询到结果，用户存在
        return p

    # 创建处理注册方法
    def register(self, user_name, passwd):
        p = self.do_find_same(user_name, passwd)
        if p:
            return False
        # 加密处理
        hash = hashlib.md5((user_name + "the-salt").encode())
        hash.update(passwd.encode())
        try:
            sql = login.register(self.table, user_name, hash.hexdigest())
            self.cur.execute(sql)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print('Failed:', e)
            return False
        pass

    # 创建处理登录方法
    def login(self, user_name, passwd):
        info = self.do_find_same(user_name, passwd)
        if info:
            return True
        else:
            return False
        pass

    # 插入历史记录
    def insert_history(self, user_name, word):
        sql = login.insert_history(user_name, word)
        try:
            self.cur.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print('Failed:', e)
        pass

    # 查单词
    def query(self, word):
        sql = login.query(word)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]
        pass

    # 查询历史记录
    def history(self, user_name):
        sql = login.history(user_name)
        self.cur.execute(sql)
        r = self.cur.fetchall()
        return r





