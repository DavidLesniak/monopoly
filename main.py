import pygame as pg


pg.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

pg.display.set_caption("Monopoly")
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Game:
    def __init__(self, width, height, screen):
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height

        self.screen = screen

    def run(self):
        run = True

        while run:
            pg.time.delay(450)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            self.update()

    def update(self):
        pg.display.update()


if __name__ == '__main__':
    monopoly = Game(SCREEN_WIDTH, SCREEN_HEIGHT, screen)
    monopoly.run()
    pg.quit()