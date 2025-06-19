import pygame as pg

class Text:
    def __init__(self, text, text_color, tlx, tly, font_size = 36, font_family = None):
        self.text = str(text)
        self.text_color = text_color
        self.font_size = font_size
        self.font_family = font_family
        self.font = pg.font.SysFont(self.font_family, self.font_size)
        self.tlx = tlx
        self.tly = tly
        self.update()

    def update(self):
        self.image = self.font.render(self.text, 1, self.text_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.tlx, self.tly

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class TextCenter(Text):
    def __init__(self, text, text_color, cx, cy, font_size = 36, font_family = None):
        self.text = str(text)
        self.text_color = text_color
        self.font_size = font_size
        self.font_family = font_family
        self.font = pg.font.SysFont(self.font_family, self.font_size)
        self.cx = cx
        self.cy = cy
        self.update()

    def update(self):
        self.image = self.font.render(self.text, 1, self.text_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.cx, self.cy