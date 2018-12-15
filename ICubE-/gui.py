import pygame as pg

# 나중에 from . import pygame_textinput으로 교체
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from SeeWhy import pygame_textinput

FONT_DIR = '..\\SeeWhy\\font\\NanumSquareRoundEB.ttf'

pg.init()

TIME_DELAY = 10

TEXT_BOX_INACTIVE = (100, 100, 150)
TEXT_BOX_ACTIVE = (150, 150, 200)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)


class BaseGui:
    def __init__(self):
        pg.display.init()
        pg.display.set_caption('상!평!')
        self.screen = None

    def make_text(self, text, font, font_size, color, coord, h_align, v_align):
        """
        매개변수를 받아 텍스트가 든 Surface, 그것의 테두리 Rect를 반환함.
        :param text: 텍스트.
        :param font: 폰트.
        :param font_size: 폰트 크기.
        :param color: 색.
        :param coord: 좌표. h_align과 v_align에 따라 무엇을 의미하는지 바뀜.
        :param h_align: 0이면 왼쪽 정렬, 1이면 가운데 정렬, 2이면 오른쪽 정렬.
        :param v_align: 0이면 위쪽 정렬, 1이면 가운데 정렬, 2이면 아래쪽 정렬.
        :return:
        """
        text_box = pg.font.Font(font, font_size).render(text, True, color)
        text_box_rect = text_box.get_rect()
        if h_align == 0:
            text_box_rect.left = coord[0]
        elif h_align == 1:
            text_box_rect.centerx = coord[0]
        elif h_align == 2:
            text_box_rect.right = coord[0]
        else:
            raise RuntimeError("'h_align' should be one of 0, 1, 2.") from Exception
        if v_align == 0:
            text_box_rect.top = coord[1]
        elif v_align == 1:
            text_box_rect.centery = coord[1]
        elif v_align == 2:
            text_box_rect.bottom = coord[1]
        else:
            raise RuntimeError("'v_align' should be one of 0, 1, 2.") from Exception
        # text_box_rect.center = coord
        return text_box, text_box_rect

    def make_input(self, font, font_size, color, center, width, max_len):
        input = pygame_textinput.TextInput(font_family=font, font_size=font_size, text_color=color, max_text=max_len)
        input_box = pg.Rect(0, 0, 0, 0)
        input_box.size = (width+font_size/4, font_size*2)
        input_box.center = center
        return input, input_box

    def make_text_bunch(self, text_list, font, font_size, color, top, coord_x, h_align):
        """
        매개변수를 받아 텍스트가 든 Surface의 리스트, 그것의 테두리 Rect의 리스트를 반환함.
        :param text_list: 텍스틀 리스트.
        :param font: 폰트.
        :param font_size: 폰트 크기.
        :param color: 색.
        :param top: 위 좌표.
        :param coord_x: 수평 좌표. h_align에 따라 무엇을 의미하는지 바뀜.
        :param h_align: 0이면 왼쪽 정렬, 1이면 가운데 정렬, 2이면 오른쪽 정렬.
        :return:
        """
        text_box_list, text_box_rect_list = [], []
        cnt = 0
        for text in text_list:
            if h_align == 0:
                tb, tbr = self.make_text(text, font, font_size, color, (coord_x, top+font_size*cnt*1.6), 0, 0)
            elif h_align == 1:
                tb, tbr = self.make_text(text, font, font_size, color, (coord_x, top+font_size*cnt*1.6), 1, 0)
            elif h_align == 2:
                tb, tbr = self.make_text(text, font, font_size, color, (coord_x, top+font_size*cnt*1.6), 2, 0)
            else:
                raise RuntimeError("'h_align' should be one of 0, 1, 2.") from Exception
            cnt += 1
            text_box_list.append(tb)
            text_box_rect_list.append(tbr)
        return text_box_list, text_box_rect_list


class AlertConnectionErrorGui(BaseGui):
    def __init__(self, width=400, height=200, font=FONT_DIR, font_size=16):
        super().__init__()
        self.width = width
        self.height = height
        self.font = font
        self.font_size = font_size

        self.screen = pg.display.set_mode((self.width, self.height))
        self.screen.fill(LIGHT_GRAY)
        msg = "연결이 비정상적으로 종료되었습니다."
        self.text, self.text_rect = self.make_text(msg, self.font, self.font_size, BLACK, (self.width / 2, 100), 1, 1)

    def show(self):
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    return

            self.screen.fill(LIGHT_GRAY)
            self.screen.blit(self.text, self.text_rect)
            pg.display.update()

            pg.time.delay(TIME_DELAY)


