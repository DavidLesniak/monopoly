import pygame as pg
from config import *
from logo import *

class End:
    def draw_end(self, screen, color, rect_width, rect_height, width, border_radius):
        self.screen = screen
        self.color = color
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.width = width
        self.border_radius = border_radius
        shadow_offset = 8
        black = (0, 0, 0)
        dark_gray = (100, 100, 100)
        # Cień pod prostokątem
        rect_x = CREEN_WIDTH // 2 - rect_width // 2
        rect_y = SCREEN_HEIGHT // 2 - rect_height // 2
        shadow_rect = pg.Rect(rect_x + shadow_offset, rect_y + shadow_offset, rect_width, rect_height)
        pg.draw.rect(screen, dark_gray, shadow_rect, width=0, border_radius=border_radius+8)
        # Główny prostokąt
        rect = pg.Rect(rect_x, rect_y, rect_width, rect_height)
        pg.draw.rect(screen, color, rect, width=0, border_radius=border_radius)
        # Ramka
        pg.draw.rect(screen, black, rect, width=4, border_radius=border_radius)
        return rect

    def draw_text(self, screen, text, font, color, x, y):
        self.screen = screen
        self.text = text
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)
        return text_rect

    def run(self, score):
        screen = pg.display.set_mode((CREEN_WIDTH, SCREEN_HEIGHT))
        running = True
        while running:
            screen.fill((202, 228, 241))
            screen.blit(logo, get_logo_rect(screen))
            color = (189, 236, 182)
            heading_color = (0, 0, 0)
            font_heading = pg.font.SysFont("arial", 44, bold=True)
            font_score = pg.font.SysFont("arial", 32, bold=False)
            
            table_end = self.draw_end(screen, color, 400, 400, 1, 20)
            self.draw_text(screen, "Wynik graczy:", font_heading, heading_color, table_end.centerx, table_end.top + 30)

            for i, player in enumerate(score):
                text = f"{i+1}. {player['name']} : {player['cash']} $"
                self.draw_text(screen, text, font_score, heading_color, table_end.centerx, table_end.top + 80 + i*40)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            pg.display.update()
        pg.quit()
