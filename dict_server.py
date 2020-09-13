"""
    词典服务端代码
    接受来自客户端请求，并且反馈
"""
from socket import *
from multiprocessing import Process
import signal
import sys
from db_controller import *
from time import sleep

# 设定服务器地址
ADDR = '0.0.0.0'
PORT = 8888
HOST = (ADDR, PORT)


# 创建处理注册函数
def do_register(user_name, passwd, db, c):
    # 在数据库中操作
    if db.register(user_name, passwd):
        c.send(b'OK')
    else:
        c.send(b'failed')
    pass


# 创建处理登录函数
def do_login(user_name, passwd, db, c):
    if db.login(user_name, passwd):
        c.send(b'OK')
    else:
        c.send(b'error')
    pass


# 创建处理结束进程函数
def do_quit(c):
    c.close()
    sys.exit('客户端退出')
    pass


# 创建查询单词函数
def do_find_words(user_name, word, db, c):
    db.insert_history(user_name, word)  # 插入历史记录
    mean = db.query(word)
    if not mean:
        c.send('没有找到该单词'.encode())
    else:
        msg = "{}:{}".format(word, mean)
        c.send(msg.encode())
    pass


# 创建历史查询函数
def do_history(user_name, db, c):
    hist = db.history(user_name)
    if not hist:
        c.send(b'FAIL')
        return
    c.send(b'OK')
    for item in hist:
        record = '%s    %s    %s' % (item[1], item[2], item[3])
        sleep(0.1)
        c.send(record.encode())
    sleep(0.1)
    c.send(b'##')


# 分叉函数处理客户端不同请求
def do_request(c, db):
    db.create_cur()
    while True:
        data = c.recv(1024).decode()
        if not data:
            do_quit(c)
        tmp = data.split(' ')
        print(c.getpeername(), ':', tmp[1])
        user_name = tmp[1]
        passwd = tmp[2]
        if tmp[0] == 'E':
            do_quit(c)
        elif tmp[0] == 'R':
            do_register(user_name, passwd, db, c)
        elif tmp[0] == 'L':
            do_login(user_name, passwd, db, c)
        elif tmp[0] == 'Q':
            do_find_words(user_name, passwd, db, c)
        elif tmp[0] == 'H':
            do_history(user_name, db, c)

    pass


# 主函数用于处理客户端链接
def main():
    # 创建数据库链接对象
    db = Database()

    # 建立tcp套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(HOST)
    s.listen(5)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 等待客户端链接
    print('Listening to the port 8888')
    while True:
        try:
            c, addr = s.accept()
            print('Connect from:', addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue
        # 创建子进程
        p = Process(target=do_request, args=(c, db))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()

