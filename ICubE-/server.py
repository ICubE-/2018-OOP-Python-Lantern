import socket
import threading

server_ip = '127.0.0.1'
server_port = 51742


def connect():
    pass


server_address = (server_ip, server_port)

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(server_address)
server_sock.listen()
print("start")

thread_server = threading.Thread(target=connect, args=())
thread_server.start()