import socket
from threading import Thread
import random
import time
import copy

server_ip = '127.0.0.1'
server_port = 51742

room_dict = {}  # 게임방 이름을 키로 하여 리스트 안에 게임방 스레드를 저장하는 딕셔너리.

# server에 저장 - 과제 리스트
task_name1 = ['KYPT', '세종수학축전', '한화사이언스챌린지', '세종 해커톤', '동아리 발표 대회']
task_name2 = ['융합@수학 산출물', '삼성휴먼테크논문쓰기', '객체지향프로그래밍 프로젝트', '도시환경과 도시계획 연구', '논리적글쓰기 인문학보고서']
task_name3 = ['공학개론 의자 만들기', '스파게티 다리 만들기', '고급물리 교류 발전기 만들기', '사회문제와인문학적상상력 발표', '창작 시 콘서트']
task_name_all = [task_name1, task_name2, task_name3]
task_header = ['외부활동', '연구활동', '조별과제']
task_list = {}

# server에 저장 - 보상 리스트
reward_list = [[[3, 1, 2], [1, 1, 2], [0, 1, 0]], [[3, 0, 0], [0, 2, 0], [0, 0, 1]], [[2, 1, 2], [1, 0, 1], [0, 1, 0]], [[2, 2, 2], [1, 1, 1], [0, 0, 0]], [[1, 2, 1], [0, 0, 0], [0, 0, 0]]]
time_name = {1: '공강시간1', 2: '1차자습시간', 3: '공강시간2', 4: '1, 2차 자습시간', 5: '공강시간3', 6: '평일자습시간', 7: '주말자습시간', 8: '밤샘시간'}
reward_name = ['자유로운 공강', '행복한 취미생활', '편안한 숙면']
hp_list = [8, 11, 14, 17, 20]

STAGE_NUM = 3
ROUND_NUM = 5


def get_input(play, pl_list):
    while True:
        play.player_thread.send(bytes('$getInput', 'utf-8'))
        data = play.player_thread.receive().decode('utf-8')
        if data.split()[0] == "$btn":
            data = int(' '.join(data.split()[1:]))
            if play.put_card(data):
                return [data, play]
        else:
            for i in pl_list:
                i.player_thread.send(bytes(data, 'utf-8'))



class InputThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return
# source from https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python

def print_status(player_list):  # 전부 client에서 출력
    for j in player_list:
        j.player_thread.send(bytes(repr(j.card_list)))
        j.player_thread.send(bytes(repr(j.reward_dict)))


def run_game(round_num, task_stage, player_list):
    for i in range(round_num):
        tmp = random.randint(0, 4 - i)
        task_now = task_stage[tmp]
        task_stage.pop(tmp)
        for play in player_list:
            play.player_thread.send(bytes("$monsterInfo "+repr((task_now.name, task_now.hp)), 'utf-8'))
        time.sleep(0.5)

        input_list = []
        InputThread_list=[]
        for k in player_list:
            InputThread_list.append(InputThread(target=get_input, args=(k, player_list, )))
        for q in InputThread_list:
            q.start()
        for r in InputThread_list:
            input_list.append(r.join())
        input_list_only_num = []
        for i in input_list:
            input_list_only_num.append(input_list[0])
        input_list_new = copy.copy(input_list)
        for i in input_list:
            chk=False
            for j in input_list:
                if i[0] == j[0] and i[1] != j[1]:
                    input_list.remove(j)
                    chk=True
            if chk:
                input_list.remove(i)

        tot = 0
        for input_val in input_list:
            tot = tot + input_val[0]

        if task_now.hp <= tot:
            for play in player_list:
                play.player_thread.send(bytes("$Success "+str(tot), 'utf-8'))
            for number in range(3):
                min_val = 99999
                for j in input_list:
                    if j[0] < min_val:
                        min_val = j[0]
                for j in input_list:
                    if j[0] == min_val:
                        j[1].get_reward(task_now.reward[i])
                        input_list.remove(j)

        else:
            for play in player_list:
                play.player_thread.send(bytes("$Failed "+str(tot), 'utf-8')) # client에서 출력
            min_val = 99999
            for k in input_list_new:
                if k[0] < min_val:
                    min_val = k[0]
            for k in input_list_new:
                if k[0] == min_val:
                    k[1].take_time()

        print_status(player_list)


