# import asyncio
#
#
# async def tcp_echo_client(message, loop):
#     reader, writer = await asyncio.open_connection('127.0.1.2', 8888)
#
#     print('Send: %r' % message)
#     writer.write(message.encode())
#
#     data = await reader.read(100)
#     print('Received: %r' % data.decode())
#
#     print('Close the socket')
#     writer.close()
#
#
# message = 'Hello World!'
# loop = asyncio.get_event_loop()
# loop.run_until_complete(tcp_echo_client(message, loop))
# loop.close()

import socket

s = socket.socket()
# s.connect(('127.0.1.2', 8888))
s.connect(('192.168.0.196', 5051))

while 1:
    data = input()
    s.sendall(data.encode())
    if data == "howmuch":
        print((s.recv(100)).decode())

