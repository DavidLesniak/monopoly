import pygame as pg
from main import SCREEN_WIDTH, SCREEN_HEIGHT
start_img = pg.image.load("grafika/start.png")
start_hover_img = pg.image.load("grafika/start_hover.png")
setup_img = pg.image.load("grafika/setup.png")
setup_hover_img = pg.image.load("grafika/setup_hover.png")
exit_img = pg.image.load("grafika/exit.png")
exit_hover_img = pg.image.load("grafika/exit_hover.png")
button_width = start_img.get_width()
button_height = start_img.get_height()
button_spacing = 30  
menu_height = (button_height * 3) + (button_spacing * 2)

start_x = (SCREEN_WIDTH - button_width) // 2
start_y = (SCREEN_HEIGHT - menu_height) // 2
setup_x = start_x
setup_y = start_y + button_height + button_spacing
exit_x = start_x
exit_y = setup_y + button_height + button_spacing

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
