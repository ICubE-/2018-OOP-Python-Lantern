import pygame as pg
from . import pygame_textinput

pg.init()

FONT_DIR = '..\\SeeWhy\\font\\NanumGothic.ttf'

TIME_DELAY = 10

TEXT_BOX_INACTIVE = (100, 100, 150)
TEXT_BOX_ACTIVE = (150, 150, 200)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
BLACK = (0, 0, 0)


class BaseGui:
    def __init__(self):
        pg.display.set_caption('상!평!')
        self.screen = pg.display.set_mode((0,0))

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


class AlertConnectionError(BaseGui):
    def __init__(self, width=200, height=100, font=FONT_DIR, font_size=20):
        super().__init__()
        self.width = width
        self.height = height
        self.font = font
        self.font_size = font_size

        self.screen = pg.display.set_mode((self.width, self.height))
        self.screen.fill(LIGHT_GRAY)
        self.msg = "연결이 비정상적으로 종료되었습니다."
        #self.btn =


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
        self.desc = "사용할 이름을 입력하세요."
        self.text, self.text_rect = self.make_text(self.desc, self.font, self.font_size, BLACK, (self.width/2, 200))
        self.input, self.input_box = self.make_input(font, font_size, BLACK, (self.width/2, 280), 200, 10)

    def show(self):
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    return
            self.screen.fill(LIGHT_GRAY)
            self.screen.blit(self.text, self.text_rect)
            nickname = self.input.update(events)
            if nickname:
                print(nickname)
            pg.draw.rect(self.screen, WHITE, self.input_box, 0)
            pg.draw.rect(self.screen, BLACK, self.input_box, 1)
            input_loc = (self.input_box.left+self.font_size/4, self.input_box.top+self.font_size/4)
            self.screen.blit(self.input.get_surface(), input_loc)
            pg.display.update()

            pg.time.delay(TIME_DELAY)


if __name__ == '__main__':
    tmp = ChooseNickname()
    tmp.show()
