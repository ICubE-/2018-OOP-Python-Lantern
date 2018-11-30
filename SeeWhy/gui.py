# -*- coding: utf-8 -*-
# -pip3 install pygame
# -pip3 install heconvert
import sys
import pygame
from pygame.locals import *
import pygame_textinput

pygame.init()

#색정의
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(51,51,255)
WHITE=(255,255,255)

#기본값 정의
win_width=1040
win_height=560
ratio_title=1/12
ratio_chatroom=3/4
ratio_monster=8/12
ratio_status=5/6
bgcolor=WHITE
screen = pygame.display.set_mode((win_width, win_height))

def settings(Win_Width=win_width, Win_Height=win_height, Ratio_Chatroom=ratio_chatroom, Ratio_Monster=ratio_monster, Ratio_Status=ratio_status, Ratio_Title=ratio_title, BgColor=bgcolor):
    global win_width, win_height, ratio_title, ratio_chatroom, ratio_monster, ratio_status, bgcolor, screen
    Win_Width=win_width
    Win_Height=win_height
    Ratio_Chatroom=ratio_chatroom
    ratio_monster=Ratio_Monster
    ratio_status=Ratio_Status
    ratio_title=Ratio_Title
    bgcolor=BgColor
    screen = pygame.display.set_mode((win_width, win_height))
    pass


class stage():
    global win_width, win_height, ratio_title, ratio_chatroom, ratio_monster, ratio_status, bgcolor, screen

    def __init__(self, stage_name, round_name):
        pygame.display.set_caption('상!평!')
        self.stage_name=stage_name
        self.round_name=round_name

        clock = pygame.time.Clock()
        screen.fill(WHITE)
        self.base_display()
        self.Stage_Title()


    def base_display(self):
        #base_display
        pygame.draw.line(screen, BLACK, (0, 0), (win_width,0), 4)#전체 윤곽
        pygame.draw.line(screen, BLACK, (0, 0), (0,win_height), 4)#전체 윤곽
        pygame.draw.line(screen, BLACK, (win_width-2, 0), (win_width-2, win_height), 4)#전체 윤곽
        pygame.draw.line(screen, BLACK, (0, win_height-2), (win_width, win_height-2), 4)#전체 윤곽

        pygame.draw.line(screen, BLUE, (0,win_height*ratio_title), (win_width*ratio_chatroom, win_height*ratio_title), 4)
        pygame.draw.line(screen, BLUE, (win_width*ratio_chatroom, 0), (win_width*ratio_chatroom, win_height), 4)#채팅창 구분
        pygame.draw.line(screen, BLUE, (0, win_height*ratio_monster), (win_width*ratio_chatroom, win_height*ratio_monster), 4)#몬스터 구분
        
        pygame.draw.line(screen, BLUE, (win_width*ratio_chatroom, win_height/2), (win_width, win_height/2), 4)#상태창 구분
        
        #stageTitle
    def Stage_Title(self):
        try:
            stage_title_fontObj = pygame.font.Font('font\\NanumSquareRoundEB.ttf', 40)
            text_stage = stage_title_fontObj.render('STAGE : '+self.stage_name, True, BLACK)
            text_stage_rectObj = text_stage.get_rect()
            text_stage_rectObj.center = (win_width*ratio_chatroom/2, win_height*ratio_title/2+2)
            screen.blit(text_stage, text_stage_rectObj)
        
        except:
            print('No File!')
        return


class chatroom():
    def __init__(self, nickname, chat_width=260, chat_height=140):
        self.nickname=nickname
        self.chat_width=chat_width
        self.chat_height=chat_height

    def text_input(self):
        pass

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

    '''
class InputBox:
    #https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame 에서 약간 변형

    def __init__(self, x, y, w, h, text=''):
        self.FONT=pygame.font.Font('font\\NanumGothic.ttf', 20)
        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    t=self.text
                    print(t)
                    self.text = ''
                    return t
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
        '''

if __name__ == '__main__':
    run=True
    textinput = pygame_textinput.TextInput(max_text=10)
    while run:
        pygame.time.delay(100)
        
        events=pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False
                break
            
        test=stage('조별과제', '객지프로젝트')
        textinput.update(events)
        # Blit its surface onto the screen
        screen.blit(textinput.get_surface(), (100, 500))
        pygame.display.update()
        pass
    pygame.quit()



'''
해야할 일
//1. inputbox 한/영전환
2. chating room 내용 표시
3. mystats, monster, 팀원 상태
4. round별 bgm
5. 메뉴 방
6. fail, success방
7. stage끝나면 결과창
8. 대기방
9. 한글 방향키 설정



import pygame_textinput
import pygame
pygame.init()

# Create TextInput-object
textinput = pygame_textinput.TextInput()

screen = pygame.display.set_mode((1000, 200))
clock = pygame.time.Clock()

while True:
    screen.fill((225, 225, 225))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    # Feed it with events every frame
    textinput.update(events)
    # Blit its surface onto the screen
    screen.blit(textinput.get_surface(), (100, 10))

    pygame.display.update()
    clock.tick(30)
    '''