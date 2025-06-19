import pygame as pg
from text import Text

class Scoreboard:
    def __init__(self):
        self.playerStats = pg.Surface((638, 116))
        self.playerStats.fill('lightblue')
        self.playerStatsRect = self.playerStats.get_rect()
        self.playerStatsRect.topleft = (81, 81)
    
    def update(self, players):
        self.textNames = []

        for i, player in enumerate(players):
            self.textNames.append(Text(player.name+': '+str(player.cash)+'$', 'black', self.playerStatsRect.left+10, self.playerStatsRect.top+(25*i)+5, 22))

    def draw(self, surface):
        surface.blit(self.playerStats, self.playerStatsRect)

        for name in self.textNames:
            name.draw(surface)