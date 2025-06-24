import pygame as pg
from config import *

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
BUTTON_SPACING = 30

def load_image(path):
    return pg.image.load(path)

BUTTON_IMAGES = {
    "start": (load_image("grafika/start.png"), load_image("grafika/start_hover.png")),
    "setup": (load_image("grafika/setup.png"), load_image("grafika/setup_hover.png")),
    "exit": (load_image("grafika/exit.png"), load_image("grafika/exit_hover.png")),
    "back": (load_image("grafika/back.png"), load_image("grafika/back_hover.png")),
    "next": (load_image("grafika/next.png"), load_image("grafika/next_hover.png")),
    "apply": (load_image("grafika/apply.png"), load_image("grafika/apply_hover.png")),
    "nop": (load_image("grafika/NOP.png"), load_image("grafika/NOP.png")),
    "two": (load_image("grafika/two.png"), load_image("grafika/two_hover.png")),
    "two_chosen": (load_image("grafika/two_chosen.png"), load_image("grafika/two_chosen.png")),
    "three": (load_image("grafika/three.png"), load_image("grafika/three_hover.png")),
    "three_chosen": (load_image("grafika/three_chosen.png"), load_image("grafika/three_chosen.png")),
    "four": (load_image("grafika/four.png"), load_image("grafika/four_hover.png")),
    "four_chosen": (load_image("grafika/four_chosen.png"), load_image("grafika/four_chosen.png")),
    "player1": (load_image("grafika/player1.png"), load_image("grafika/player1.png")),
    "player2": (load_image("grafika/player2.png"), load_image("grafika/player2.png")),
    "player3": (load_image("grafika/player3.png"), load_image("grafika/player3.png")),
    "player4": (load_image("grafika/player4.png"), load_image("grafika/player4.png")),
    "centos": (load_image("images/centos.png"), load_image("images/hover_centos.png")),
    "chosen_centos": (load_image("images/chosen_centos.png"), load_image("images/chosen_centos.png")),
    "debian": (load_image("images/debian.png"), load_image("images/hover_debian.png")),
    "chosen_debian": (load_image("images/chosen_debian.png"), load_image("images/chosen_debian.png")),
    "redhat": (load_image("images/redhat.png"), load_image("images/hover_redhat.png")),
    "chosen_redhat": (load_image("images/chosen_redhat.png"), load_image("images/chosen_redhat.png")),
    "windows": (load_image("images/windows.png"), load_image("images/hover_windows.png")),
    "chosen_windows": (load_image("images/chosen_windows.png"), load_image("images/chosen_windows.png")),
    "name": (load_image("grafika/name.png"), load_image("grafika/name.png")),
}

