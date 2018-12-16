from gui_game import *

#넣어줘야 할 값
RoundName='KYPT'
DAMAGE=24

#기초 선언
base=stage(RoundName)#배경 만듦

#몬스터 선언
mon=monster(RoundName, 20)

#일반적일때
while not True:
    #기본
    pygame.display.init()
    pygame.time.delay(10)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            self.run = False
            break

    base.refill()#계속 배경보이기
    mon.refill()#계속 몬스터 보이기
    pygame.display.update()

#DAMAGE가 있을때
while not False:
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