class ChooseNicknameGui(BaseGui):
    def __init__(self, width=640, height=480, font=FONT_DIR, font_size=20, banned_letters="$"):
        super().__init__()
        self.width = width
        self.height = height
        self.font = font
        self.font_size = font_size
        self.banned_letters = banned_letters

        self.screen = pg.display.set_mode((self.width, self.height))
        self.screen.fill(LIGHT_GRAY)
        desc = "사용할 이름을 입력하세요."
        self.text, self.text_rect = self.make_text(desc, self.font, self.font_size, BLACK, (self.width/2, 200), 1, 1)
        self.input, self.input_box = self.make_input(font, font_size, BLACK, (self.width/2, 280), 200, 10)
        alert_desc = "특수문자를 사용할 수 없습니다."
        alert_loc = (self.input_box.centerx, self.input_box.centery + 30)
        self.alert, self.alert_rect = self.make_text(alert_desc, self.font, int(self.font_size/1.5), RED, alert_loc, 1, 1)

    def show(self):
        banned_letter_came = False

        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.display.quit()
                    return
            nickname = self.input.update(events)
            if nickname:
                flag = False
                for letter in nickname:
                    if letter in self.banned_letters:
                        flag = True
                        break
                if flag:
                    banned_letter_came = True
                else:
                    pg.display.quit()
                    return nickname

            self.screen.fill(LIGHT_GRAY)
            self.screen.blit(self.text, self.text_rect)
            pg.draw.rect(self.screen, WHITE, self.input_box, 0)
            pg.draw.rect(self.screen, BLACK, self.input_box, 1)
            input_loc = (self.input_box.left+self.font_size/4, self.input_box.top+self.font_size/2)
            self.screen.blit(self.input.get_surface(), input_loc)
            if banned_letter_came:
                self.screen.blit(self.alert, self.alert_rect)
            pg.display.update()

            pg.time.delay(TIME_DELAY)


class ChooseRoomGui(BaseGui):
    def __init__(self, width=640, height=480, font=FONT_DIR, font_size=16, rooms=('A', 'B')):
        super().__init__()
        self.width = width
        self.height = height
        self.font = font
        self.font_size = font_size

        self.screen = pg.display.set_mode((self.width, self.height))
        self.screen.fill(LIGHT_GRAY)
        pf = ["게임방 목록", "="*40]
        sf = ["="*40, "", "들어갈 게임방의 이름을 입력하세요.", "목록에 없는 이름이 입력되면 그 이름으로 게임방을 생성합니다."]
        text_list = pf + list(rooms) + sf
        self.text_list, self.text_rect_list = self.make_text_bunch(text_list, font, font_size, BLACK, 80, self.width/2, 1)
        # desc = "게임방 목록\n"+"\n".join(rooms)+"\n들어갈 게임방의 이름을 입력하세요.\n목록에 없는 이름이 입력되면 그 이름으로 게임방을 생성합니다."
        # self.text, self.text_rect = self.make_text(desc, self.font, self.font_size, BLACK, (self.width / 2, 200))
        self.input, self.input_box = self.make_input(font, font_size, BLACK, (self.width/2, 400), 200, 20)

    def show(self):
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.display.quit()
                    return
            room_name = self.input.update(events)
            if room_name:
                pg.display.quit()
                return room_name

            self.screen.fill(LIGHT_GRAY)
            for i in range(len(self.text_list)):
                self.screen.blit(self.text_list[i], self.text_rect_list[i])
            # self.screen.blit(self.text, self.text_rect)
            pg.draw.rect(self.screen, WHITE, self.input_box, 0)
            pg.draw.rect(self.screen, BLACK, self.input_box, 1)
            input_loc = (self.input_box.left + self.font_size/4, self.input_box.top + self.font_size/2)
            self.screen.blit(self.input.get_surface(), input_loc)
            pg.display.update()

            pg.time.delay(TIME_DELAY)


