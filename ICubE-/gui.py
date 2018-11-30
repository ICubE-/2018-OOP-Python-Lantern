import pygame as pg
import pygame_textinput

pg.init()

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

    def make_input(self, font, font_size, color, center, width):
        input = pygame_textinput.TextInput(font_family=font, font_size=font_size, text_color=color)
        input_box = pg.Rect(0, 0, 0, 0)
        input_box.size = (width+font_size/4, font_size*1.5)
        input_box.center = center
        return input, input_box


class ChooseNickname(BaseGui):
    def __init__(self, width=640, height=480, font='..\\SeeWhy\\font\\NanumGothic.ttf', font_size=20):
        BaseGui.__init__(self)
        self.width = width
        self.height = height
        self.font = font
        self.font_size = font_size

        self.screen = pg.display.set_mode((self.width, self.height))
        self.screen.fill(LIGHT_GRAY)
        self.desc = "사용할 이름을 입력하세요."
        self.text, self.text_rect = self.make_text(self.desc, self.font, self.font_size, BLACK, (self.width/2, 200))
        self.input, self.input_box = self.make_input(font, font_size, BLACK, (self.width/2, 300), 200)

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

"""
import pygame as pg


def main():
    screen = pg.display.set_mode((640, 480))
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    input_box = pg.Rect(100, 100, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        print(text)
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
"""