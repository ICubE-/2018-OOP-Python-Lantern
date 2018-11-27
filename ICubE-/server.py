import socket
import threading

server_ip = '127.0.0.1'
server_port = 51742
banned_letters_in_nickname = "`~!@#$%^&*()-=+[]{}\\|;:'\",<.>/?"

client_sock_list = []       # 클라이언트 소켓을 저장하는 리스트.
client_id_dict = {}         # 클라이언트 ID를 키로 하여 튜플 안에 닉네임과 게임방 이름을 저장하는 딕셔너리.
room_dict = {}              # 게임방 이름을 키로 하여 리스트 안에 클라이언트 ID를 저장하는 딕셔너리.


class RoomThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def add_client(self):
        pass

    def run(self):
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

    def run(self):
        global client_id_dict
        global room_dict
        
        while True:
            try:
                data = self.client_sock.recv(1024)
            except ConnectionError:
                return
            self.nickname = data.decode('utf-8')
            if len(self.nickname)>10:
                self.client_sock.send(bytes("$tooLongNickname", 'utf-8'))
                continue
            flag = False
            for letter in self.nickname:
                if letter in banned_letters_in_nickname:
                    flag = True
                    break
            if flag:
                self.client_sock.send(bytes("$bannedLetterInNickname", 'utf-8'))
                continue
            self.client_sock.send(bytes("$confirmNickname", 'utf-8'))
            break
        client_id_dict[self.client_id] = (self.nickname, "")

        self.client_sock.send(bytes(repr(tuple(room_dict.keys())), 'utf-8'))
        try:
            data = self.client_sock.recv(1024)
        except ConnectionError:
            return
        selected_room = data.decode('utf-8')

        if selected_room not in room_dict:
            room_dict.setdefault(selected_room, RoomThread)
            room_dict[selected_room].start()
        room_dict[selected_room].add_client(self.client_sock)
        client_id_dict[self.client_id] = (self.nickname, selected_room)

        room_dict[selected_room].join()

        # WIP


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
