import pygame as pg

logo_original = pg.image.load("grafika/logo.png")
value = 0.36
logo = pg.transform.scale(logo_original, (int(logo_original.get_width() * value), int(logo_original.get_height() * value)))

def get_logo_rect(screen):
    rect = logo.get_rect()
    rect.centerx = screen.get_width() // 2
    rect.centery = 120
    return rect
