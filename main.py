import pygame as pg
import random
import os
from card_deck import *

pg.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FONT = pg.font.SysFont(None, 24)

pg.display.set_caption('Monopoly')
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()

path = os.path.join(os.getcwd(), 'images')
file_names = os.listdir(path)
IMAGES = {}
for file_name in file_names:
    image_name = file_name[:-4].upper()
    IMAGES[image_name] = pg.image.load(os.path.join(path, file_name)).convert_alpha()


class Text:
    def __init__(self, text, text_color, cx, cy, font_size = 36, font_family = None):
        self.text = str(text)
        self.text_color = text_color
        self.font_size = font_size
        self.font_family = font_family
        self.font = pg.font.SysFont(self.font_family, self.font_size)
        self.cx = cx
        self.cy = cy
        self.update()

    def update(self):
        self.image = self.font.render(self.text, 1, self.text_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.cx, self.cy

    def draw(self, surface):
        surface.blit(self.image, self.rect)



class Dice:
    def __init__(self):
        self.dice1 = 0
        self.dice2 = 0

    def roll(self):
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        
    @property
    def total(self):
        return self.dice1 + self.dice2

    @property
    def is_dubel(self):
        return self.dice1 == self.dice2



class Player(pg.sprite.Sprite):
    def __init__(self, name, image=None):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.name = name
        self.position = 0
        self.cash = 3000

    def move(self, steps, cards):
        self.position = (self.position + steps) % len(cards)
        self.rect.center = cards[self.position].fieldRect.center

    def draw(self, surface):
        surface.blit(self.image, self.rect)



class Card(pg.sprite.Sprite):
    def __init__(self, tlx, tly, index, color='red', sticky=False, price=0):
        super().__init__()
        self.owner = None
        self.index = index
        self.price = price
        self.color = color
        self.sticky = sticky
        self._padding = 1
        self._barThickness = 15
        self._borderThickness = 1

        # Stworzenie obramowania pola
        self.border = pg.Surface((80,80))
        self.borderRect = self.border.get_rect()
        self.borderRect.topleft = tlx, tly

        # Stworzenie pola
        self.field = pg.Surface((80-(self._borderThickness*2), 80-(self._borderThickness*2)))
        self.field.fill('#F7F7F7')
        self.fieldRect = self.field.get_rect()
        self.fieldRect.center = self.borderRect.center
        
        # Stworzenie kolorowej belki
        self.bar = pg.Surface((80-(self._padding*2), self._barThickness))
        self.bar.fill(self.color)

        # Odwrocenie i wyrownanie belki w zaleznosci od orientacji
        if sticky in ['E', 'W']:
            self.bar = pg.transform.rotate(self.bar, 90)

        self.barRect = self.bar.get_rect()
        
        if sticky:
            if sticky == 'N':
                self.barRect.topleft = self.fieldRect.topleft
            if sticky == 'E':
                self.barRect.topright = self.fieldRect.topright
            if sticky == 'S':
                self.barRect.bottomleft = self.fieldRect.bottomleft
            if sticky == 'W':
                self.barRect.topleft = self.fieldRect.topleft

    def draw_card_details(self, surface):
        # Stworzenie karty
        cardInfo = pg.Surface((140, 210))
        cardInfo.fill('#F7F7F7')
        cardInfoRect = cardInfo.get_rect()

        # Stworzenie kolorowej belki
        cardInfoBar = pg.Surface((140, 40))
        cardInfoBar.fill(self.color)
        cardInfoBarRect = cardInfoBar.get_rect()

        cardInfoRect.center = 300, 400
        cardInfoBarRect.topleft = cardInfoRect.topleft

        # Umieszczenie widgetow na ekranie
        surface.blit(cardInfo, cardInfoRect)
        surface.blit(cardInfoBar, cardInfoBarRect)

        # Wyświetlenie ceny
        cardInfoPrice = Text(str(self.price)+'$', 'black', cardInfoBarRect.centerx, cardInfoBarRect.bottom+15, 24)

        if self.owner != None:
            cardInforPlayerName = Text('Właściciel: '+str(self.owner.name), 'black', cardInfoBarRect.centerx, cardInfoBarRect.bottom+35, 16)
            cardInforPlayerName.draw(surface)

        cardInfoPrice.draw(surface)


        # Menu akcji
        buttonBuy = pg.Surface((140, 40))
        buttonBuy.fill('#F7F7F7')
        buttonBuyRect = buttonBuy.get_rect()
        buttonBuyRect.top = cardInfoRect.top
        buttonBuyRect.left = cardInfoRect.right+40

        buttonBuyText = Text("Kup", 'black', buttonBuyRect.centerx, buttonBuyRect.centery, 20)

        surface.blit(buttonBuy, buttonBuyRect)
        buttonBuyText.draw(surface)


        buttonUpgrade = pg.Surface((140, 40))
        buttonUpgrade.fill('#F7F7F7')
        buttonUpgradeRect = buttonUpgrade.get_rect()
        buttonUpgradeRect.top = buttonBuyRect.bottom+20
        buttonUpgradeRect.left = cardInfoRect.right+40

        buttonUpgradeText = Text("Ulepsz", 'black', buttonUpgradeRect.centerx, buttonUpgradeRect.centery, 20)

        surface.blit(buttonUpgrade, buttonUpgradeRect)
        buttonUpgradeText.draw(surface)

    def buy(self, player):
        self.owner = player
        self.field.fill('#c1ff72')

    def draw(self, surface):
        surface.blit(self.field, self.fieldRect)

        if self.sticky != None:
            surface.blit(self.bar, self.barRect)
        
        Text(self.index, 'black', self.fieldRect.centerx, self.fieldRect.centery, 20).draw(surface)

    def __str__(self):
        return f'\n({self.index})------------------\n | Właściciel: {self.owner}\n | Koszt: 300$'



class Board:
    def __init__(self):
        self.cards = []
        self.init_board()

    def init_board(self):
        index=0

        for j in range(9):
            if CARDS[index]['special'] == False:
                self.cards.append(Card(j*80, 0, index=index, color=CARDS[index]['color'], sticky='S', price=CARDS[index]['price']))
            else:
                self.cards.append(Card(j*80, 0, index=index, color=CARDS[index]['color'], sticky=None, price=CARDS[index]['price']))
            index+=1

        for j in range(9):
            if CARDS[index]['special'] == False:
                self.cards.append(Card(720, j*80, index=index, color=CARDS[index]['color'], sticky='W', price=CARDS[index]['price']))
            else:
                self.cards.append(Card(720, j*80, index=index, color=CARDS[index]['color'], sticky=None, price=CARDS[index]['price']))
            index+=1

        for j in reversed(range(9)):
            if CARDS[index]['special'] == False:
                self.cards.append(Card((j*80)+80, 720, index=index, color=CARDS[index]['color'], sticky='N', price=CARDS[index]['price']))
            else:
                self.cards.append(Card((j*80)+80, 720, index=index, color=CARDS[index]['color'], sticky=None, price=CARDS[index]['price']))
            index+=1

        for j in reversed(range(9)):
            if CARDS[index]['special'] == False:
                self.cards.append(Card(0, (j*80)+80, index=index, color=CARDS[index]['color'], sticky='E', price=CARDS[index]['price']))
            else:
                self.cards.append(Card(0, (j*80)+80, index=index, color=CARDS[index]['color'], sticky=None, price=CARDS[index]['price']))
            index+=1

    def draw(self, surface):
        for card in self.cards:
            card.draw(surface)



class Game:
    def __init__(self, screen):
        self.screen = screen
        self.dice = Dice()
        self.board = Board()
        self.players = [
            Player('Dawid', image=IMAGES['WINDOWS']), 
            Player('Kacper', image=IMAGES['DEBIAN'])
        ]
        self.current_player_index = 0

        self.init_players()
        self.draw_board()
        self.draw_players()
        self.update()

    def init_players(self):
        for player in self.players:
            player.move(0, self.board.cards)

    def run(self):
        run = True

        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.screen.fill((0,0,0))
                        self.tour()
                        self.draw_board()
                        self.draw_players()
                        self.update()

            clock.tick(60)

    def tour(self):
        # Przemieszczenie gracza
        player = self.players[self.current_player_index]

        textPlayerName = Text(player.name, 'white', 400, 200, 49)
        textPlayerName.draw(self.screen)

        self.dice.roll()
        
        player.move(self.dice.total, self.board.cards)

        self.board.cards[player.position].draw_card_details(self.screen)
        if self.board.cards[player.position].owner == None:
            self.board.cards[player.position].buy(player)

        self.current_player_index = (self.current_player_index+1) %len(self.players)

    def draw_board(self):
        self.board.draw(self.screen)

    def draw_players(self):
        for player in self.players:
            player.draw(self.screen)

    def update(self):
        pg.display.update()


if __name__ == '__main__':
    monopoly = Game(screen)
    monopoly.run()
    pg.quit()
