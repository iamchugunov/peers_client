import socket
import json
import threading
import commands as co

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

co.send_state_request(s)
msg = co.receive_from_server(s)

s1 = socket.socket()
s1.connect(('192.168.99.52', 5052))



def requester():
    while 1:
        data = input()

        if data == "1":
            for anchor in anchors_conf:
                co.send_anchor_info(anchor, s)


        if data == "2":
            co.send_relate_to_masters(s)

        if data == "3":
            co.send_rf_config(rf_params, s)

        if data == "go":
            co.send_start(s)

        if data == "stop":
            co.send_stop(s)

        if data == "get anchors":
            co.send_get_anchors(s)
            msg = co.receive_from_server(s)
            for anchor in msg:
                print(anchor)

        if data == "get tags":
            co.send_get_tags(s)
            msg = co.receive_from_server(s)
            for tag in msg:
                print(tag)

        if data == "state request":
            co.send_state_request(s)
            msg = co.receive_from_server(s)
            print(msg)


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