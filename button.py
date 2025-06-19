import pygame as pg
from config import *

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

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

NOP_img = pg.image.load("grafika/NOP.png")
two_img = pg.image.load("grafika/two.png")
two_hover_img = pg.image.load("grafika/two_hover.png")
two_chosen_img = pg.image.load("grafika/two_chosen.png")
three_chosen_img = pg.image.load("grafika/three_chosen.png")
four_chosen_img = pg.image.load("grafika/four_chosen.png")
three_img = pg.image.load("grafika/three.png")
three_hover_img = pg.image.load("grafika/three_hover.png")
four_img = pg.image.load("grafika/four.png")
four_hover_img = pg.image.load("grafika/four_hover.png")
number_button_width = two_img.get_width()
number_width = (number_button_width * 3) + (button_spacing * 2)

back_img = pg.image.load("grafika/back.png")
back_hover_img = pg.image.load("grafika/back_hover.png")
next_img = pg.image.load("grafika/next.png")
next_hover_img = pg.image.load("grafika/next_hover.png")

start_x = (SCREEN_WIDTH - button_width) // 2
start_y = (SCREEN_HEIGHT - menu_height) // 2
setup_x = start_x
setup_y = start_y + button_height + button_spacing
exit_x = start_x
exit_y = setup_y + button_height + button_spacing

NOP_x = (SCREEN_WIDTH - NOP_img.get_width()) // 2
NOP_y = (SCREEN_HEIGHT - NOP_img.get_height()) // 4
between_NOP_and_numbers_height = NOP_y + 1
between_NOP_and_numbers_width = (SCREEN_WIDTH - number_width) // 2
between_numbers_and_next_back_height = between_NOP_and_numbers_height + 30


start_button = Button(start_x, start_y, start_img, start_hover_img, 1)
setup_button = Button(setup_x, setup_y, setup_img, setup_hover_img, 1)
exit_button = Button(exit_x, exit_y, exit_img, exit_hover_img, 1)

NOP_button = Button(NOP_x, NOP_y, NOP_img, NOP_img, 1)
two_button = Button(between_NOP_and_numbers_width, NOP_y + between_NOP_and_numbers_height, two_img, two_hover_img, 1)
two_chosen_button = Button(between_NOP_and_numbers_width, NOP_y + between_NOP_and_numbers_height, two_chosen_img, two_chosen_img, 1)
three_button = Button(between_NOP_and_numbers_width + number_button_width + button_spacing, NOP_y + between_NOP_and_numbers_height, three_img, three_hover_img, 1)
three_chosen_button = Button(between_NOP_and_numbers_width + number_button_width + button_spacing, NOP_y + between_NOP_and_numbers_height, three_chosen_img, three_chosen_img, 1)
four_button = Button(between_NOP_and_numbers_width + 2 * (number_button_width + button_spacing), NOP_y + between_NOP_and_numbers_height, four_img, four_hover_img, 1)
four_chosen_button = Button(between_NOP_and_numbers_width + 2 * (number_button_width + button_spacing), NOP_y + between_NOP_and_numbers_height, four_chosen_img, four_chosen_img, 1)
back_button = Button(between_NOP_and_numbers_width, between_numbers_and_next_back_height + between_NOP_and_numbers_width + NOP_y, back_img, back_hover_img, 1)


throwButton = Button(380, 300, pg.image.load("grafika/throw.png"), pg.image.load("grafika/throw_hover.png"), 0.5)
throwButtonNoactive = Button(380, 300, pg.image.load('grafika/throw_notactive.png'), pg.image.load('grafika/throw_notactive.png'), 0.5)
buyButton = Button(380, 370, pg.image.load("grafika/buy.png"), pg.image.load("grafika/buy_hover.png"), 0.5)
buyButtonNoactive = Button(380, 370, pg.image.load("grafika/buy_noactive.png"), pg.image.load("grafika/buy_noactive.png"), 0.5)
endthrowButton = Button(380, 440, pg.image.load("grafika/endthrow.png"), pg.image.load("grafika/endthrow_hover.png"), 0.5)
endthrowButtonNoactive = Button(380, 440, pg.image.load("grafika/endthrow_notactive.png"), pg.image.load("grafika/endthrow_notactive.png"), 0.5)
upgradeButton = Button(380, 370, pg.image.load("grafika/upgrade.png"), pg.image.load("grafika/upgrade_hover.png"), 0.5)
