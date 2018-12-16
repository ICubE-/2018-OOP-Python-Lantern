# -*- coding: utf-8 -*-
# -pip3 install pygame
# -pip3 install heconvert
import sys
import pygame
from pygame.locals import *
import pygame_textinput
from time import *

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
names={'KYPT' : ['대회 활동', 30],
       '세종수학축전' : ['대회 활동', 20],
       '한화사이언스챌린지' : ['대회 활동', 25],
       '세종 해커톤' : ['대회 활동', 20],
       '동아리 발표 대회' : ['대회 활동', 20],
       '융합@수학 산출물' : ['연구 활동', 50],
       '삼성휴먼테크논문쓰기' : ['연구 활동', 40],
       '객지프로젝트' : ['연구 활동', 80],
       '도시환경과 도시계획연구' : ['연구 활동', 20],
       '논리적글쓰기 인문학 보고서' : ['연구 활동', 20],
       '공학개론 의자 만들기' : ['조별 과제', 10],
       '사회문제와인문학적상상력 발표' : ['조별 과제', 10],
       '고급물리 교류발전기 만들기' : ['조별 과제', 20],
       '공학개론 다리 만들기' : ['조별 과제', 10],
       '창작 시 콘서트' : ['조별 과제', 20]
       }
tempstatus=[1,1,0,0,0,0,1,0,1,0,1,1,1,1,1,1]


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
resultflag=True
y=0.0
damage=0
resulting=[0,0,0,0,20,0,0,0,0,-20,-20,0,0,0,0,20,20,0,0,0,0,-20,-20,0,0,0,0,20,18,0,0,0,0,-18,-18,0,0,0,0,18,18,0,0,0,0,-18,-15,0,0,0,0,15,15,0,0,0,0,-15,-10,0,0,0,0,10,5,0,0,0,0,-5,-5,0,0,0,0,5]


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

    #credit
    print(
        '''
        "Unity" Kevin MacLeod (incompetech.com)
        Licensed under Creative Commons: By Attribution 3.0 License
        http://creativecommons.org/licenses/by/3.0/
        "Welcome to HorrorLand" Kevin MacLeod (incompetech.com)
        Licensed under Creative Commons: By Attribution 3.0 License
        http://creativecommons.org/licenses/by/3.0/
        '''
        )
    pass


