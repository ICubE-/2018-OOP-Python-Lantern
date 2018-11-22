import socket
import threading

server_ip = '127.0.0.1'
server_port = 51742
banned_letters_in_nickname = "`~!@#$%^&*()-=+[]{}\\|;:'\",<.>/?"

client_sock_list = []       # 클라이언트 소켓을 저장하는 리스트.
client_id_list = {}         # 클라이언트 ID를 키로 하여 튜플 안에 닉네임과 게임방 이름을 저장하는 딕셔너리.
room = {}                   # 게임방 이름을 키로 하여 리스트 안에 클라이언트 ID를 저장하는 딕셔너리.


class ClientThread(threading.Thread):
    """
    각 클라이언트를 위한 스레드.
    """
    def __init__(self, client_sock, client_id):
        threading.Thread.__init__(self)
        self.client_sock = client_sock
        self.client_id = client_id
        self.nickname = ""

    def run(self):
        while True:
            self.client_sock.send(bytes("사용할 이름을 입력하세요.", 'utf-8'))
            data = self.client_sock.recv()
            self.nickname = data.decode('utf-8')
            flag = True
            for i in banned_letters_in_nickname:
                if i in self.nickname:
                    flag = False
                    break
            if flag:
                break
        global client_id_list
        client_id_list[self.client_id] = (self.nickname, "")

        # WIP


def connect():
    """
    소켓 연결을 위한 함수.

    :return: 없다.
    """
    global client_sock_list
    global client_id_list

    while True:
        client_sock, client_address = server_sock.accept()
        client_sock_list.append(client_sock)
        client_id_list.setdefault(client_sock.fileno(), ("", ""))

        ClientThread(client_sock, client_sock.fileno())


server_address = (server_ip, server_port)

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(server_address)
server_sock.listen()
print("start")

connect()

server_sock.close()
