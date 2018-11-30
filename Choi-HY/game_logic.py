# -*- coding: utf-8 -*-
import random
import copy

class player():
    def __init__(self, nickname):
        self.nickname=nickname
        self.card_list=list(range(1,8))
        self.reward_dict={'자유로운 공강':1, '행복한 취미생활':1, '편안한 숙면':1}

    def put_card(self, card_num):
        try:
            self.card_list.remove(card_num)
        except ValueError:
            print("Choose From What You Have") #client에서 출력
            return False
        else:
            self.card_list.sort()
            return True

    def get_reward(self,  amount):
        ind=0
        for i in amount:
            self.reward_dict[reward_name[ind]]=self.reward_dict[reward_name[ind]]+i
            ind=ind+1

    def take_time(self):
        waste=max(self.reward_dict.items(), key = lambda x: x[1])[0]
        self.reward_dict[waste]=0

    def init_time(self):
        self.card_list=list(range(1,8))

    def init_reward(self):
        self.reward_dict={'자유로운 공강':1, '행복한 취미생활':1, '편안한 숙면':1}

    def return_reward(self):
        sum=self.reward_dict['자유로운 공강']+self.reward_dict['행복한 취미생활']+self.reward_dict['편안한 숙면']
        return sum

class time_monster():
    def __init__(self, name, reward, hp):
        self.name=name
        self.reward=reward
        self.hp=hp

    def return_reward(self, rank):
        return self.reward[rank]

def get_input(play):
    global player_list
    tmp=int(input('input choice')) #client에서 출력
    return [tmp, player_list[play]]

def print_status(): #전부 client에서 출력
    for j in player_list:
        print(j.nickname)
        print(j.card_list)
        print(j.reward_dict)

def run_game(num, round_num, task_stage):
    for i in range(round_num):
        tmp=random.randint(0, 4-i)
        task_now=task_stage[tmp]
        task_stage.pop(tmp)
        print(task_now.name) #client에서 출력
        print(task_now.hp) #client에서 출력

        input_list=[]

        for i in range(num):
            while True:
                tmp=get_input(i)
                if tmp[1].put_card(tmp[0]):
                    input_list.append(tmp)
                    break

        input_list_new = copy.copy(input_list)

        for i in input_list:
            for j in input_list:
                if i[0]==j[0] and i!=j:
                    input_list.remove(i)
                    input_list.remove(j)

        tot=0
        for i in input_list:
            tot=tot+i[0]

        if task_now.hp<=tot:
            print("Success") #client에서 출력
            for i in range(3):
                min=99999
                for j in input_list:
                    if j[0]<min:
                        min=j[0]
                for j in input_list:
                    if j[0]==min:
                        j[1].get_reward(task_now.reward[i])
                        input_list.remove(j)

        else:
            print("Failed") #client에서 출력
            min=99999
            for i in input_list_new:
                if i[0]<min:
                    min=i[0]
            for i in input_list_new:
                if i[0]==min:
                    i[1].take_time()

        print_status()

def best_player():
    max_num=0
    for i in player_list:
        if max_num<i.return_reward():
            max_num=i.return_reward()
    for i in player_list:
        if max_num==i.return_reward():
            print('1st : '+i.nickname) #client에서 출력

def play_again():
    return input('Press Y to restart').lower().startswith('y') #이건 바뀔 예정


num_player=0

while True:
    num_player=int(input('insert num')) #client에서 출력
    if num_player>5 or num_player<=0-1:
        print("Invalid Input") #client에서 출력
        continue
    else:
        while True:
            nick_player = tuple(input('names?').split(' ')) #이것도 바뀔 예정
            if len(nick_player) == num_player:
                break
            else:
                print("Invalid Input") #client에서 출력
                continue
    break

player_list=[]

#server에 저장 - 과제 리스트
task_name1=['KYPT', '세종수학축전', '한화사이언스챌린지', '해커톤', '동아리 발표 대회']
task_name2=['융합@수학 산출물', '삼성 휴먼테크 논문대상', '객체지향프로그래밍 프로젝트', '도시환경과 도시계획 연구', '논리적 글쓰기 인문학보고서']
task_name3=['의자 만들기', '스파게티 다리 만들기', '교류 발전기 만들기', '논문 분석', '창작 시 콘서트']
task_name_all=[task_name1, task_name2, task_name3]
task_header=['외부활동', '연구활동', '조별과제']
task_list={}

#server에 저장 - 보상 리스트
reward_list=[[[3, 1, 2], [1, 1, 2], [0, 1, 0]], [[3, 0, 0], [0, 2, 0], [0, 0, 1]], [[2, 1, 2], [1, 0, 1], [0, 1, 0]], [[2, 2, 2], [1, 1, 1], [0, 0, 0]], [[1, 2, 1], [0, 0, 0], [0, 0, 0]]]
time_name={1:'공강시간1', 2:'1차자습시간', 3:'공강시간2', 4:'1, 2차 자습시간', 5:'공강시간3', 6:'평일자습시간', 7:'주말자습시간', 8:'밤샘시간'}
reward_name=['자유로운 공강', '행복한 취미생활', '편안한 숙면']
hp_list=[8, 11, 14, 17, 20]

for i in range(3):
    tmp=[]
    key = random.randint(1, 5)
    for j in range(5):
        tmp.append(time_monster(task_name_all[i][j], reward_list[(key+j)%5], int(hp_list[(key+j)%5]*num_player/5)))
    task_list[task_header[i]]=tmp


for i in range(num_player):
    player_list.append(player(nick_player[i]))

stage_num=3
round_num=5


while True:
    for j in player_list:
        j.init_reward()
    for i in range(stage_num):
        task_tmp=copy.deepcopy(task_list)
        print(task_header[i])
        run_game(num_player, round_num, task_tmp[task_header[i]])
        for j in player_list:
            j.init_time()
        best_player()
    best_player()
    if play_again():
        continue
    else:
        break
