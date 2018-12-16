from gui_game import *

#넣어줘야 할 값
RoundName='KYPT'
DAMAGE=24

#기초 선언
base=stage(RoundName)#배경 만듦

#몬스터 선언
mon=monster(RoundName, 20)

#채팅방 선언
textinput = pygame_textinput.TextInput()

#일반적일때
while True:
    #기본
    pygame.display.init()
    pygame.time.delay(10)
    events = pygame.event.get()

    base.refill()#계속 배경보이기
    mon.refill()#계속 몬스터 보이기

    texts = textinput.update(events)#화면에 입력된 것들을 문자열로 받음
    screen.blit(textinput.get_surface(), (30, win_height - 32))#받은것들을 입력창에 띄움

    chatting_input(texts)#받은 TEXT들을 모두 채팅방에 띄운다

    stat=my_status({'자유로운 공강': 5, '행복한 취미생활': 2, '편안한 숙면': 1}, [1, 1, 1, 1, 1, 1, 1, 1])#보석들과 공격카드 정보를 받으면 화면에 표시
    
    who_let_the_stones_out([0,1,0,1,0,1,0,1,0,1,0,1,1])#플레이어 공격력들의 리스트가 들어갔을 때 빨강초록 표시
    
    for event in events:
        if event.type == pygame.QUIT:
            self.run = False
            break
        elif event.type == pygame.MOUSEBUTTONUP:
            #버튼 누르는것 ( stat선언보다 뒤에 있어야 버튼 눌림)
            if event.button == 1:
                for i in range(8):
                    if stat.C[i].collidepoint(event.pos[0], event.pos[1]):
                        print(i+1)#button pushed

    pygame.display.update()


#DAMAGE가 있을때
while False:
    #기본
    pygame.display.init()
    pygame.time.delay(10)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            self.run = False
            break

    base.refill()#계속 배경보이기
    mon.view_result(DAMAGE)#몬스터 때리기 (1회용)
    pygame.display.update()