import sys
from PyQt5


class chatroom():
    def __init__(self, nickname):
        self.nickname=nickname

    def out(self,somestring):
        view(somestring)

class my_status():
    def __init__(self, stone1, stone2, stone3):
        self.stone1=stone1
        self.stone2=stone2
        self.stone3=stone3
        tot_block(self)

    def change_block(self, stone1=0, stone2=0, stone3=0):
        self.stone1-=stone1
        self.stone2-=stone2
        self.stone3-=stone3

    def tot_block(self):
        self.tot=(self.stone1+self.stone2+self.stone3)
        show_block()

class who_let_the_stones_out():
    def __init__(self, somelist):
        self.somelist=somelist
        view_stones(somelist)

class monster():
    def __init__(self, name):
        self.name=name
        view_image(self)
        view_status(self)

    def view_image(self):
        pass

    def view_status(self):
        pass

if __name__ == '__main__':
    pass