import socket
import threading
import random
import copy

server_ip = '127.0.0.1'
server_port = 51742
banned_letters_in_nickname = "`~!@#$%^&*()-=+[]{}\\|;:'\",<.>/? "

client_sock_list = []  # 클라이언트 소켓을 저장하는 리스트.
client_id_dict = {}  # 클라이언트 ID를 키로 하여 튜플 안에 닉네임과 게임방 이름을 저장하는 딕셔너리.
room_dict = {}  # 게임방 이름을 키로 하여 리스트 안에 게임방 스레드를 저장하는 딕셔너리.

# server에 저장 - 과제 리스트
task_name1 = ['KYPT', '세종수학축전', '한화사이언스챌린지', '해커톤', '동아리 발표 대회']
task_name2 = ['융합@수학 산출물', '삼성 휴먼테크 논문대상', '객체지향프로그래밍 프로젝트', '도시환경과 도시계획 연구', '논리적 글쓰기 인문학보고서']
task_name3 = ['의자 만들기', '스파게티 다리 만들기', '교류 발전기 만들기', '논문 분석', '창작 시 콘서트']
task_name_all = [task_name1, task_name2, task_name3]
task_header = ['외부활동', '연구활동', '조별과제']
task_list = {}

# server에 저장 - 보상 리스트
reward_list = [[[3, 1, 2], [1, 1, 2], [0, 1, 0]], [[3, 0, 0], [0, 2, 0], [0, 0, 1]], [[2, 1, 2], [1, 0, 1], [0, 1, 0]],
               [[2, 2, 2], [1, 1, 1], [0, 0, 0]], [[1, 2, 1], [0, 0, 0], [0, 0, 0]]]
time_name = {1: '공강시간1', 2: '1차자습시간', 3: '공강시간2', 4: '1, 2차 자습시간', 5: '공강시간3', 6: '평일자습시간', 7: '주말자습시간', 8: '밤샘시간'}
reward_name = ['자유로운 공강', '행복한 취미생활', '편안한 숙면']
hp_list = [8, 11, 14, 17, 20]


def get_input(play, player_list):
    tmp = int(input('input choice (' + player_list[play].nickname + ') : '))  # client에서 출력
    return [tmp, player_list[play]]


def print_status(player_list):  # 전부 client에서 출력
    for j in player_list:
        print(j.nickname)
        print(j.card_list)
        print(j.reward_dict)


def run_game(num, round_num, task_stage, player_list):
    for i in range(round_num):
        tmp = random.randint(0, 4 - i)
        task_now = task_stage[tmp]
        task_stage.pop(tmp)
        print(task_now.name)  # client에서 출력
        print(task_now.hp)  # client에서 출력

        input_list = []

        for i in range(num):
            while True:
                tmp = get_input(i, player_list)
                if tmp[1].put_card(tmp[0]):
                    input_list.append(tmp)
                    break

        input_list_new = copy.copy(input_list)

        for i in input_list:
            for j in input_list:
                if i[0] == j[0] and i != j:
                    input_list.remove(i)
                    input_list.remove(j)

        tot = 0
        for i in input_list:
            tot = tot + i[0]

        if task_now.hp <= tot:
            print("Success")  # client에서 출력
            for i in range(3):
                min = 99999
                for j in input_list:
                    if j[0] < min:
                        min = j[0]
                for j in input_list:
                    if j[0] == min:
                        j[1].get_reward(task_now.reward[i])
                        input_list.remove(j)

        else:
            print("Failed")  # client에서 출력
            min = 99999
            for i in input_list_new:
                if i[0] < min:
                    min = i[0]
            for i in input_list_new:
                if i[0] == min:
                    i[1].take_time()

        print_status()


def best_player(player_list):
    max_num = 0
    for i in player_list:
        if max_num < i.return_reward():
            max_num = i.return_reward()
    for i in player_list:
        if max_num == i.return_reward():
            print('1st : ' + i.nickname)  # client에서 출력


def play_again():
    return input('Press Y to restart').lower().startswith('y')  # 이건 바뀔 예정


class player():
    def __init__(self, nickname):
        self.nickname = nickname
        self.card_list = list(range(1, 8))
        self.reward_dict = {'자유로운 공강': 1, '행복한 취미생활': 1, '편안한 숙면': 1}

    def put_card(self, card_num):
        try:
            self.card_list.remove(card_num)
        except ValueError:
            print("Choose From What You Have")  # client에서 출력
            return False
        else:
            self.card_list.sort()
            return True

    def get_reward(self, amount):
        ind = 0
        for i in amount:
            self.reward_dict[reward_name[ind]] = self.reward_dict[reward_name[ind]] + i
            ind = ind + 1

    def take_time(self):
        waste = max(self.reward_dict.items(), key=lambda x: x[1])[0]
        self.reward_dict[waste] = 0

    def init_time(self):
        self.card_list = list(range(1, 8))

    def init_reward(self):
        self.reward_dict = {'자유로운 공강': 1, '행복한 취미생활': 1, '편안한 숙면': 1}

    def return_reward(self):
        sum = self.reward_dict['자유로운 공강'] + self.reward_dict['행복한 취미생활'] + self.reward_dict['편안한 숙면']
        return sum


class time_monster():
    def __init__(self, name, reward, hp):
        self.name = name
        self.reward = reward
        self.hp = hp

    def return_reward(self, rank):
        return self.reward[rank]


class RoomThread(threading.Thread):
    def __init__(self, room_name):
        threading.Thread.__init__(self)
        self.room_name = room_name
        self.member_thread = []
        self.status = 0  # 0: before start, 1: started, 2: finished

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
        for i in range(3):
            tmp = []
            key = random.randint(1, 5)
            for j in range(5):
                tmp.append(time_monster(task_name_all[i][j], reward_list[(key + j) % 5],
                                        int(hp_list[(key + j) % 5] * len(self.member_thread) / 5)))
            task_list[task_header[i]] = tmp
        player_list = []
        for i in self.member_thread:
            player_list.append(player(i.nickname))
        run_game()
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
        self.status = 0  # 0: no problem, 1: quit

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
            if len(self.nickname) > 10:
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

        available_room_name = []
        for room in room_dict.values():
            if room.status == 0:
                available_room_name.append(room.room_name)
        self.send(bytes(repr(tuple(available_room_name)), 'utf-8'))
        if self.status == 1:
            return
        data = self.receive()
        self.room_name = data.decode('utf-8')

        if self.room_name not in room_dict:
            room_dict.setdefault(self.room_name, RoomThread(self.room_name))
            room_dict[self.room_name].start()
            self.send(bytes("$giveHead", 'utf-8'))
        room_dict[self.room_name].add_client(self)
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
            my_room = room_dict[self.room_name]
            temp = 0
            while True:
                data = self.receive()
                if data.decode('utf-8') == "$gameStart":
                    my_room.game()
                elif data.decode('utf-8') == "$gameStarted":
                    break
                elif data.decode('utf-8') == "$leave":
                    my_room.del_client(self)
                    temp = 1
                    break
                else:
                    my_room.chat(bytes(self.nickname + " : ", 'utf-8') + data)
            if temp:
                continue
            while True:
                data = self.receive()
                break


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
