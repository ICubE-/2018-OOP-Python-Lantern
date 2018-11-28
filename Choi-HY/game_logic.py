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
            print("Choose From What You Have")
            return False
        else:
            self.card_list.sort()
            return True

    def get_reward(self, time, amount):
        ind=0
        for i in amount:
            self.reward_dict[reward_name[ind]]=self.reward_dict[reward_name[ind]]+i
            ind=ind+1

    def take_time(self):
        waste=max(self.reward_dict.items(), key=lambda x:x[1])[0]
        self.reward_dict[waste]=0

    def init_time(self):
        self.card_list=list(range(1,8))

class time_monster():
    def __init__(self, name, reward, hp):
        self.name=name
        self.reward=reward
        self.hp=hp

    def return_reward(self, rank):
        return self.reward[rank]

def get_input(play):
    global player_list
    tmp=int(input())
    return (tmp, player_list[play])

def run_game(num, round_num, task_list):
    for i in range(round_num):
        tmp=random.randint(8)
        time_now=task_list[tmp]
        task_list.pop(tmp)

        input_list=[]

        for i in range(num):
            while True:
                tmp=get_input(i)
                if tmp[1].put_card(tmp[0]):
                    input_list.append(tmp)
                    break

        input_list_new = copy.deepcopy(input_list)

        for i in range(num):
            for j in range(num):
                if input_list[i][0]==input_list[j][0] and i!=j:
                    try:
                        input_list_new.remove(input_list[i])
                    except ValueError:
                        print("Error")

        tot=0
        for i in range(num):
            tot=tot+input_list_new[i][0]

        if time_now.hp<=tot:
            print("Success")

        else:
            print("Failed")

def play_again():
    return input('Press Y to restart').lower().startswith('y')


num_player=int(input())
nick_player=input().split(' ')
player_list=[]

task_name1=['KYPT', '세종수학축전', '한화사이언스챌린지', '해커톤', '동아리 발표 대회']
task_name2=['융합@수학 산출물', 'SA', '객체지향프로그래밍 프로젝트', '도시환경과 도시계획 연구', '논리적 글쓰기 인문학보고서']
task_name3=['의자 만들기', '스파게티 다리 만들기', '교류 발전기 만들기', '논문 분석', '창작 시 콘서트']
task_name_all=[task_name1, task_name2, task_name3]
task_header=['외부활동', '연구활동', '조별과제']
task_list={}

reward_list=[[[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []]]
time_name={1:'공강시간1', 2:'1차자습시간', 3:'공강시간2', 4:'1, 2차 자습시간', 5:'공강시간3', 6:'평일자습시간', 7:'주말자습시간', 8:'밤샘시간'}
reward_name=['자유로운 공강', '행복한 취미생활', '편안한 숙면']
hp_list=[8, 11, 14, 17, 20]

for i in range(3):
    tmp=[]
    for j in range(5):
        key = random.randint(5)
        tmp.append(time_monster(task_name_all[i][j], reward_list[(key+j)%5], int(hp_list[(key+j)%5]*num_player/5)))
    task_list[task_header[i]]=tmp


for i in range(num_player):
    player_list.append(player(nick_player[i]))

stage_num=3
round_num=5

while True:
    for i in range(stage_num):
        task_tmp=copy.deepcopy(task_list)
        run_game(num_player, round_num, task_tmp[task_header[i]])

    if play_again():
        continue
    else:
        break



