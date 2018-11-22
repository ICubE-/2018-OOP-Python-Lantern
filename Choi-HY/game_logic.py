import operator

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
        self.time_dict=dict(sorted(self.time_dict.items(), key=operator.itemgetter(1), reverse=True))