import pygame as pg


pg.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FONT = pg.font.SysFont(None, 24)

pg.display.set_caption("Monopoly")
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Card:
    def __init__(self, x, y, index):
        self.index = index
        self.name = None
        self.price = None
        self.x = x 
        self.y = y
        self.width = 80
        self.height = 80
        self.owner = None

    def draw(self, screen):
        pg.draw.rect(screen, (247, 247, 247), (self.x, self.y, self.width, self.height))

        index = FONT.render(str(self.index), True, (0, 0, 0))
        screen.blit(index, (self.x+5, self.y+5))


class Board:
    def __init__(self):
        self.cards = []
        self.create_board()

    def create_board(self):
        o=1

        for i in range(4):
            if i==0:
                for j in range(10):
                    self.cards.append(Card(j*80, 0, o))
                    o+=1

            if i==1:
                for j in range(9):
                    self.cards.append(Card(720, (j*80)+80, o))
                    o+=1

            if i==2:
                for j in reversed(range(10)):
                    self.cards.append(Card((j*80)-80, 720, o))
                    o+=1

            if i==3:
                for j in reversed(range(8)):
                    self.cards.append(Card(0, (j*80)+80, o))
                    o+=1

    def draw(self, screen):
        for card in self.cards:
            card.draw(screen)


class Game:
    def __init__(self, width, height, screen):
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.screen = screen
        self.board = Board()

    def run(self):
        run = True

        while run:
            pg.time.delay(450)
            self.screen.fill((0, 0, 0)) #wypelnia okno

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            self.draw_board()
            self.update()

    def draw_board(self):
        self.board.draw(self.screen)

    def update(self):
        pg.display.update()

COLORS = {
    'background': (50, 50, 50), # Kolor tła menu (ciemnoszary)
    'button': (100, 200, 100), # Kolor przycisków (zielonkawy)
    'text': (255, 255, 255) # Kolor tekstu (biały)
}

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.game = None
        self.buttons = [
            {'rect': pg.Rect(300, 300, 200, 50), 'text': "Start", 'action': "play"},
            {'rect': pg.Rect(300, 370, 200, 50), 'text': "Exit", 'action': "exit"}
        ]
        self.font = pg.font.SysFont(None, 45)  #czcionka tekstu

    def draw(self):
        self.screen.fill(COLORS['background']) # Wypełnienie tła określonym kolorem
        for button in self.buttons:
            pg.draw.rect(self.screen, COLORS['button'], button['rect']) # Rysowanie przycisku
            text = self.font.render(button['text'], True, COLORS['text'])
            text_rect = text.get_rect(center=button['rect'].center) #Pozycjonuje tekst na środku prostokąta
            self.screen.blit(text, text_rect)
        pg.display.update()
        
    def handle_events(self):
        mouse_pos = pg.mouse.get_pos() # Pobiera aktualną pozycję myszy
        click = False # Flaga oznaczająca kliknięcie
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "exit"
            if event.type == pg.MOUSEBUTTONDOWN:
                click = True

        if click:
            for button in self.buttons:
                if button['rect'].collidepoint(mouse_pos):
                    return button['action']
        return "menu"

    def run(self):
        run = True
        while run:
            action = self.handle_events()
            if action == "exit": #zatrzymuje menu
                run = False
            elif action == "play":
                self.game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen)
                self.game.run()
                run = False         
            self.draw()

        

    

if __name__ == '__main__':
    menu = Menu(screen)
    menu.run()
    #monopoly = Menu(screen)
    #monopoly.run()
    pg.quit()