class stage():

    def __init__(self):
        global round_name, names
        pygame.display.set_caption('상!평!')
        try:
            self.stage_name=names[round_name][0]
        except:
            print('배열안의 이름이랑 넣은 이름이랑 안맞는듯')

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
            text_stage = stage_title_fontObj.render('STAGE : '+self.stage_name, True, (255,255,255))
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
    def __init__(self, stonedic, cardlist):
        self.stonedic = list(stonedic.values())
        self.cardlist = cardlist
        self.stone1=pygame.image.load('images\\{}.png'.format('자유로운 공강'))
        self.stone2=pygame.image.load('images\\{}.png'.format('행복한 취미생활'))
        self.stone3=pygame.image.load('images\\{}.png'.format('편안한 숙면'))
        self.vx=[]
        self.vy=[]
        self.card=[]
        self.someflag=True
        self.somesum=0
        for i in range(4): self.vx.append(self.tx(i+1))
        for i in range(2): self.vy.append(self.ty(i))
        for i in range(8): self.card.append(pygame.image.load('images\\{}.png'.format(i+1)))

        self.show_block()

    def tx(self, x):
        return int(win_width*(ratio_chatroom+(1-ratio_chatroom)*x/5))

    def ty(self, y):
        return int(win_height*(19/24+y/12))

    def show_block(self):
        screen.blit(self.stone1, (self.vx[0]-26, win_height*(13/24)-10))
        screen.blit(self.stone2, (self.vx[0]-26, win_height*(13/24+1/12)-10))
        screen.blit(self.stone3, (self.vx[0]-26, win_height*(13/24+1/6)-10))
        
        for i in range(len(self.stonedic)):
            stone_fontobj = pygame.font.Font('font\\NanumGothic-ExtraBold.ttf', 40)
            stone = stone_fontobj.render('{}'.format(self.stonedic[i]), True, BLACK)
            stone_rectObj = stone.get_rect()
            stone_rectObj.center = (self.vx[0]+self.stone1.get_rect().size[0]+10, stone.get_rect().size[1]/2+win_height*(13/24+i/12)-10)
            screen.blit(stone, stone_rectObj)
        
        self.C=[]
        for i in range(8):
            if self.cardlist[i]:
                screen.blit(self.card[i], (self.vx[i%4]-self.card[i].get_rect().size[0]/2, self.vy[i//4]))
                self.C.append(pygame.Rect((self.vx[i%4]-self.card[i].get_rect().size[0]/2, self.vy[i//4]),(self.card[i].get_rect().size[0], self.card[i].get_rect().size[1])))
        return

class who_let_the_stones_out():
    def __init__(self, somelist):
        self.num=len(somelist)
        self.somelist=somelist
        self.view_stones()

    def view_stones(self):
        global resultflag, damage
        vx=[]
        vy=[]
        self.someflag=True
        self.somesum=0
        for i in range(5): vx.append(self.tx(i+1))
        for i in range((self.num-1)//5+1): vy.append(self.ty(i))
        for i in range(self.num):
            if self.somelist[i]:
                s=pygame.image.load('images\\{}.png'.format('green'))
                screen.blit(s, (vx[i%5]-20, vy[i//5]-30))
                self.somesum+=self.somelist[i]
            else:
                s=pygame.image.load('images\\{}.png'.format('red'))
                screen.blit(s, (vx[i%5]-20, vy[i//5]-30))
                self.someflag=False
        if self.someflag:
            resultflag=False
            damage = self.somesum

    def tx(self, x):
        return int(win_width*(ratio_chatroom+(1-ratio_chatroom)*x/6))

    def ty(self, y):
        return int(win_height*(1/6+y/12))

class monster():
    def __init__(self):
        global round_name
        self.bgm()
        self.tempflag=True
        self.cnt=0
        try:
            self.Img = pygame.image.load('images\\{}.png'.format(round_name))
            self.x = win_width*ratio_chatroom/2-self.Img.get_rect().size[0]/2
            self.y = (win_height*(ratio_monster)-self.Img.get_rect().size[1])/2
            
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

    def view_result(self):
        global resulting, damage
        if self.cnt<len(resulting):
            if self.tempflag:
                self.tempflag=False
                try:
                    pygame.mixer.music.load("music\\soundeffect\\{}.mp3".format('punch')) 
                    pygame.mixer.music.play(0)
                    sleep(0.2)
                except:
                    print("No soundeffect file!!")
                    pass

            self.x+=resulting[self.cnt]
            screen.blit(self.Img, (self.x, self.y))
            dg_fontobj = pygame.font.Font('font\\NanumGothic-ExtraBold.ttf', 60)
            dg = dg_fontobj.render('{}'.format(damage), True, RED)
            dg_rectObj = dg.get_rect()
            dg_rectObj.center = (self.x+self.Img.get_rect().size[0]/2, self.y)
            screen.blit(dg, dg_rectObj)
            self.cnt+=1
            
            #HP
            currentHP=max(names[round_name][1]-damage, 0)
            pygame.draw.rect(screen, BLACK, (win_width*ratio_chatroom/2-10*names[round_name][1]/2,win_height*ratio_monster-65-self.name.get_height()/2,10*names[round_name][1], 32), 1)
            pygame.draw.rect(screen, GREEN, (win_width*ratio_chatroom/2-10*names[round_name][1]/2+1,win_height*ratio_monster-65-self.name.get_height()/2+1,int(max(min(currentHP / float(names[round_name][1]) * (10*names[round_name][1]-2), 10*names[round_name][1]-2), 0)), 30), 0)
            HP_fontobj = pygame.font.Font('font\\NanumBarunGothicWeb.ttf', 20)
            HP = HP_fontobj.render('{}/{}'.format(currentHP, names[round_name][1]), True, BLACK)
            HP_rectObj = HP.get_rect()
            HP_rectObj.center = (win_width*ratio_chatroom/2, win_height*ratio_monster-52-HP.get_height()/2)
            screen.blit(HP, HP_rectObj)
            
            if self.cnt==len(resulting):
                pygame.mixer.music.load("music\\bgm\\{}.mp3".format('result')) 
                pygame.mixer.music.play(-1)
                self.rs=result(currentHP)

        else:
            if names[round_name][1] > damage:
                screen.blit(self.Img, (self.x, self.y))
            self.rs.refill()
            pass

    def bgm(self):
        global round_name
        try:
            pygame.mixer.music.load("music\\bgm\\{}.mp3".format(round_name)) 
            pygame.mixer.music.play(-1,0.0)
        except:
            print("No file!!")
            pass

    def view_status(self):
        global round_name
        #라운드 이름
        name_fontobj = pygame.font.Font('font\\NanumBarunGothicWeb.ttf', 25)
        self.name = name_fontobj.render(round_name, True, BLACK)
        name_rectObj = self.name.get_rect()
        name_rectObj.center = (win_width*ratio_chatroom/2, win_height*ratio_monster-15-self.name.get_height()/2)
        screen.blit(self.name, name_rectObj)

        #HP
        currentHP=names[round_name][1]
        pygame.draw.rect(screen, BLACK, (win_width*ratio_chatroom/2-10*names[round_name][1]/2,win_height*ratio_monster-65-self.name.get_height()/2,10*names[round_name][1], 32), 1)
        pygame.draw.rect(screen, GREEN, (win_width*ratio_chatroom/2-10*names[round_name][1]/2+1,win_height*ratio_monster-65-self.name.get_height()/2+1,int(max(min(currentHP / float(names[round_name][1]) * (10*names[round_name][1]-2), 10*names[round_name][1]-2), 0)), 30), 0)
        HP_fontobj = pygame.font.Font('font\\NanumBarunGothicWeb.ttf', 20)
        HP = HP_fontobj.render('{}/{}'.format(currentHP, names[round_name][1]), True, BLACK)
        HP_rectObj = HP.get_rect()
        HP_rectObj.center = (win_width*ratio_chatroom/2, win_height*ratio_monster-52-HP.get_height()/2)
        screen.blit(HP, HP_rectObj)
        pass

class result():
    def __init__(self, hp):
        self.hp=hp

    def refill(self):
        if self.hp:
            self.Fail()
        else:
            self.Success()

    def Success(self):
        sc_fontobj = pygame.font.Font('font\\NanumGothic-ExtraBold.ttf', int(win_height/4))
        sc = sc_fontobj.render('SUCCESS', True, BLUE[1])
        sc_rectObj = sc.get_rect()
        sc_rectObj.center = (win_width*ratio_chatroom/2, win_height*ratio_monster/2)
        screen.blit(sc, sc_rectObj)

    def Fail(self):
        fail_fontobj = pygame.font.Font('font\\NanumGothic-ExtraBold.ttf', int(win_height/4))
        fail = fail_fontobj.render('FAIL', True, BLUE[1])
        fail_rectObj = fail.get_rect()
        fail_rectObj.center = (win_width*ratio_chatroom/2, win_height*ratio_monster/2)
        screen.blit(fail, fail_rectObj)

    #damage=0

    pass

class running():
    def __init__(self):
        self.run=True
        self.textinput = pygame_textinput.TextInput()
        self.system('$input')
        self.activate()

    def system(self, instructions):
        global round_name, tempstatus, resultflag
        if instructions=='$input':
            while True:
                try:
                    round_name=input()
                    names[round_name]

                    #초기화
                    self.mon=monster()
                    self.test=stage()
                    resultflag=True
                    tempstatus=[0,0,0,1,0,1,0]
                    break
                except:
                    print('라운드 이름이 정확하지 않음')
                    continue
        if instructions=='$stone':
            tempstatus=[4,2,2,6,4,3,5]
        return

    def activate(self):
        global round_name, tempstatus
        while self.run:
            pygame.time.delay(10)
        
            events=pygame.event.get()

            self.test.refill()
        

            if resultflag:
                self.st = my_status({'자유로운 공강': 1, '행복한 취미생활': 1, '편안한 숙면': 1}, [1,1,1,1,1,1,1,1])
                who_let_the_stones_out(tempstatus)
                self.mon.refill()
            else:
                self.mon.view_result()

            y=self.textinput.update(events)
            # Blit its surface onto the screen
            screen.blit(self.textinput.get_surface(), (30, win_height-32))
            try:
                if y[0]=='$':
                    self.system(y)
                else:
                    chatting_input(y)
            except:
                chatting_input(y)
                
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    break
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        for i in range(8):
                            if self.st.C[i].collidepoint(event.pos[0], event.pos[1]):
                                buttonpushed=i
                                print(i)
            
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