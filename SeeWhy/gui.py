# -*- coding: utf-8 -*-
import sys
import pygame
from pygame.locals import *

pygame.init()

#색정의
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(51,51,255)
WHITE=(255,255,255)


class stage():
    def __init__(self, stage_name, win_width=1040, win_height=560):
        pygame.display.set_caption('상!평!')
        self.stage_name='THE BOSS : '+stage_name
        self.win_width = win_width
        self.win_height = win_height

        self.screen = pygame.display.set_mode((self.win_width, self.win_height))
        clock = pygame.time.Clock()
        self.screen.fill(WHITE)
        self.base_display()


    def base_display(self, ratio_title=1/12, ratio_chatroom=3/4, ratio_monster=7/12, ratio_status=5/6):
        #pygame.draw.rect(self.screen, BLACK, (0, 0, self.win_width, self.win_height), 4)#전체 윤곽
        pygame.draw.line(self.screen, BLACK, (0, 0), (self.win_width,0), 4)#전체 윤곽
        pygame.draw.line(self.screen, BLACK, (0, 0), (0,self.win_height), 4)#전체 윤곽
        pygame.draw.line(self.screen, BLACK, (self.win_width-2, 0), (self.win_width-2, self.win_height), 4)#전체 윤곽
        pygame.draw.line(self.screen, BLACK, (0, self.win_height-2), (self.win_width, self.win_height-2), 4)#전체 윤곽

        pygame.draw.line(self.screen, BLUE, (0,self.win_height*ratio_title), (self.win_width*ratio_chatroom, self.win_height*ratio_title), 4)
        pygame.draw.line(self.screen, BLUE, (self.win_width*ratio_chatroom, 0), (self.win_width*ratio_chatroom, self.win_height), 4)#채팅창 구분
        pygame.draw.line(self.screen, BLUE, (0, self.win_height*ratio_monster), (self.win_width*ratio_chatroom, self.win_height*ratio_monster), 4)#몬스터 구분
        pygame.draw.line(self.screen, BLUE, (0, self.win_height*ratio_status), (self.win_width*ratio_chatroom, self.win_height*ratio_status), 4)#상태창 구분
        
        #stageTitle
        try:
            stage_title_fontObj = pygame.font.Font('font\\NanumSquareRoundEB.ttf', 40)
            text_stage = stage_title_fontObj.render(self.stage_name, True, BLACK)
            text_stage_rectObj = text_stage.get_rect()
            text_stage_rectObj.center = (self.win_width*ratio_chatroom/2,self.win_height*ratio_title/2+2)
            self.screen.blit(text_stage, text_stage_rectObj)
        
        except:
            print('No File!')
            return


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
        self.tot_block()

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
        self.view_image()
        self.view_status()

    def view_image(self):
        pass

    def view_status(self):
        pass

if __name__ == '__main__':
    run=True
    while run:
        pygame.time.delay(100)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        test=stage('객지프로젝트')
        pygame.display.update()
        pass
    pygame.quit()