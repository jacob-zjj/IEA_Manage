# 这里定义一个包含了所有与设备进行IPv6通信并获取数据的类
# 通过向设备发送报文 接受报文来获取数据设备实时数据
import socket
import sys
class ClientToIPv6:
    def __init__(self):
        # 创建一个私有变量来保存socket通信对象
        self.__tcpT6Client = socket.socket()

    def connect(self):
        flag = False
        try:
            self.__tcpT6Client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            # tcpT6Client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            self.__tcpT6Client.connect(('fe80::8000:0:0:e1', 502))
            flag = True
        except socket.error as msg:
            print(msg)
            print("IPv6未联通，请确认边缘网关已经开启！！！")
            sys.exit(1)

    # 1代表设备1
    def temperature1(self):
        self.__tcpT6Client.send(b"\x01\x03\x00\x01\x00\x01\xd5\xca")
        res = self.__tcpT6Client.recv(1024)
        # 解析温度数据
        result = ( res[3] * 256 + res[4] ) / 10
        return result

    def humidity1(self):
        self.__tcpT6Client.send(b"\x01\x03\x00\x00\x00\x01\x84\x0a")
        res = self.__tcpT6Client.recv(1024)
        # 解析湿度数据
        result = ( res[3] * 256 + res[4] ) / 1000
        return result

    def floodLight1(self):
        self.__tcpT6Client.send(b"\x01\x03\x00\x06\x00\x01\x64\x0b")
        res = self.__tcpT6Client.recv(1024)
        # 解析光照数据
        result = ( res[3] * 256 + res[4] )
        return result

    # 8代表设备8
    def temperature8(self):
        self.__tcpT6Client.send(b"\x08\x03\x00\x01\x00\x01\xd5\x53")
        res = self.__tcpT6Client.recv(1024)
        # 解析温度数据
        result = ( res[3] * 256 + res[4] ) / 10
        return result

    def humidity8(self):
        self.__tcpT6Client.send(b"\x08\x03\x00\x00\x00\x01\x84\x93")
        res = self.__tcpT6Client.recv(1024)
        # 解析湿度数据
        result = ( res[3] * 256 + res[4] ) / 1000
        return result

    def floodLight8(self):
        self.__tcpT6Client.send(b"\x08\x03\x00\x06\x00\x01\x64\x92")
        res = self.__tcpT6Client.recv(1024)
        # 解析光照数据
        result = ( res[3] * 256 + res[4] )
        return result

    # 2代表设备2
    def atPressure2(self):
        self.__tcpT6Client.send(b"\x02\x03\x00\x00\x00\x01\x84\x39")
        res = self.__tcpT6Client.recv(1024)
        # 解析温度数据
        result = (res[3] * 256 + res[4])
        return result

    def temperature2(self):
        self.__tcpT6Client.send(b"\x02\x03\x00\x01\x00\x01\xd5\xf9")
        res = self.__tcpT6Client.recv(1024)
        # 解析温度数据
        result = ( res[3] * 256 + res[4] )
        return result

    # 7代表设备7
    def atPressure7(self):
        self.__tcpT6Client.send(b"\x07\x03\x00\x00\x00\x01\x84\x6c")
        res = self.__tcpT6Client.recv(1024)
        # 解析温度数据
        result = (res[3] * 256 + res[4])
        return result

    def temperature7(self):
        self.__tcpT6Client.send(b"\x07\x03\x00\x01\x00\x01\xd5\xac")
        res = self.__tcpT6Client.recv(1024)
        # 解析温度数据
        result = ( res[3] * 256 + res[4] )
        return result

    # 关闭socket IPv6通信通信
    def colse(self):
        self.__tcpT6Client.close()