import socket
import threading
import time

server_ip = '127.0.0.1'
server_port = 51742

room_dict = {}              # 게임방 이름을 키로 하여 리스트 안에 게임방 스레드를 저장하는 딕셔너리.


class RoomThread(threading.Thread):
    def __init__(self, room_name):
        threading.Thread.__init__(self)
        self.room_name = room_name
        self.member_thread = []
        self.status = 0     # 0: before start, 1: started, 2: finished

    def add_client(self, client_thread):
        self.member_thread.append(client_thread)

    def del_client(self, client_thread):
        if self.member_thread.index(client_thread) == 0:
            if self.member_thread.__len__() == 1:
                self.status = 2
            else:
                self.member_thread[1].send(bytes("$giveHead", 'utf-8'))
        self.member_thread.remove(client_thread)

    def chat(self, data):
        for thread in self.member_thread:
            thread.client_sock.send(data)

    def game(self):
        for thread in self.member_thread:
            thread.client_sock.send(bytes("$gameStarted", 'utf-8'))
        # WIP
        for thread in self.member_thread:
            thread.client_sock.send(bytes("Game Over", 'utf-8'))
        self.status = 2
        # WIP

    def run(self):
        while self.status != 2:
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
        self.status = 0     # 0: no problem, 1: quit error, 2: quit no error

    def alert_connection_error(self):
        print("{}({})의 연결이 비정상적으로 종료되었습니다.".format(self.client_id, self.nickname))
        self.status = 1

    def receive(self):
        try:
            data = self.client_sock.recv(1024)
        except ConnectionError:
            self.alert_connection_error()
            return
        if not data:
            self.alert_connection_error()
            return
        elif data.decode('utf-8') == "$quit":
            self.status = 2
            print("{}({})의 연결이 종료되었습니다.".format(self.client_id, self.nickname))
        return data

    def send(self, data):
        try:
            self.client_sock.send(data)
        except ConnectionError:
            self.alert_connection_error()

    def select_nickname(self):
        global room_dict

        data = self.receive()
        if self.status != 0:
            return
        self.nickname = data.decode('utf-8')

    def select_room(self):
        global room_dict

        available_room_name = []
        for room in room_dict.values():
            if room.status == 0:
                available_room_name.append(room.room_name)
        self.send(bytes(repr(tuple(available_room_name)), 'utf-8'))
        if self.status != 0:
            return

        print("{}({})에게 방 정보를 보냈습니다.".format(self.client_id, self.nickname))
        data = self.receive()
        if self.status != 0:
            return
        self.room_name = data.decode('utf-8')

        if self.room_name not in room_dict:
            room_dict.setdefault(self.room_name, RoomThread(self.room_name))
            room_dict[self.room_name].start()
            self.send(bytes("$giveHead", 'utf-8'))
        room_dict[self.room_name].add_client(self)

    def run(self):
        global room_dict

        print("{}({})와 연결되었습니다.".format(self.client_id, self.nickname))
        self.select_nickname()
        if self.status != 0:
            return
        print("{}({})의 닉네임이 지정되었습니다.".format(self.client_id, self.nickname))
        while True:
            self.select_room()
            if self.status != 0:
                return
            my_room = room_dict[self.room_name]
            print("{}({})이 방 {}로 들어갔습니다.".format(self.client_id, self.nickname, my_room.room_name))
            temp = 0
            while True:
                if my_room.status == 1:
                    break
                data = self.receive()
                if self.status != 0:
                    my_room.del_client(self)
                    return
                if data.decode('utf-8') == "$gameStart":
                    my_room.game()
                elif data.decode('utf-8') == "$leave":
                    my_room.del_client(self)
                    self.send(bytes("$tmp", 'utf-8'))
                    temp = 1
                    break
                else:
                    my_room.chat(bytes(self.nickname + " : ", 'utf-8') + data)
            if temp:
                continue
            while True:
                data = self.receive()
                my_room.chat(bytes(self.nickname + " : ", 'utf-8') + data)


def connect():
    """
    소켓 연결을 위한 함수.

    :return: 없다.
    """

    while True:
        client_sock, client_address = server_sock.accept()

        ClientThread(client_sock, client_sock.fileno()).start()


server_address = (server_ip, server_port)

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(server_address)
server_sock.listen()
print("start")

connect()

server_sock.close()
