import pygame as pg
class Setup:
    def __init__(self):
        self.run()

    def run(self):
        screen = pg.display.get_surface()
        run = True
        while run:
            screen.fill((202, 228, 241))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    run = False
            pg.display.update()
