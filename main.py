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
import json



with open("config/rf_params.json", "r") as file:
    rf_params = (json.loads(file.read()))

# list of anchors to configure
anchors_conf = []
with open("config/anchors.json", "r") as file:
    for line in file:
        anchors_conf.append(json.loads(line))

print(type(anchors_conf[0]))

s = socket.socket()
# s.connect(('127.0.1.2', 8888))
s.connect(('192.168.1.22', 5051))

while 1:
    data = input()
    if data == "1":
        for anchor in anchors_conf:
            data2send = anchor
            data2send["type"] = "new_anchor"
            data2send = json.dumps(data2send).encode()
            s.sendall(len(data2send).to_bytes(4, "little"))
            s.sendall(data2send)

    if data == "2":
        data2send = {}
        data2send["type"] = "relate_to_masters"
        data2send = json.dumps(data2send).encode()
        s.sendall(len(data2send).to_bytes(4, "little"))
        s.sendall(data2send)

    if data == "3":
        data2send = rf_params
        data2send["type"] = "rf_config"
        data2send = json.dumps(data2send).encode()
        s.sendall(len(data2send).to_bytes(4, "little"))
        s.sendall(data2send)

    if data == "go":
        data2send = {}
        data2send["type"] = "Start"
        data2send = json.dumps(data2send).encode()
        s.sendall(len(data2send).to_bytes(4, "little"))
        s.sendall(data2send)

    if data == "stop":
        data2send = {}
        data2send["type"] = "Stop"
        data2send = json.dumps(data2send).encode()
        s.sendall(len(data2send).to_bytes(4, "little"))
        s.sendall(data2send)



    # s.sendall(data.encode())
    if data == "howmuch":
        print((s.recv(100)).decode())

