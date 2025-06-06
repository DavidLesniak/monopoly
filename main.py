import pygame as pg
import random


pg.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FONT = pg.font.SysFont(None, 24)

pg.display.set_caption("Monopoly")
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Player:
    def __init__(self, name, color):
        self.position = 0
        self.rect = pg.Rect(0, 0, 20, 20)
        self.name = name
        self.color = color

    def move(self, steps, cards):
        self.position = (self.position + steps) % len(cards)

        card = cards[self.position]

        center_x = card.x+card.width // 2
        center_y = card.y+card.height // 2
        self.rect.center = (center_x, center_y)

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)


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
                for j in range(9):
                    self.cards.append(Card(j*80, 0, o))
                    o+=1

            if i==1:
                for j in range(9):
                    self.cards.append(Card(720, j*80, o))
                    o+=1

            if i==2:
                for j in reversed(range(9)):
                    self.cards.append(Card((j*80)+80, 720, o))
                    o+=1

            if i==3:
                for j in reversed(range(9)):
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

        self.players = [Player('Dawid', 'green'), Player('Kacper', 'blue')]
        self.init_players()

        self.current_player_index = 0

    def init_players(self):
        for player in self.players:
            player.move(0, self.board.cards)

    def run(self):
        run = True

        while run:
            pg.time.delay(50)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.check_queue()
                        
            self.draw_board()   # Rysowanie planszy
            self.draw_interface()
            self.draw_players() # Rysowanie gracyz
            self.update()       # Aktualizacja

    def check_queue(self):
        player = self.players[self.current_player_index]
        player.move(random.randint(1, 6), self.board.cards)

        # Zmiana tury gracza
        self.current_player_index = (self.current_player_index+1) % len(self.players)

    def draw_board(self):
        self.board.draw(self.screen)

    def draw_interface(self):
        pg.draw.rect(self.screen, (120, 200, 80), (80, 80, 640, 100))
        tour = FONT.render('Tura: '+self.players[self.current_player_index].name, True, (0, 0, 0))
        screen.blit(tour, (90, 90))


    def draw_players(self):
        for player in self.players:
            player.draw(self.screen)

    def update(self):
        pg.display.update()


if __name__ == '__main__':
    monopoly = Game(SCREEN_WIDTH, SCREEN_HEIGHT, screen)
    monopoly.run()
    pg.quit()