class RoomGui(BaseGui):
    def __init__(self, width=1024, height=576, font=FONT_DIR, font_size=20, room_name="ROOM", client_nickname="NICK", members=()):
        super().__init__()
        self.width = width
        self.height = height
        self.font = font
        self.font_size = font_size
        self.room_name = room_name
        self.client_nickname = client_nickname
        self.members = list(members)
        self.is_head = False
        self.can_start = False
        self.chat = []

        self.screen = pg.display.set_mode((self.width, self.height))

        self.msg = pygame_textinput.TextInput(font_family=self.font, font_size=self.font_size, text_color=BLACK, max_text=36)
        self.game_button = pg.Rect((self.width*11/16, self.height*7/8), (self.width*5/32, self.height/8))
        self.leave_button = pg.Rect((self.width*27/32, self.height*7/8), (self.width*5/32, self.height/8))

    def display_base(self):
        self.screen.fill(WHITE)
        pg.draw.rect(self.screen, BLACK, ((0, 0), (self.width, self.height/8)), 0)
        pg.draw.rect(self.screen, LIGHT_GRAY, ((self.width*11/16, self.height/8), (self.width*5/16, self.height*3/4)), 0)
        pg.draw.rect(self.screen, LIGHT_GRAY if self.is_head and not self.can_start else GREEN, self.game_button, 0)
        pg.draw.rect(self.screen, RED, self.leave_button, 0)

        pg.draw.line(self.screen, BLACK, (0, self.height/8), (self.width, self.height/8), 2)
        pg.draw.line(self.screen, BLACK, (self.width*11/16, self.height/8), (self.width*11/16, self.height), 2)
        pg.draw.line(self.screen, BLACK, (0, self.height-self.font_size*2), (self.width*11/16, self.height-self.font_size*2), 2)
        pg.draw.line(self.screen, BLACK, (self.width*11/16, self.height*7/8), (self.width, self.height*7/8), 2)
        pg.draw.line(self.screen, BLACK, (self.width*27/32, self.height*7/8), (self.width*27/32, self.height), 2)
        pg.draw.rect(self.screen, BLACK, ((0, 0), (self.width, self.height)), 4)

        title = self.make_text(self.room_name, self.font, int(self.height/16), WHITE, (self.width/2, self.height/16), 1, 1)
        self.screen.blit(title[0], title[1])
        game = self.make_text("시작" if self.is_head else "준비", self.font, int(self.font_size*1.2), BLACK, (self.width*49/64, self.height*15/16), 1, 1)
        self.screen.blit(game[0], game[1])
        leave = self.make_text("나가기", self.font, int(self.font_size*1.2), BLACK, (self.width*59/64, self.height*15/16), 1, 1)
        self.screen.blit(leave[0], leave[1])
        chat_arrow = self.make_text(">", self.font, self.font_size, BLACK, (self.font_size, self.height-self.font_size), 1, 1)
        self.screen.blit(chat_arrow[0], chat_arrow[1])

    def make_member_list(self, member_list, font, font_size, top, coord_x, h_align):
        text_box_list, text_box_rect_list = [], []
        cnt = 0
        for member in member_list:
            text, color = member[0], GREEN if member[1] else RED
            if member == member_list[0]:
                color = BLACK
            if h_align == 0:
                tb, tbr = self.make_text(text, font, font_size, color, (coord_x, top+font_size*cnt*1.6), 0, 0)
            elif h_align == 1:
                tb, tbr = self.make_text(text, font, font_size, color, (coord_x, top+font_size*cnt*1.6), 1, 0)
            elif h_align == 2:
                tb, tbr = self.make_text(text, font, font_size, color, (coord_x, top+font_size*cnt*1.6), 2, 0)
            else:
                raise RuntimeError("'h_align' should be one of 0, 1, 2.") from Exception
            cnt += 1
            text_box_list.append(tb)
            text_box_rect_list.append(tbr)
        return text_box_list, text_box_rect_list

    def set_members(self, members):
        self.members = members
        if self.members.__len__() == 1:
            self.can_start = False
        else:
            flag = True
            for i in self.members[1:]:
                if not i[1]:
                    flag = False
                    break
            self.can_start = flag

    def set_head(self):
        self.is_head = True

    def add_chat(self, msg):
        if len(self.chat) >= 14:
            self.chat.pop(0)
        self.chat.append(msg)

    def quit(self):
        pg.display.quit()

    def show(self):
        com = None
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.display.quit()
                return
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.game_button.collidepoint(event.pos[0], event.pos[1]):
                        if self.is_head:
                            com = "$gameStart" if self.can_start else None
                        else:
                            com = "$ready"
                    elif self.leave_button.collidepoint(event.pos[0], event.pos[1]):
                        com = "$leave"

        msg = self.msg.update(events)

        self.display_base()
        self.screen.blit(self.msg.get_surface(), (self.font_size*1.75, self.height - self.font_size*1.5))
        chat_list, chat_rect_list = self.make_text_bunch(self.chat, self.font, self.font_size, BLACK, self.height/8+self.font_size*0.75, self.font_size, 0)
        for i in range(len(chat_list)):
            self.screen.blit(chat_list[i], chat_rect_list[i])
        member_list, member_rect_list = self.make_member_list(self.members, self.font, self.font_size, self.height/8+self.font_size*2, self.width*11/16+self.font_size, 0)
        for i in range(len(member_list)):
            self.screen.blit(member_list[i], member_rect_list[i])

        pg.display.update()

        pg.time.delay(TIME_DELAY)

        return msg, com


if __name__ == '__main__':
    # tmp = ChooseNickname()
    # tmp = AlertConnectionError()
    # tmp = ChooseRoomGui()
    tmp = RoomGui()
    # tmp.set_head()
    tmp.set_members(("A", "asdf", "0055", "응으으으"))
    while True:
        tmp.show()
