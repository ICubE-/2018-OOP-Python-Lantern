# -*- coding: utf-8 -*-
# -pip3 install pygame
# -pip3 install heconvert
import sys
import pygame
from pygame.locals import *
import pygame_textinput

pygame.init()

#색정의
BLACK=(15,46,71)
RED=(255, 33, 5)
GREEN=(68, 255, 91)
BLUE=[(27,77,131), (0, 68, 102), (1, 102, 153), (91, 183, 212)]
WHITE=(228,229,230)
GRAY=(217,230,248)
MINT=(38,160,231)

#기본값 정의
names={'KYPT' : ['대회 활동', 20],
       '세종수학축전' : ['대회 활동', 20],
       '한화사이언스챌린지' : ['대회 활동', 20],
       '세종 해커톤' : ['대회 활동', 20],
       '동아리 발표 대회' : ['대회 활동', 20],
       '융합@수학 산출물' : ['연구 활동', 20],
       '삼성휴먼테크논문쓰기' : ['연구 활동', 20],
       '객지프로젝트' : ['연구 활동', 20],
       '도시환경과 도시계획 연구' : ['연구 활동', 20],
       '논리적글쓰기 인문학 보고서' : ['연구 활동', 20],
       '공학개론 의자 만들기' : ['조별 과제', 20],
       '사회문제와인문학적상상력 발표' : ['조별 과제', 20],
       '고급물리 교류발전기 만들기' : ['조별 과제', 20],
       '공학개론 다리 만들기' : ['조별 과제', 20],
       '창작 시 콘서트' : ['조별 과제', 20]
       }
win_width=1340
win_height=660
ratio_title=1/12
ratio_chatroom=3/4
ratio_monster=8/12
ratio_status=5/6
bgcolor=WHITE
round_name=''
chat_num=(win_height*(1-ratio_monster)-60)//17-1
chatting_t=[]
screen = pygame.display.set_mode((win_width, win_height))
flag=True
y=0.0


def settings(Win_Width=win_width, Win_Height=win_height, Ratio_Chatroom=ratio_chatroom, Ratio_Monster=ratio_monster, Ratio_Status=ratio_status, Ratio_Title=ratio_title, BgColor=bgcolor, Chat_Num=chat_num):
    global win_width, win_height, ratio_title, ratio_chatroom, ratio_monster, ratio_status, bgcolor, screen, chat_num
    win_width=Win_Width
    win_height=Win_Height
    ratio_chatroom=Ratio_Chatroom
    ratio_monster=Ratio_Monster
    ratio_status=Ratio_Status
    ratio_title=Ratio_Title
    bgcolor=BgColor
    chat_num=(win_height*(1-ratio_monster)-60)//17-1
    screen = pygame.display.set_mode((win_width, win_height))
    pass


class stage():

    def __init__(self, rd_name):
        global round_name, names
        pygame.display.set_caption('상!평!')
        try:
            self.stage_name=names[rd_name][0]
        except:
            print('배열안의 이름이랑 넣은 이름이랑 안맞는듯')
        round_name=rd_name

    def refill(self):
        screen.fill(WHITE)
        self.base_display()
        self.Stage_Title()

    def base_display(self):
        #base_display
        pygame.draw.line(screen, BLACK, (0, 0), (win_width,0), 4)#전체 윤곽
        pygame.draw.line(screen, BLACK, (0, 0), (0,win_height), 4)#전체 윤곽
        pygame.draw.line(screen, BLACK, (win_width-2, 0), (win_width-2, win_height), 4)#전체 윤곽
        pygame.draw.line(screen, BLACK, (0, win_height-2), (win_width, win_height-2), 4)#전체 윤곽

        pygame.draw.line(screen, BLUE[2], (3,win_height*ratio_title), (win_width*ratio_chatroom, win_height*ratio_title), 4)
        pygame.draw.line(screen, BLUE[2], (win_width*ratio_chatroom, 3), (win_width*ratio_chatroom, win_height-4), 4)#채팅창 구분
        pygame.draw.line(screen, BLUE[2], (3, win_height*ratio_monster), (win_width*ratio_chatroom, win_height*ratio_monster), 4)#몬스터 구분
        
        pygame.draw.line(screen, BLUE[2], (win_width*ratio_chatroom, win_height/2), (win_width-4, win_height/2), 4)#상태창 구분

        pygame.draw.rect(screen, GRAY, (25, win_height-34, win_width*ratio_chatroom-50, 22))#입력창
        pygame.draw.rect(screen, MINT, (25, win_height-34, win_width*ratio_chatroom-50, 22), 1)#입력창
        pygame.draw.rect(screen, GRAY, (25, win_height*ratio_monster+15, win_width*ratio_chatroom-50, win_height*(1-ratio_monster)-60), 1)#채팅창
        pygame.draw.rect(screen, MINT, (25, win_height*ratio_monster+15, win_width*ratio_chatroom-50, win_height*(1-ratio_monster)-60), 1)#채팅창
        
        #stageTitle
    def Stage_Title(self):
        try:
            pygame.draw.rect(screen, BLUE[1], (0, 0, win_width*ratio_chatroom, win_height*ratio_title))
            stage_title_fontObj = pygame.font.Font('font\\NanumSquareRoundEB.ttf', 40)
            text_stage = stage_title_fontObj.render('STAGE : '+self.stage_name, True, WHITE)
            text_stage_rectObj = text_stage.get_rect()
            text_stage_rectObj.center = (win_width*ratio_chatroom/2, win_height*ratio_title/2+2)
            screen.blit(text_stage, text_stage_rectObj)
        
        except:
            print('No File!!')
            raise
        return

