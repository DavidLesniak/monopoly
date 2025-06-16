import pygame as pg
start_img = pg.image.load("grafika/start.png")
start_hover_img = pg.image.load("grafika/start_hover.png")
exit_img = pg.image.load("grafika/exit.png")
exit_hover_img = pg.image.load("grafika/exit_hover.png")
button_width = start_img.get_width()

class Button:
    def __init__(self, x, y, image, hover_image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.hover_image = pg.transform.scale(hover_image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False

    def draw(self, screen):
        action = False
        position = pg.mouse.get_pos()
        if self.rect.collidepoint(position):
            screen.blit(self.hover_image, self.rect)
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        else:
            screen.blit(self.image, self.rect)
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action
