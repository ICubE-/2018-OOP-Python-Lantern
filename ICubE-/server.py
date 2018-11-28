import socket
import threading
import time

server_ip = '127.0.0.1'
server_port = 51742
banned_letters_in_nickname = "`~!@#$%^&*()-=+[]{}\\|;:'\",<.>/?"

client_sock_list = []       # 클라이언트 소켓을 저장하는 리스트.
client_id_dict = {}         # 클라이언트 ID를 키로 하여 튜플 안에 닉네임과 게임방 이름을 저장하는 딕셔너리.
room_dict = {}              # 게임방 이름을 키로 하여 리스트 안에 게임방 스레드를 저장하는 딕셔너리.


class RoomThread(threading.Thread):
    def __init__(self, room_name):
        threading.Thread.__init__(self)
        self.room_name = room_name
        self.member_sock = []

    def add_client(self, client_sock):
        self.member_sock.append(client_sock)

    def chat(self, sender_nickname, data):
        for sock in self.member_sock:
            sock.send(bytes(sender_nickname + " : ", 'utf-8') + data)

    def run(self):

        while True:
            pass


class ClientThread(threading.Thread):
    """
    각 클라이언트를 위한 스레드.
    """
    def __init__(self, client_sock, client_id):
        threading.Thread.__init__(self)
        self.client_sock = client_sock
        self.client_id = client_id
        self.nickname = ""
        self.room_name = ""
        self.status = 0     # 0: no problem, 1: quit

    def alert_connection_error(self):
        print("{}({})의 연결이 비정상적으로 종료되었습니다.".format(self.client_id, self.nickname))
        self.status = 1

    def receive(self):
        try:
            data = self.client_sock.recv(1024)
        except ConnectionError:
            self.alert_connection_error()
            return
        return data

    def send(self, data):
        try:
            self.client_sock.send(data)
        except ConnectionError:
            self.alert_connection_error()

    def select_nickname(self):
        global client_id_dict
        global room_dict

        while True:
            data = self.receive()
            if self.status == 1:
                return
            self.nickname = data.decode('utf-8')
            if len(self.nickname)>10:
                self.send(bytes("$tooLongNickname", 'utf-8'))
                if self.status == 1:
                    return
                continue
            flag = False
            for letter in self.nickname:
                if letter in banned_letters_in_nickname:
                    flag = True
                    break
            if flag:
                self.send(bytes("$bannedLetterInNickname", 'utf-8'))
                if self.status == 1:
                    return
                continue
            self.send(bytes("$confirmNickname", 'utf-8'))
            if self.status == 1:
                return
            break
        client_id_dict[self.client_id] = (self.nickname, "")

    def select_room(self):
        global client_id_dict
        global room_dict

        self.send(bytes(repr(tuple(room_dict.keys())), 'utf-8'))
        if self.status == 1:
            return
        data = self.receive()
        self.room_name = data.decode('utf-8')

        if self.room_name not in room_dict:
            room_dict.setdefault(self.room_name, RoomThread(self.room_name))
            room_dict[self.room_name].start()
        room_dict[self.room_name].add_client(self.client_sock)
        client_id_dict[self.client_id] = (self.nickname, self.room_name)

    def run(self):
        global client_id_dict
        global room_dict
        
        self.select_nickname()
        if self.status == 1:
            return
        while True:
            self.select_room()
            if self.status == 1:
                return
            while True:
                data = self.receive()
                room_dict[self.room_name].chat(self.nickname, data)


def connect():
    """
    소켓 연결을 위한 함수.

    :return: 없다.
    """
    global client_sock_list
    global client_id_dict

    while True:
        client_sock, client_address = server_sock.accept()
        client_sock_list.append(client_sock)
        client_id_dict.setdefault(client_sock.fileno(), ("", ""))

        ClientThread(client_sock, client_sock.fileno()).start()


server_address = (server_ip, server_port)

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(server_address)
server_sock.listen()
print("start")

connect()

server_sock.close()
