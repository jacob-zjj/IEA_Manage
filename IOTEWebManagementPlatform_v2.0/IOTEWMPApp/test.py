import socket
tcpT6Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpT6Client.connect(('192.168.1.102', 21136))
while True:
    for i  in  range(17):
        tcpT6Client.send(str(i).encode())
        res = tcpT6Client.recv(1024)
        print(float(res))

tcpT6Client.close()