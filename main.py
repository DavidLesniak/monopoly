import pygame as pg
import random
import os
from card_deck import *
from button import *
from setup import *
from config import *
from dice import Dice
from text import Text, TextCenter
from scoreboard import Scoreboard

pg.init()

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


class Player(pg.sprite.Sprite):
    def __init__(self, name, image=None):
        self.image = image
        self.rect = self.image.get_rect()
        self.name = name
        self.position = 0
        self.destination = 0
        self.moving = False
        self.cash = 3000
        self.animation = False

    def move(self, steps):
        self.moving = True
        self.destination = (self.position + steps) % 36

    def actionAnimation(self, text='', color='black', size=25):
        self.animation = True
        self._animationText = TextCenter(text, color, self.rect.centerx, self.rect.centery, size)

    def update(self, cards):
        if self.position != self.destination:
            self.position = (self.position+1) % 36
            pg.time.delay(50)

        else:
            self.moving = False

        self.rect.center = cards[self.position].fieldRect.center

        if self.animation:
            self._animationText.cy -= 0.7
            self._animationText.update()

            if self._animationText.cy < self.rect.centery-40:
                self.animation = False


    def draw(self, surface):
        surface.blit(self.image, self.rect)

        if self.animation:
            self._animationText.draw(surface)


class Card(pg.sprite.Sprite):
    def __init__(self, tlx, tly, index, color='red', name='', sticky='', price=0, fee=[0,0,0,0]):
        self.index = index
        self.color = color
        self.price = price
        self.fee = fee
        self.updateLevel = 0
        self.owner = None 
        self.name = name
        self.sticky = sticky
        self._padding = 1
        self._borderThickness = 1
        self._barThickness = 15
       
        # Stworzenie obramowania pola
        self.border = pg.Surface((80,80))
        self.border.fill('black')
        self.borderRect = self.border.get_rect()
        self.borderRect.topleft = tlx, tly

        # Stworzenie pola
        self.field = pg.Surface((80-(self._borderThickness*2), 80-(self._borderThickness*2)))
        self.field.fill('#F7F7F7')
        self.fieldRect = self.field.get_rect()
        self.fieldRect.center = self.borderRect.center
        
        # Stworzenie
        self.imageUpgrade = IMAGES['HOUSE0']
        self.imageUpgradeRect = self.imageUpgrade.get_rect()
        self.imageUpgradeRect.center = self.fieldRect.center

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

        cardInfoRect.topleft = 225, 300
        cardInfoBarRect.topleft = cardInfoRect.topleft

        # Umieszczenie nazwy pola
        cardName = TextCenter(self.name, 'black', cardInfoBarRect.centerx, cardInfoBarRect.centery, 20)

        # Umieszczenie szczegółów karty na ekranie
        surface.blit(cardInfo, cardInfoRect)
        surface.blit(cardInfoBar, cardInfoBarRect)

        # Wyświetlenie ceny
        cardInfoPrice = TextCenter(str(self.price)+'$', 'black', cardInfoBarRect.centerx, cardInfoBarRect.bottom+25, 24)

        if self.owner != None:
            cardInforPlayerName = TextCenter('Właściciel: '+str(self.owner.name), 'black', cardInfoBarRect.centerx, cardInfoBarRect.bottom+50, 16)
            cardInforPlayerName.draw(surface)

        cardInfoPrice.draw(surface)
        cardName.draw(surface)

        Text('Opłaty: ', 'black', cardInfoBarRect.left+10, cardInfoBarRect.bottom+70, 16).draw(surface)

        for i in range(0, len(self.fee)):
            if i == self.updateLevel and self.owner != None:
                Text(f'Poziom {i+1}: '+str(self.fee[i])+'$', 'black', cardInfoBarRect.left+10, cardInfoBarRect.bottom+90+(15*i), 16).draw(surface)
            else:
                Text(f'Poziom {i+1}: '+str(self.fee[i])+'$', 'gray', cardInfoBarRect.left+10, cardInfoBarRect.bottom+90+(15*i), 16).draw(surface)

    def buy(self, player):
        if self.sticky != None:
            if self.owner == None:
                if player.cash - self.price >= 0:
                    self.owner = player
                    player.cash -= self.price
                    self.field.fill('#c1ff72')
                    self.update()   
                    player.actionAnimation(f'-{self.price}$', 'red')
                    pg.time.delay(100)
           
                else:
                    player.actionAnimation('Brak środków!', size=20)
            else:
                print(f'To pole należy do gracza {self.owner.name}')
        else:
            print('Pole specjalne nie można go kupić!')

    def pay(self, player):
        player.cash -= self.fee[self.updateLevel]
        self.owner.cash += self.fee[self.updateLevel]
        print(f'Gracz {player.name} płaci {self.fee[self.updateLevel]}$ graczowi {self.owner.name}')

    def upgrade(self, player):
        if self.sticky != None:
            if self.owner == player:
                if self.updateLevel < len(self.fee)-1:
                    if player.cash - 100 >= 0:
                        player.cash -= 100
                        self.updateLevel += 1
                        self.update()
                        player.actionAnimation(f'-100$', 'red')
                    else:
                        player.actionAnimation('Brak środków!', size=20)
                else:
                    print('Osiągnięto maksymalny posiom ulepszeń!')
            else:
                print(f'To pole należy do gracza {self.owner.name}')
        else:
            print('Pole specjalne nie można go ulepszyć!')

    def update(self):
        self.imageUpgrade = IMAGES['HOUSE'+str(self.updateLevel+1)]
        self.imageUpgradeRect = self.imageUpgrade.get_rect()
        self.imageUpgradeRect.center = self.fieldRect.center

    def draw(self, surface):
        surface.blit(self.border, self.borderRect)
        surface.blit(self.field, self.fieldRect)
        surface.blit(self.imageUpgrade, self.imageUpgradeRect)

        if self.sticky != None:
            surface.blit(self.bar, self.barRect)
    

