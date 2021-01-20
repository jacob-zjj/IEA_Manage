# 开启一个客户端去连接边缘网关服务器
# 这里定义一个包含了所有与设备进行IPv6通信并获取数据的类
# 通过向设备发送报文 接受报文来获取数据设备实时数据
import socket
import sys
class ClientToServer:
    def __init__(self):
        # 创建一个私有变量来保存socket通信对象
        self.__tcpT6Client = socket.socket()

    def connect(self):
        try:
            # self.__tcpT6Client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            # 这里将2001::1 改为对应服务器的IPv6地址相连接
            # self.__tcpT6Client.connect(('2001::1', 502))

            # IPv4 通信
            self.__tcpT6Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__tcpT6Client.connect(('192.168.1.102', 21136))

        except socket.error as msg:
            print(msg)
            print("IPv6未联通，请确认边缘网关已经开启！！！")
            sys.exit(1)

    # 在底层服务器中已经将每个设备对应了不同的id 因此需要获得不同设备的数据
    # 只需要返回数据即可
    def sendDeviceId(self, id):
        self.__tcpT6Client.send(str(id).encode())
        res = self.__tcpT6Client.recv(1024)
        return float(res)

    # 关闭socket IPv6通信通信
    def close(self):
        self.__tcpT6Client.close()