def chatting_input(sometext=''):
    global chatting_t, chat_num
    if sometext:
        #print(sometext)
        if len(chatting_t)<=chat_num:
            chatting_t.append(sometext)
        else:
            chatting_t=chatting_t[1:]
            chatting_t.append(sometext)

        #print(chatting_t)

    t=0
    for c in chatting_t:
        chat_fontobj = pygame.font.Font('font\\NanumGothic.ttf', 15)
        chat = chat_fontobj.render(c, True, BLACK)
        chat_rectObj = chat.get_rect()
        chat_rectObj.center = (25+chat.get_width()/2, win_height*ratio_monster+15+chat.get_height()/2+t)
        screen.blit(chat, chat_rectObj)
        t+=17

    pass


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
        self.num=len(somelist)
        self.somelist=somelist
        self.view_stones()

    def view_stones(self):
        vx=[]
        vy=[]
        for i in range(5): vx.append(self.tx(i+1))
        for i in range((len(self.somelist)-1)//5+1): vy.append(self.ty(i))
        for i in range(len(self.somelist)):
            if self.somelist[i]:
                pygame.draw.circle(screen, GREEN, (vx[i%5], vy[i//5]), 15)
            else:
                pygame.draw.circle(screen, RED, (vx[i%5], vy[i//5]), 15)

    def tx(self, x):
        return int(win_width*(ratio_chatroom+(1-ratio_chatroom)*x/6))

    def ty(self, y):
        return int(win_height*(1/6+y/12))

class monster():
    def __init__(self, round):
        global round_name
        self.round=round
        self.bgm()
        try:
            
            self.Img = pygame.image.load('images\\{}.png'.format(self.round))
            self.x=win_width*ratio_chatroom/2-self.Img.get_rect().size[0]/2
            self.y=(win_height*(ratio_monster)-self.Img.get_rect().size[1])/2
            
        except:
            print('No file!!')

    def refill(self):
        self.view_image()
        self.view_status()

    def view_image(self):
        global flag, y
        if y>=10:
            flag=False
        elif y<=-10 :
            flag=True
        screen.blit(self.Img, (self.x, self.y+y))
        if flag:
            y+=0.1
        else:
            y-=0.1
        pass

    def bgm(self):
        try:
            print(self.round)
            pygame.mixer.music.load("music\\bgm\\{}.mp3".format(self.round)) 
            pygame.mixer.music.play(-1,0.0)
        except:
            print("No file!!")
            pass

    def view_status(self):
        global round_name
        #라운드 이름
        name_fontobj = pygame.font.Font('font\\NanumBarunGothicWeb.ttf', 25)
        name = name_fontobj.render(round_name, True, BLACK)
        name_rectObj = name.get_rect()
        name_rectObj.center = (win_width*ratio_chatroom/2, win_height*ratio_monster-15-name.get_height()/2)
        screen.blit(name, name_rectObj)

        #HP
        pygame.draw.rect(screen, BLACK, (win_width*ratio_chatroom/2-10*names[round_name][1]/2,win_height*ratio_monster-65-name.get_height()/2,10*names[round_name][1], 32), 1)
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

def running():
    run=True
    textinput = pygame_textinput.TextInput()
    tempstatus=[1,1,0,0,0,0,1,0,1,0,1,1,1,1,1,1]
    test=stage('객지프로젝트')
    mon=monster(round_name)
    while run:
        pygame.time.delay(10)
        
        events=pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False
                break
            
        test.refill()
        mon.refill()

        who_let_the_stones_out(tempstatus)
        y=textinput.update(events)
        # Blit its surface onto the screen
        screen.blit(textinput.get_surface(), (30, win_height-32))
        try:
            if y[0]=='$':
                system(y)
            else:
                chatting_input(y)
        except:
            chatting_input(y)
        pygame.display.update()
        pass
    pygame.quit()

if __name__ == '__main__':
    running()


'''
해야할 일
//1. inputbox 한/영전환(수정완료)
2. chating room 내용 표시(수정완료)
3. mystats, monster, 팀원 상태
4. round별 bgm
5. 메뉴 방
6. fail, success방
7. stage끝나면 결과창
8. 대기방
9. 한글 방향키 설정 (수정불가)



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