class CardSpecial(Card):
    def __init__(self):
        pass


class Board:
    def __init__(self):
        self.cards = []
        self.init_board()

    def init_board(self):
        index=0
        sticky = ['S', 'W', 'N', 'E']
        xy = [((x*80, 0) for x in range(9)), ((720, y*80) for y in range(9)), (((x*80)+80, 720) for x in reversed(range(9))), ((0,(y*80)+80) for y in reversed(range(9)))]
        
        for _ in range(36):
            x = _ // 9
            print(x)
            tlx, tly = next(xy[x])

            if CARDS[_]['type'] == 'property':
                self.cards.append(Card(tlx, tly, index=_, color=CARDS[_]['color'], name=CARDS[_]['name'], sticky=sticky[x], price=CARDS[_]['price'], fee=CARDS[_]['fee']))
            else:
                self.cards.append(Card(tlx, tly, index=_, color=CARDS[_]['color'], name=CARDS[_]['name'], sticky=None, price=CARDS[_]['price']))

    def draw(self, surface):
        for card in self.cards:
            card.draw(surface)

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.dice = Dice()
        self.board = Board()
        self.scoreboard = Scoreboard()
        self.players = [
            Player('Dawid', image=IMAGES['WINDOWS']), 
            Player('Kacper', image=IMAGES['DEBIAN']),
            Player('Tomek', image=IMAGES['REDHAT']),
            Player('Marcin', image=IMAGES['CENTOS'])
        ]

        self.init_players()

    def init_players(self):
        for player in self.players:
            player.move(0)
            player.update(self.board.cards)

    def run(self):
        run = True
        tour_index = 0
        tour = False
        player = self.players[tour_index]
        card = self.board.cards[0]

        while run:
            self.screen.fill('#808080')

            card = self.board.cards[player.position]

            # Przycisk rzutu kościom
            if tour == False:
                if throwButton.draw(self.screen):
                    tour = True
                    self.dice.roll()
                    player.move(self.dice.total)
            else:
                throwButtonNoactive.draw(self.screen)

            # Przycisk ulepszenia
            if card.owner == player and player.moving == False and tour == True:
                if card.updateLevel < len(card.fee)-1:
                    if upgradeButton.draw(self.screen):
                        card.upgrade(player)

            # Przycisk zakupu
            if card.owner == None and player.moving == False and tour == True:
                if buyButton.draw(self.screen):
                    card.buy(player)
                        
            # Przycisk końca tury
            if tour == True and player.moving == False:
                if endthrowButton.draw(self.screen):

                    # Pdatek
                    if card.owner != player and card.owner != None:
                        card.pay(player)
                        player.actionAnimation(f'-{card.fee[card.updateLevel]}$', 'red')    # @property
                        card.owner.actionAnimation(f'+{card.fee[card.updateLevel]}$', 'darkgreen') 

                    tour = False
                    tour_index = (tour_index+1) % len(self.players)
                    player = self.players[tour_index]

            else:
                endthrowButtonNoactive.draw(self.screen)
            
            # Wyłączanie gry
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False                        
                        
            # Rysowanie planszy
            self.board.draw(self.screen)

            # Rysowanie graczy
            for p in self.players:
                p.update(self.board.cards)
                p.draw(self.screen)
            
            # Rysowanie statystyk graczy
            self.scoreboard.update(self.players)
            self.scoreboard.draw(self.screen)

            # Rysowanie karty na której znajduje się gracz
            card.draw_card_details(self.screen)

            # Odświeżenie obrazu
            pg.display.update()
            clock.tick(60)

    

if __name__ == '__main__':

    run = True
    while run:
        screen.fill((202, 228, 241))
        if start_button.draw(screen):
            game = Game(screen)
            game.run()
            run = False
        if setup_button.draw(screen):
            setup = Setup()
        if exit_button.draw(screen):
            run = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        pg.display.update()
    pg.quit()
