from . import ClientToIPv6
ClientToIPv6 = ClientToIPv6.ClientToIPv6()
ClientToIPv6.connect()
res = ClientToIPv6.atPressure7()
print(res)