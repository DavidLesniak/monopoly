import pygame

pygame.init()

screen = pygame.display.set_mode((750, 750))
pygame.display.set_caption("Monopoly")

run = True

while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
