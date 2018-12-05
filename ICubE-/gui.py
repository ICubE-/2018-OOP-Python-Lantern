import pygame as pg

# 나중에 from . import pygame_textinput으로 교체
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from SeeWhy import pygame_textinput

FONT_DIR = '..\\SeeWhy\\font\\NanumGothic.ttf'

pg.init()

TIME_DELAY = 10

TEXT_BOX_INACTIVE = (100, 100, 150)
TEXT_BOX_ACTIVE = (150, 150, 200)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class BaseGui:
    def __init__(self):
        pg.display.set_caption('상!평!')
        self.screen = None

    def make_text(self, text, font, font_size, color, center):
        text_box = pg.font.Font(font, font_size).render(text, True, color)
        text_box_rect = text_box.get_rect()
        text_box_rect.center = center
        return text_box, text_box_rect

    def make_input(self, font, font_size, color, center, width, max_len):
        input = pygame_textinput.TextInput(font_family=font, font_size=font_size, text_color=color, max_text=max_len)
        input_box = pg.Rect(0, 0, 0, 0)
        input_box.size = (width+font_size/4, font_size*1.5)
        input_box.center = center
        return input, input_box

    def make_text_bunch(self, text_list, font, font_size, color, top, centerx):
        text_box_list, text_box_rect_list = [], []
        cnt = 0
        for text in text_list:
            tb, tbr = self.make_text(text, font, font_size, color, (centerx, top+font_size*cnt))
            cnt += 1
            text_box_list.append(tb)
            text_box_rect_list.append(tbr)
        return text_box_list, text_box_rect_list


class AlertConnectionError(BaseGui):
    def __init__(self, width=400, height=200, font=FONT_DIR, font_size=16):
        super().__init__()
        self.width = width
        self.height = height
        self.font = font
        self.font_size = font_size

        self.screen = pg.display.set_mode((self.width, self.height))
        self.screen.fill(LIGHT_GRAY)
        msg = "연결이 비정상적으로 종료되었습니다."
        self.text, self.text_rect = self.make_text(msg, self.font, self.font_size, BLACK, (self.width / 2, 100))

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


class ChooseNickname(BaseGui):
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
        self.text, self.text_rect = self.make_text(desc, self.font, self.font_size, BLACK, (self.width/2, 200))
        self.input, self.input_box = self.make_input(font, font_size, BLACK, (self.width/2, 280), 200, 10)
        alert_desc = "특수문자를 사용할 수 없습니다."
        alert_loc = (self.input_box.centerx, self.input_box.centery + 30)
        self.alert, self.alert_rect = self.make_text(alert_desc, self.font, int(self.font_size/1.5), RED, alert_loc)

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
            input_loc = (self.input_box.left+self.font_size/4, self.input_box.top+self.font_size/4)
            self.screen.blit(self.input.get_surface(), input_loc)
            if banned_letter_came:
                self.screen.blit(self.alert, self.alert_rect)
            pg.display.update()

            pg.time.delay(TIME_DELAY)


class ChooseRoom(BaseGui):
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
        self.text_list, self.text_rect_list = self.make_text_bunch(text_list, font, font_size, BLACK, 80, self.width/2)
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
            input_loc = (self.input_box.left + self.font_size / 4, self.input_box.top + self.font_size / 4)
            self.screen.blit(self.input.get_surface(), input_loc)
            pg.display.update()

            pg.time.delay(TIME_DELAY)


if __name__ == '__main__':
    # tmp = ChooseNickname()
    # tmp = AlertConnectionError()
    tmp = ChooseRoom()
    tmp.show()
