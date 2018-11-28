import random
import copy

class player():
    def __init__(self, nickname):
        self.nickname=nickname
        self.card_list=list(range(1,8))
        self.time_dict={'자유로운 공강':1, '행복한 취미생활':1, '편안한 숙면':1}
    def put_card(self, card_num):
        try:
            self.card_list.remove(card_num)
        except ValueError:
            print("Choose From What You Have")
        else:
            return card_num
            self.card_list.sort()
    def get_time(self, time, amount):
        self.time_dict[time]=self.time_dict[time]+amount
    def take_time(self):
        waste=max(self.time_dict.items(), key=lambda x:x[1])[0]
        waste_time=max(self.time_dict.items(), key=lambda x:x[1])[1]
        self.time_dict[waste]=0
        return waste_time
    def init_time(self):
        self.card_list=list(range(1,8))

class time_monster():
    def __init__(self, name, reward, hp):
        self.name=name
        self.reward=reward
        self.hp=hp
    def return_reward(self, title):
        return self.reward[title]

def get_input(play):
    tmp=int(input())
    return (tmp, player_list[play])

def run_game(num, round_num, task_list):
    for i in range(round_num):
        tmp=random.randint(8)
        time_now=task_list[tmp]
        task_list.pop(tmp)
        input_list={}
        for i in range(num):
            while True:
                tmp=get_input(i)
                input_list[tmp[1]]=tmp[0]
        input_list_new = copy.deepcopy(input_list)
        check_list=list(input_list.values())
        same_list=[]
        for i in range(num):
            for j in range(num):
                if check_list[i]==check_list[j] and i!=j:
                    same_list.append(check_list[i])
        tot=0
        for i in range(num):
            tot=tot+input_list[i]
        if time_now.hp<=tot:
            print("Success")

        else:
            print("Failed")




num_player=int(input())
nick_player=input().split(' ')
player_list=[]
reward_list=[[[], [], []], [[], [], []]]
task_name1=['KYPT', '세종수학축전', '한화사이언스챌린지', '해커톤', '동아리 발표 대회']
task_name2=['융합@수학 산출물', 'SA', '객체지향프로그래밍 프로젝트', '도시환경과 도시계획 연구', '논리적 글쓰기 인문학보고서']
task_name3=['의자 만들기', '스파게티 다리 만들기', '교류 발전기 만들기', '논문 분석', '창작 시 콘서트']
task_name_all=[task_name1, task_name2, task_name3]
task_header=['외부활동', '연구활동', '조별과제']
task_list={}
time_name={1:'공강시간1', 2:'1차자습시간', 3:'공강시간2', 4:'1, 2차 자습시간', 5:'공강시간3', 6:'평일자습시간', 7:'주말자습시간', 8:'밤샘시간'}
hp_list=[8, 11, 14, 17, 20]
for i in range(3):
    tmp=[]
    for j in range(5):
        key = random.randint(5)
        tmp.append(time_monster(task_name_all[i][j], reward_list[(key+j)%5], int(hp_list[(key+j)%5]*num_player/5)))
    task_list[task_header[i]]=tmp
for i in range(num_player):
    player_list.append(player(nick_player[i]))
global player_list, time_name
stage_num=3
round_num=5
for i in range(stage_num):
    task_tmp=copy.deepcopy(task_list)
    run_game(num_player, round_num, task_tmp[task_header[i]])


