import pygame as pg
from button import *
from main import *

class Setup:
    def __init__(self):
        self.number_of_players = 2
        self.two_button = Button(between_NOP_and_numbers_width, NOP_y + between_NOP_and_numbers_height, two_img, two_hover_img, 1)
        self.three_button = Button(between_NOP_and_numbers_width + number_button_width + button_spacing, NOP_y + between_NOP_and_numbers_height, three_img, three_hover_img, 1)
        self.four_button = Button(between_NOP_and_numbers_width + 2 * (number_button_width + button_spacing), NOP_y + between_NOP_and_numbers_height, four_img, four_hover_img, 1)
        self.run()

    def run(self):
        screen = pg.display.get_surface()
        run = True
        while run:
            screen.fill((202, 228, 241))
            NOP_button.draw(screen)

            if self.number_of_players == 2:
                self.two_button.image = two_chosen_img
                self.two_button.hover_image = two_chosen_img
                self.three_button.image = three_img
                self.three_button.hover_image = three_hover_img
                self.four_button.image = four_img
                self.four_button.hover_image = four_hover_img
            elif self.number_of_players == 3:
                self.two_button.image = two_img
                self.two_button.hover_image = two_hover_img
                self.three_button.image = three_chosen_img
                self.three_button.hover_image = three_chosen_img
                self.four_button.image = four_img
                self.four_button.hover_image = four_hover_img
            elif self.number_of_players == 4:
                self.two_button.image = two_img
                self.two_button.hover_image = two_hover_img
                self.three_button.image = three_img
                self.three_button.hover_image = three_hover_img
                self.four_button.image = four_chosen_img
                self.four_button.hover_image = four_chosen_img

            if self.two_button.draw(screen):
                self.number_of_players = 2
            if self.three_button.draw(screen):
                self.number_of_players = 3
            if self.four_button.draw(screen):
                self.number_of_players = 4

            if back_button.draw(screen):
                run = False

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False    
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    run = False
            pg.display.update()
