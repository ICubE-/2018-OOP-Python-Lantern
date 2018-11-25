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

num_player=int(input())
nick_player=input().split(' ')
player_list=[]
for i in num_player:
    player_list.append(player(nick_player[i]))



