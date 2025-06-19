import pygame as pg
from button import *
from main import *

class Setup:
    def __init__(self):
        self.number_of_players = 2

    def run(self):
        screen = pg.display.get_surface()
        while True:
            screen.fill((202, 228, 241))
            setup_buttons["nop"].draw(screen)

            if self.number_of_players == 2:
                if setup_buttons["two_chosen"].draw(screen):
                    self.number_of_players = 2
                if setup_buttons["three"].draw(screen):
                    self.number_of_players = 3
                if setup_buttons["four"].draw(screen):
                    self.number_of_players = 4
            elif self.number_of_players == 3:
                if setup_buttons["two"].draw(screen):
                    self.number_of_players = 2
                if setup_buttons["three_chosen"].draw(screen):
                    self.number_of_players = 3
                if setup_buttons["four"].draw(screen):
                    self.number_of_players = 4
            elif self.number_of_players == 4:
                if setup_buttons["two"].draw(screen):
                    self.number_of_players = 2
                if setup_buttons["three"].draw(screen):
                    self.number_of_players = 3
                if setup_buttons["four_chosen"].draw(screen):
                    self.number_of_players = 4

            if setup_buttons["back"].draw(screen):
                return "back"
            if setup_buttons["next"].draw(screen):
                return "next"

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "back"
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return "back"
            pg.display.update()

class Setup2(Setup):
    def __init__(self):
        super().__init__()
        self.tokens = ["centos", "debian", "redhat", "windows"]
        self.selected_tokens = []
        self.current_player = 1
        self.chosen_token = "centos"  

    def run(self):
        screen = pg.display.get_surface()
        while True:
            screen.fill((202, 228, 241))

            setup_buttons["player1"].draw(screen)

            available_tokens = [t for t in self.tokens if t not in self.selected_tokens]

            if setup_buttons["back"].draw(screen):
                if self.current_player > 1:
                    self.current_player -= 1
                    if self.selected_tokens:
                        self.selected_tokens.pop()
                    left = [t for t in self.tokens if t not in self.selected_tokens]
                    self.chosen_token = left[0] if left else "centos"
                else:
                    return "back"

            if len(self.selected_tokens) == self.number_of_players - 1:
                if setup_buttons["apply"].draw(screen):
                    if self.chosen_token in available_tokens:
                        self.selected_tokens.append(self.chosen_token)
                        return {"players": self.number_of_players, "tokens": self.selected_tokens}
            else:
                if setup_buttons["next"].draw(screen):
                    if self.chosen_token in available_tokens:
                        self.selected_tokens.append(self.chosen_token)
                        self.current_player += 1
                        left = [t for t in self.tokens if t not in self.selected_tokens]
                        self.chosen_token = left[0] if left else "centos"
                        continue

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "back"
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return "back"
            pg.display.update()
