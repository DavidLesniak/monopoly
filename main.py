import pygame

SCREEN_WIDTH = 736
SCREEN_HEIGHT = 736

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Monopoly")
bg = pygame.image.load('board.png')

def redrawGameWindow():
    global bg

    screen.blit(bg, (0,0))
    pygame.display.update()

run = True

while run:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    redrawGameWindow()

pygame.quit()
