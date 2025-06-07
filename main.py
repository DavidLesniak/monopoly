import pygame as pg
import random
import os


pg.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FONT = pg.font.SysFont(None, 24)

pg.display.set_caption("Monopoly")
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

path = os.path.join(os.getcwd(), 'images')
file_names = os.listdir(path)
IMAGES = {}
for file_name in file_names:
    image_name = file_name[:-4].upper()
    IMAGES[image_name] = pg.image.load(os.path.join(path, file_name)).convert_alpha()


class Player(pg.sprite.Sprite):
    def __init__(self, name, image=None):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = 0, 0
        self.name = name
        self.position = 0

    def move(self, steps, cards):
        self.position = (self.position + steps) % len(cards)
        self.rect.center = cards[self.position].rect.center

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Card(pg.sprite.Sprite):
    def __init__(self, tlx, tly, index, image=None):
        super().__init__()
        #self.rect = self.image.get_rect()
        self.rect = pg.Rect(0, 0, 80, 80)
        self.rect.topleft = tlx, tly
        self.index = index
        
    def draw(self, surface):
        pg.draw.rect(screen, (247, 247, 247), self.rect)
        index = FONT.render(str(self.index), True, (0, 0, 0))
        screen.blit(index, self.rect.center)


class Board:
    def __init__(self):
        self.cards = []
        self.init_board()

    def init_board(self):
        index=0

        for j in range(9):
            self.cards.append(Card(j*80, 0, index))
            index+=1

        for j in range(9):
            self.cards.append(Card(720, j*80, index))
            index+=1

        for j in reversed(range(9)):
            self.cards.append(Card((j*80)+80, 720, index))
            index+=1

        for j in reversed(range(9)):
            self.cards.append(Card(0, (j*80)+80, index))
            index+=1

    def draw(self, surface):
        for card in self.cards:
            card.draw(surface)

class Game:
    def __init__(self, width, height, screen):
        self.widht = width
        self.height = height
        self.screen = screen

        self.board = Board()

        self.players = [Player('Dawid', image=IMAGES['WINDOWS']), Player('Kacper', image=IMAGES['DEBIAN'])]
        self.init_players()

        self.current_player_index = 0

    def init_players(self):
        for player in self.players:
            player.move(0, self.board.cards)
            player.update()

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
            #self.draw_interface()
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
        # Licznik tura
        pg.draw.rect(self.screen, (120, 200, 80), (80, 80, 640, 30))
        tour = FONT.render('Tura: '+self.players[self.current_player_index].name, True, (0, 0, 0))
        self.screen.blit(tour, (90, 90))

        # Licznik pieniądze
        pg.draw.rect(self.screen, 'lightblue', (80, 110, 640, 60))
        for i, player in enumerate(self.players):
            cash_value = FONT.render(player.name+': '+str(player.cash)+'$', True, (0, 0, 0))
            self.screen.blit(cash_value, (90, 90+((i+1)*30)))

    def draw_players(self):
        for player in self.players:
            player.draw(self.screen)

    def update(self):
        pg.display.update()


if __name__ == '__main__':
    monopoly = Game(SCREEN_WIDTH, SCREEN_HEIGHT, screen)
    monopoly.run()
    pg.quit()
