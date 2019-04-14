#!/usr/bin/python3
import socket
import json
import time
import psutil as ps


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', 25125))
server_socket.listen(1)

def get_data():
    cpu_count = ps.cpu_count(logical=False)
    cpu_percent = ps.cpu_percent(interval=None, percpu=True)
    total, available, percent, used, free, *rest = ps.virtual_memory()
    total_swap, used_swap, free_swap, percent_swap, *rest = ps.swap_memory()
    total_disk, used_disk, free_disk, percent_disk = ps.disk_usage('/')
    username, *rest = ps.users()
    return {
        'cpu_count': cpu_count,
        'cpu_percent': cpu_percent,
        'totla_memory': total,
        'available_memory': available,
        'percent_memory': percent,
        'used_memory': used,
        'free_memory': free,
        'total_swap': total_swap,
        'used_swap': used_swap,
        'free_swap': free_swap,
        'percent_swap': percent_swap,
        'total_disk': total_disk,
        'used_disk': used_disk,
        'free_disk': free_disk,
        'percent_disk': percent_disk,
        'username': username[0]
    }

def send_message(client_socket):
    while True:
        data = json.dumps(get_data())
        client_socket.send(data.encode())
        time.sleep(1)


def server_loop():
    client_socket, address = server_socket.accept()
    if client_socket:
        try:
            send_message(client_socket)
        except BrokenPipeError:
            print('Connection was lost')
            client_socket.close()

server_loop()