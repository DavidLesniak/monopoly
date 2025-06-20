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

class Setup2():
    def __init__(self, number_of_players):
        self.tokens = ["centos", "debian", "redhat", "windows"]
        self.selected_tokens = []
        self.current_player = 1
        self.chosen_token = "centos"
        self.number_of_players = number_of_players  
        self.input_text = ""              
        self.player_names = [""] * self.number_of_players 

    def run(self):
        screen = pg.display.get_surface()
        y = 280
        y_input = y + 100

        while True:
            screen.fill((202, 228, 241))

            setup_buttons[f"player{self.current_player}"].draw(screen)

            available_tokens = [t for t in self.tokens if t not in self.selected_tokens]
            button_width = BUTTON_IMAGES["centos"][0].get_width()
            num_buttons = len(available_tokens)
            total_width = num_buttons * button_width + (num_buttons - 1) * BUTTON_SPACING
            pawn_x = (SCREEN_WIDTH - total_width) // 2
            
            for idx, token in enumerate(available_tokens):
                x = pawn_x + idx * (button_width + BUTTON_SPACING)
                if token == self.chosen_token:
                    setup_buttons[f"chosen_{token}"].rect.topleft = (x, y)
                    if setup_buttons[f"chosen_{token}"].draw(screen):
                        self.chosen_token = token
                else:
                    setup_buttons[token].rect.topleft = (x, y)
                    if setup_buttons[token].draw(screen):
                        self.chosen_token = token

            setup_buttons["name"].draw(screen)

            draw_input(screen, y_input, self.input_text)

            if setup_buttons["back"].draw(screen):
                if self.current_player > 1:
                    self.current_player -= 1
                    if self.selected_tokens:
                        self.selected_tokens.pop()
                    left = [t for t in self.tokens if t not in self.selected_tokens]
                    self.chosen_token = left[0] if left else "centos"
                    self.input_text = self.player_names[self.current_player - 1]
                else:
                    return "back"

            if len(self.selected_tokens) < self.number_of_players - 1:
                if setup_buttons["next"].draw(screen):
                    if self.chosen_token in available_tokens:
                        name = self.input_text.strip() if self.input_text.strip() else f"player{self.current_player}"
                        self.player_names[self.current_player - 1] = name
                        self.selected_tokens.append(self.chosen_token)
                        self.current_player += 1
                        left = [t for t in self.tokens if t not in self.selected_tokens]
                        self.chosen_token = left[0] if left else "centos"
                        self.input_text = ""
                        continue
            else:
                if setup_buttons["apply"].draw(screen):
                    if self.chosen_token in available_tokens:
                        name = self.input_text.strip() if self.input_text.strip() else f"player{self.current_player}"
                        self.player_names[self.current_player - 1] = name
                        self.selected_tokens.append(self.chosen_token)
                        player_tokens = {f"player{i+1}": token for i, token in enumerate(self.selected_tokens)}
                        return {
                            "tokens": player_tokens,
                            "names": self.player_names
                        }

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "back"
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return "back"
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == pg.K_RETURN:
                        pass  
                    else:
                        if len(self.input_text) < 16:
                            self.input_text += event.unicode
            pg.display.update()