class Button:
    def __init__(self, x, y, image, hover_image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.hover_image = pg.transform.scale(hover_image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.was_pressed = False

    def draw(self, screen):
        action = False
        position = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()[0]
        if self.rect.collidepoint(position):
            screen.blit(self.hover_image, self.rect)
            if mouse_pressed and not self.was_pressed:
                self.was_pressed = True
            elif not mouse_pressed and self.was_pressed:
                self.was_pressed = False
                action = True
        else:
            screen.blit(self.image, self.rect)
        if not mouse_pressed:
            self.was_pressed = False
        return action

def create_menu_buttons():
    button_width = BUTTON_IMAGES["start"][0].get_width()
    button_height = BUTTON_IMAGES["start"][0].get_height()
    menu_height = (button_height * 3) + (BUTTON_SPACING * 2)
    start_x = (SCREEN_WIDTH - button_width) // 2
    start_y = (SCREEN_HEIGHT - menu_height) // 2

    buttons = {
        "start": Button(start_x, start_y, *BUTTON_IMAGES["start"]),
        "setup": Button(start_x, start_y + button_height + BUTTON_SPACING, *BUTTON_IMAGES["setup"]),
        "exit": Button(start_x, start_y + 2 * (button_height + BUTTON_SPACING), *BUTTON_IMAGES["exit"]),
    }
    return buttons

def create_setup_buttons():
    nop_img = BUTTON_IMAGES["nop"][0]
    number_button_width = BUTTON_IMAGES["two"][0].get_width()
    number_button_height = BUTTON_IMAGES["two"][0].get_height()
    back_width = BUTTON_IMAGES["back"][0].get_width()
    next_width = BUTTON_IMAGES["next"][0].get_width()
    name_width = BUTTON_IMAGES["name"][0].get_width()
    number_width = (number_button_width * 3) + (BUTTON_SPACING * 2)
    nop_x = (SCREEN_WIDTH - nop_img.get_width()) // 2
    nop_y = (SCREEN_HEIGHT - nop_img.get_height()) // 4
    numbers_y = nop_y + nop_img.get_height() + BUTTON_SPACING
    numbers_x = (SCREEN_WIDTH - number_width) // 2
    nav_width = back_width + BUTTON_SPACING + next_width
    nav_x = numbers_x + (number_width - nav_width) // 2
    nav_y = numbers_y + number_button_height + BUTTON_SPACING
    back_x = nav_x
    next_x = nav_x + back_width + BUTTON_SPACING

    system_buttons = ["centos", "debian", "redhat", "windows"]
    button_width = BUTTON_IMAGES["centos"][0].get_width()
    num_buttons = len(system_buttons)
    total_width = num_buttons * button_width + (num_buttons - 1) * BUTTON_SPACING
    pawn_x = (SCREEN_WIDTH - total_width) // 2
    name_x = (SCREEN_WIDTH - name_width) // 2
    
    

    buttons = {
        "nop": Button(nop_x, nop_y, *BUTTON_IMAGES["nop"]),
        "two": Button(numbers_x, numbers_y, *BUTTON_IMAGES["two"]),
        "two_chosen": Button(numbers_x, numbers_y, *BUTTON_IMAGES["two_chosen"]),
        "three": Button(numbers_x + number_button_width + BUTTON_SPACING, numbers_y, *BUTTON_IMAGES["three"]),
        "three_chosen": Button(numbers_x + number_button_width + BUTTON_SPACING, numbers_y, *BUTTON_IMAGES["three_chosen"]),
        "four": Button(numbers_x + 2 * (number_button_width + BUTTON_SPACING), numbers_y, *BUTTON_IMAGES["four"]),
        "four_chosen": Button(numbers_x + 2 * (number_button_width + BUTTON_SPACING), numbers_y, *BUTTON_IMAGES["four_chosen"]),
        "back": Button(back_x, nav_y, *BUTTON_IMAGES["back"]),
        "next": Button(next_x, nav_y, *BUTTON_IMAGES["next"]),
        "apply": Button(next_x, nav_y, *BUTTON_IMAGES["apply"]),
        "player1": Button(nop_x, nop_y, *BUTTON_IMAGES["player1"]),
        "player2": Button(nop_x, nop_y, *BUTTON_IMAGES["player2"]),
        "player3": Button(nop_x, nop_y, *BUTTON_IMAGES["player3"]),
        "player4": Button(nop_x, nop_y, *BUTTON_IMAGES["player4"]),  
        
        "centos": Button(pawn_x + 0 * (button_width + BUTTON_SPACING), numbers_y, *BUTTON_IMAGES["centos"]),
        "chosen_centos": Button(pawn_x + 0 * (button_width + BUTTON_SPACING), numbers_y, *BUTTON_IMAGES["chosen_centos"]),
        "debian": Button(pawn_x + 1 * (button_width + BUTTON_SPACING), numbers_y, *BUTTON_IMAGES["debian"]),
        "chosen_debian": Button(pawn_x + 1 * (button_width + BUTTON_SPACING), numbers_y, *BUTTON_IMAGES["chosen_debian"]),
        "redhat": Button(pawn_x + 2 * (button_width + BUTTON_SPACING), numbers_y, *BUTTON_IMAGES["redhat"]),
        "chosen_redhat": Button(pawn_x + 2 * (button_width + BUTTON_SPACING), numbers_y, *BUTTON_IMAGES["chosen_redhat"]),
        "windows": Button(pawn_x + 3 * (button_width + BUTTON_SPACING), numbers_y, *BUTTON_IMAGES["windows"]),
        "chosen_windows": Button(pawn_x + 3 * (button_width + BUTTON_SPACING), numbers_y, *BUTTON_IMAGES["chosen_windows"]),
        "name": Button(name_x, numbers_y + BUTTON_SPACING, *BUTTON_IMAGES["name"]),
    }
    return buttons

def draw_input(screen, y_input, input_text):
    font = pg.font.SysFont(None, 36)
    input_rect = pg.Rect((screen.get_width() // 2) - 100, y_input, 200, 40)
    color_active = pg.Color('#0000ff')
    pg.draw.rect(screen, color_active, input_rect, 2)
    input_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

menu_buttons = create_menu_buttons()
setup_buttons = create_setup_buttons()

throwButton = Button(415, 300, pg.image.load("grafika/throw.png"), pg.image.load("grafika/throw_hover.png"), 0.5)
throwButtonNoactive = Button(415, 300, pg.image.load('grafika/throw_notactive.png'), pg.image.load('grafika/throw_notactive.png'), 0.5)
buyButton = Button(415, 380, pg.image.load("grafika/buy.png"), pg.image.load("grafika/buy_hover.png"), 0.5)
buyButtonNoactive = Button(415, 380, pg.image.load("grafika/buy_noactive.png"), pg.image.load("grafika/buy_noactive.png"), 0.5)
endthrowButton = Button(415, 460, pg.image.load("grafika/endthrow.png"), pg.image.load("grafika/endthrow_hover.png"), 0.5)
endthrowButtonNoactive = Button(415, 460, pg.image.load("grafika/endthrow_notactive.png"), pg.image.load("grafika/endthrow_notactive.png"), 0.5)
upgradeButton = Button(415, 380, pg.image.load("grafika/upgrade.png"), pg.image.load("grafika/upgrade_hover.png"), 0.5)
