import random

class player():
    def __init__(self, nickname):
        self.nickname=nickname
        self.card_list=list(range(1,8))
        self.time_dict={'공강':1, '자습시간':1, '취침시간':1}
    def put_card(self, card_num):
        try:
            self.card_list.remove(card_num)
        except ValueError:
            print("Choose From What You Have")
    def get_time(self, time, amount):
        self.time_dict[time]=self.time_dict[time]+amount
    def take_time(self):
        waste=max(self.time_dict.items(), key=lambda x:x[1])[0]
        waste_time=max(self.time_dict.items(), key=lambda x:x[1])[1]
        self.time_dict[waste]=0
        return waste_time


def get_input(play):
    tmp=int(input())
    return (tmp, player_list[play])

def run_game(num, tot_time):
    input_list={}
    for i in range(num):
        while True:
            tmp=get_input(i)
            if tmp[0] in player_list[i].card_list:
                input_list[tmp[0]]=tmp[1]
                break
            else:
                continue
    for i in range(num):
        for j in range(num):
            if input_list[i]==input_list[j] and i!=j:
                input_list[i]=input_list[j]=0
    tot=0
    for i in range(num):
        tot=tot+input_list[i]
    if tot_time<=tot:
        print("Success")



num_player=int(input())
nick_player=input().split(' ')
player_list=[]
time_list=[]
for i in range(num_player):
    player_list.append(player(nick_player[i]))
global player_list
while True:
    tmp=random.randint(8)

    run_game(num_player)

