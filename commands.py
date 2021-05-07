import json

def send_to_server(data2send, s):
    data2send = json.dumps(data2send).encode()
    s.sendall(len(data2send).to_bytes(4, "little"))
    s.sendall(data2send)


def receive_from_server(s):
    rcv_size = int.from_bytes(s.recv(4), 'little')
    msg = json.loads(s.recv(rcv_size).decode())
    return msg


def send_anchor_info(anchor, s):
    data2send = anchor
    data2send["type"] = "new_anchor"
    send_to_server(data2send, s)


def send_relate_to_masters(s):
    data2send = {}
    data2send["type"] = "relate_to_masters"
    send_to_server(data2send, s)


def send_rf_config(rf_params, s):
    data2send = rf_params
    data2send["type"] = "rf_config"
    send_to_server(data2send, s)


def send_start(s):
    data2send = {}
    data2send["type"] = "Start"
    send_to_server(data2send, s)


def send_stop(s):
    data2send = {}
    data2send["type"] = "Stop"
    send_to_server(data2send, s)


def send_get_anchors(s):
    data2send = {}
    data2send["type"] = 'get_anchors'
    send_to_server(data2send, s)


def send_get_tags(s):
    data2send = {}
    data2send["type"] = 'get_tags'
    send_to_server(data2send, s)


def send_state_request(s):
    data2send = {}
    data2send["type"] = 'state_request'
    send_to_server(data2send, s)


