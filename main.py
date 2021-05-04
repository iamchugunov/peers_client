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
import threading


with open("config/rf_params_ttk.json", "r") as file:
    rf_params = (json.loads(file.read()))

# list of anchors to configure
anchors_conf = []
with open("config/anchors.json", "r") as file:
    for line in file:
        anchors_conf.append(json.loads(line))

print((anchors_conf))

s = socket.socket()
s.connect(('192.168.99.52', 5051))

s1 = socket.socket()
s1.connect(('192.168.99.52', 5052))

def send_to_server(data2send, s):
    data2send = json.dumps(data2send).encode()
    s.sendall(len(data2send).to_bytes(4, "little"))
    s.sendall(data2send)

def requester():
    while 1:
        data = input()

        if data == "1":
            for anchor in anchors_conf:
                data2send = anchor
                data2send["type"] = "new_anchor"
                send_to_server(data2send, s)

        if data == "2":
            data2send = {}
            data2send["type"] = "relate_to_masters"
            send_to_server(data2send, s)

        if data == "3":
            data2send = rf_params
            data2send["type"] = "rf_config"
            send_to_server(data2send, s)

        if data == "go":
            data2send = {}
            data2send["type"] = "Start"
            send_to_server(data2send, s)

        if data == "stop":
            data2send = {}
            data2send["type"] = "Stop"
            send_to_server(data2send, s)

        if data == "get anchors":
            data2send = {}
            data2send["type"] = 'get_anchors'
            send_to_server(data2send, s)
            rcv_size = int.from_bytes(s.recv(4), 'little')
            msg = json.loads(s.recv(rcv_size).decode())
            for anchor in msg:
                print(anchor)

        if data == "get tags":
            data2send = {}
            data2send["type"] = 'get_tags'
            send_to_server(data2send, s)
            rcv_size = int.from_bytes(s.recv(4), 'little')
            msg = json.loads(s.recv(rcv_size).decode())
            for tag in msg:
                print(tag)

def streamer():
    while 1:
        rcv_size = int.from_bytes(s1.recv(4), 'little')
        msg = json.loads(s1.recv(rcv_size).decode())
        print(msg)

mainthread = threading.Thread(target=requester)
streamthread = threading.Thread(target=streamer)
mainthread.start()
print("main started")
streamthread.start()
print("stream started")