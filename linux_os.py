import os
import paramiko
import time
import re

remotr_path='/home/docker/ksync'
local_path='D:\桌面'
class Linux(object):
    def __init__(self,password,ip='211.149.156.147',username="root",port=22000,timeout=30):
        self.ip=ip
        self.username=username
        self.password=password
        self.timeout=timeout
        self.port=port
    # transport和chanel
        self.t = ''
        self.chan = ''
    # 链接失败的重试次数
        self.try_times = 3
    def connect(self):
        while True:
            try:
                # 设置ssh连接的远程主机地址和端口
                self.t=paramiko.Transport(sock=(self.ip,self.port))
                # 设置登录名和密码
                self.t.connect(username=self.username,password=self.password)
                # 连接成功后打开一个channel
                self.chan=self.t.open_session()
                # 设置会话超时时间
                self.chan.settimeout(self.timeout)
                # 打开远程的terminal
                self.chan.get_pty()
                # 激活terminal
                self.chan.invoke_shell()
                print(u'连接%s成功'%self.ip)
                print(self.chan.recv(65535).decode('utf-8'))
                return
            except Exception as e:
                print(e)
                if self.try_times !=0 :
                    print(u'连接%s失败，进行重试' % self.ip)
                    self.try_times -= 1
                else:
                    print(u'重试3次失败，结束程序')
                    exit(1)
    #断开连接
    def close(self):
        self.chan.close()
        self.t.close()

        # 发送要执行的命令
    def send(self, cmd, pattern):
        cmd += '\r'
        # 通过命令执行提示符来判断命令是否执行完成
        patt = pattern
        p = re.compile(patt)
        result = ''
        # 发送要执行的命令
        self.chan.send(cmd)
        # 回显很长的命令可能执行较久，通过循环分批次取回回显
        while True:
            time.sleep(1)
            ret = self.chan.recv(65535)
            ret = ret.decode('utf-8')
            result += ret
            if p.search(ret):
                print(result)
                return result
    def ftp(self,remote_path,local_path,file_name):
        sftp = paramiko.SFTPClient.from_transport(self.t)  # sftp传输协议
        src = remote_path + '/' + file_name
        des = local_path + '/' + file_name
        sftp.get(src, des)