class Player():
    def __init__(self, player_thread):
        self.nickname = player_thread.nickname
        self.card_list = [1, 1, 1, 1, 1, 1, 1, 1]
        self.reward_dict = {'자유로운 공강': 1, '행복한 취미생활': 1, '편안한 숙면': 1}
        self.player_thread = player_thread

    def put_card(self, card_num):
        if self.card_list[card_num-1]:
            self.card_list[card_num-1] = 0
            return True
        else:
            self.player_thread.send(bytes("Choose From What You Have", 'utf-8'))
            return False

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
        sum_reward = self.reward_dict['자유로운 공강'] + self.reward_dict['행복한 취미생활'] + self.reward_dict['편안한 숙면']
        return sum_reward


class TimeMonster():
    def __init__(self, name, reward, hp):
        self.name = name
        self.reward = reward
        self.hp = hp

    def return_reward(self, rank):
        return self.reward[rank]

class RoomThread(Thread):
    def __init__(self, room_name):
        Thread.__init__(self)
        self.room_name = room_name
        self.member_thread = []
        self.status = 0  # 0: before start, 1: started, 2: finished
        self.player_list = []
        self.member_is_ready = {}
        self.status = 0  # 0: before start, 1: started, 2: finished

    def add_client(self, client_thread):
        self.member_thread.append(client_thread)
        self.member_is_ready.setdefault(client_thread.nickname, False)
        if self.member_thread.__len__() == 1:
            client_thread.send(bytes("$giveHead", 'utf-8'))
        time.sleep(0.1)
        self.chat_members_list()

    def del_client(self, client_thread):
        if self.member_thread.index(client_thread) == 0:
            if self.member_thread.__len__() == 1:
                room_dict.pop(self.room_name)
                self.status = 2
            else:
                self.member_thread[1].send(bytes("$giveHead", 'utf-8'))
        self.member_is_ready.pop(client_thread.nickname)
        self.member_thread.remove(client_thread)
        self.chat_members_list()

    def chat_members_list(self):
        members_nickname_list = []
        for thread in self.member_thread:
            members_nickname_list.append((thread.nickname, self.member_is_ready[thread.nickname]))
        time.sleep(0.1)
        self.chat(bytes("$setMembers " + repr(tuple(members_nickname_list)), 'utf-8'))

    def chat(self, data):
        for thread in self.member_thread:
            thread.send(data)

    def game(self):
        self.chat(bytes("$gameStarted", 'utf-8'))
        # WIP
        for i in range(3):
            tmp = []
            key = random.randint(1, 5)
            for j in range(5):
                tmp.append(TimeMonster(task_name_all[i][j], reward_list[(key + j) % 5],
                                        int(hp_list[(key + j) % 5] * len(self.member_thread) / 5)))
            task_list[task_header[i]] = tmp
        for i in self.member_thread:
            self.player_list.append(Player(i))
        for j in self.player_list:
            j.init_reward()
        for i in range(STAGE_NUM):
            task_tmp = copy.deepcopy(task_list)
            run_game(ROUND_NUM, task_tmp[task_header[i]], self.player_list)
            for j in self.player_list:
                j.init_time()
            max_num = 0
            for k in self.player_list:
                if max_num < k.return_reward():
                    max_num = k.return_reward()
            for k in self.player_list:
                if max_num == k.return_reward():
                    self.chat('1st : ' + k.nickname)
        for thread in self.member_thread:
            thread.client_sock.send(bytes("Game Over", 'utf-8'))
        self.status = 2
        # WIP

    def run(self):
        while self.status != 2:
            pass


class ClientThread(Thread):
    """
    각 클라이언트를 위한 스레드.
    """

    def __init__(self, client_sock, client_id):
        Thread.__init__(self)
        self.client_sock = client_sock
        self.client_id = client_id
        self.nickname = ""
        self.room_name = ""
        self.status = 0  # 0: no problem, 1: quit error, 2: quit no error

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
        room_dict[self.room_name].add_client(self)

    def run(self):
        global room_dict

        self.select_nickname()
        if self.status != 0:
            return
        while True:
            self.select_room()
            if self.status != 0:
                return
            my_room = room_dict[self.room_name]
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
                elif data.decode('utf-8') == "$ready":
                    my_room.member_is_ready[self.nickname] = not my_room.member_is_ready[self.nickname]
                    my_room.chat_members_list()
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
