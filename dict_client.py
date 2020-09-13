"""
    词典客户端代码
    发起请求，展示结果
"""
from socket import *
from getpass import getpass

# 设定服务器地址
ADDR = '127.0.0.1'
PORT = 8888
HOST = (ADDR, PORT)

# 建立套接字
s = socket()
s.connect(HOST)


# 通过客户端选择功能发送信息
def input_info():
    user_name = input('请输入用户名：')
    if user_name == 'exit':
        print('谢谢使用')
        return None, None
    passwd = getpass('请输入密码：')
    return user_name, passwd


# 二级界面
def second_login(user_name):
    while True:
        print('=======QUERY========')
        print('****1.find words****')
        print('*****2.history******')
        print('*****3.log out******')
        print('====================')
        cmd = input('请输入选项：')
        if cmd == '1':
            do_find_words(user_name)
        elif cmd == '2':
            do_history(user_name)
        elif cmd == '3':
            print('退出账户')
            return
        else:
            print('输入有误')


def do_find_words(user_name):
    while True:
        word = input('请输入单词（输入##结束查询）：')
        if word == '##':  # 结束单词查询
            break
        msg = 'Q ' + '%s %s' % (user_name, word)
        s.send(msg.encode())
        data = s.recv(2048).decode()
        print(data)
    pass


def do_history(user_name):
    msg = 'H ' + '%s 0' % user_name
    s.send(msg.encode())
    data = s.recv(128).decode()  # 接受来自服务端信号
    if data == 'OK':
        while True:
            record = s.recv(2048).decode()
            if record == '##':
                break
            print(record)
    elif data == 'FAIL':
        print('还没有历史记录')
    pass


# 注册账户
def do_register():
    print('注册账户')
    while True:
        user_name, passwd = input_info()
        if not user_name:
            return
        passwd1 = getpass('请再次输入密码')
        if (' ' in user_name) or (' ' in passwd):
            print('用户名或密码不能有空格')
            continue
        if passwd != passwd1:
            print('两次密码不一致')
            continue

        msg = 'R ' + '%s %s' % (user_name, passwd)
        s.send(msg.encode())
        data = s.recv(1024).decode()
        if data == 'OK':
            print('注册成功')
            second_login(user_name)
        else:
            print('注册失败')
        return
    pass


# 登录账户
def do_login():
    print('登录账户')
    user_name, passwd = input_info()
    if not user_name:
        return
    msg = 'L ' + '%s %s' % (user_name, passwd)
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if data == 'OK':
        print('登录成功')
        second_login(user_name)
    elif data == 'error':
        print('登录失败')
    return


# 退出程序
def do_quit():
    s.send(b'E 0 0')
    print('谢谢使用')
    pass


# 创建函数打印界面
def view():
    print('======WELCOME=======')
    print('*****1.register*****')
    print('******2.login*******')
    print('*******3.quit*******')
    print('====================')


# 主函数用于对输入的指令进行选择
def main():
    while True:
        view()
        cmd = input('请输入选项：')
        if cmd == '1':
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            do_quit()
            return
        else:
            print('输入有误')

    pass


if __name__ == '__main__':
    main()








