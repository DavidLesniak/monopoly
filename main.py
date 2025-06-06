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

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            self.draw_board()
            self.update()

    def draw_board(self):
        self.board.draw(self.screen)

    def update(self):
        pg.display.update()


if __name__ == '__main__':
    monopoly = Game(SCREEN_WIDTH, SCREEN_HEIGHT, screen)
    monopoly.run()
    pg.quit()