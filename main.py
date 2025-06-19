import pygame as pg
import random
import os
from card_deck import *
from button import *
from setup import *
from config import *

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


class TextCenter:
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


class Text:
    def __init__(self, text, text_color, tlx, tly, font_size = 36, font_family = None):
        self.text = str(text)
        self.text_color = text_color
        self.font_size = font_size
        self.font_family = font_family
        self.font = pg.font.SysFont(self.font_family, self.font_size)
        self.tlx = tlx
        self.tly = tly
        self.update()

    def update(self):
        self.image = self.font.render(self.text, 1, self.text_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.tlx, self.tly

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
        self.image = image
        self.rect = self.image.get_rect()
        self.name = name
        self.position = 0
        self.destination = 0
        self.moving = False
        self.cash = 3000

    def move(self, steps):
        self.moving = True
        self.destination = (self.position + steps) % 36
        
    def update(self, cards):
        if self.position != self.destination:
            self.position = (self.position+1) % 36
            pg.time.delay(50)

        else:
            self.moving = False

        self.rect.center = cards[self.position].fieldRect.center

    def draw(self, surface):
        surface.blit(self.image, self.rect)

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

        cardInfoRect.topleft = 200, 300
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

        Text('Opłaty: ', 'black', cardInfoBarRect.left+20, cardInfoBarRect.bottom+70, 16).draw(surface)

        for i in range(0,4):
            Text(f'Poziom {i+1}: '+str(self.fee[i])+'$', 'black', cardInfoBarRect.left+20, cardInfoBarRect.bottom+90+(15*i), 16).draw(surface)


    def buy(self, player):
        if self.sticky != None:
            if self.owner == None:
                if player.cash - self.price >= 0:
                    self.owner = player
                    player.cash -= self.price
                    self.field.fill('#c1ff72')
                else:
                    print('Brak wystarczających środków na koncie!')
            else:
                print(f'To pole należy do gracza {self.owner.name}')
        else:
            print('Pole specjalne nie można go kupić!')

    def pay(self, player):
        player.cash -= self.fee[self.updateLevel]
        print(f'Gracz {player.name} płaci {self.fee[self.updateLevel]}$ graczowi {self.owner.name}')


    def update(self, player):
        # Przycisk zakupu
        if self.owner == None and player.moving == False:
            if buyButton.draw(self.screen):
                self.buy(player)
        else:
            buyButtonNoactive.draw(self.screen)



    def draw(self, surface):
        surface.blit(self.border, self.borderRect)
        surface.blit(self.field, self.fieldRect)

        if self.sticky != None:
            surface.blit(self.bar, self.barRect)

        
        
        #TextCenter(self.index, 'black', self.fieldRect.centerx, self.fieldRect.centery, 20).draw(surface)


class CardSpecial(Card):
    def __init__(self):
        pass


class Board:
    def __init__(self):
        self.cards = []
        self.init_board()

    def init_board(self):
        index=0

        for j in range(9):
            if CARDS[index]['type'] == 'property':
                self.cards.append(Card(j*80, 0, index=index, color=CARDS[index]['color'], name=CARDS[index]['name'], sticky='S', price=CARDS[index]['price'], fee=CARDS[index]['fee']))
            else:
                self.cards.append(Card(j*80, 0, index=index, color=CARDS[index]['color'], name=CARDS[index]['name'], sticky=None, price=CARDS[index]['price']))
            index+=1

        for j in range(9):
            if CARDS[index]['type'] == 'property':
                self.cards.append(Card(720, j*80, index=index, color=CARDS[index]['color'], name=CARDS[index]['name'], sticky='W', price=CARDS[index]['price'], fee=CARDS[index]['fee']))
            else:
                self.cards.append(Card(720, j*80, index=index, color=CARDS[index]['color'], name=CARDS[index]['name'], sticky=None, price=CARDS[index]['price']))
            index+=1

        for j in reversed(range(9)):
            if CARDS[index]['type'] == 'property':
                self.cards.append(Card((j*80)+80, 720, index=index, color=CARDS[index]['color'], name=CARDS[index]['name'], sticky='N', price=CARDS[index]['price'], fee=CARDS[index]['fee']))
            else:
                self.cards.append(Card((j*80)+80, 720, index=index, color=CARDS[index]['color'], name=CARDS[index]['name'], sticky=None, price=CARDS[index]['price']))
            index+=1

        for j in reversed(range(9)):
            if CARDS[index]['type'] == 'property':
                self.cards.append(Card(0, (j*80)+80, index=index, color=CARDS[index]['color'], name=CARDS[index]['name'], sticky='E', price=CARDS[index]['price'], fee=CARDS[index]['fee']))
            else:
                self.cards.append(Card(0, (j*80)+80, index=index, color=CARDS[index]['color'], name=CARDS[index]['name'], sticky=None, price=CARDS[index]['price']))
            index+=1

    def draw(self, surface):
        for card in self.cards:
            card.draw(surface)


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



class Game:
    def __init__(self, screen):
        self.screen = screen
        self.dice = Dice()
        self.board = Board()
        self.scoreboard = Scoreboard()
        self.players = [
            Player('Dawid', image=IMAGES['WINDOWS']), 
            Player('Kacper', image=IMAGES['DEBIAN'])
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

            #print(player.name)
            #print('D:'+str(self.players[0].position))
            #print('K: '+str(self.players[1].position))
            # Przycisk zakupu
            #if self.board.cards[player.destination].owner == None and player.moving == False and self.tour == True:
            #    if buyButton.draw(self.screen):
            #        player = self.players[self.current_player_index]
            #
            #        self.board.cards[player.destination].buy(player)
            #else:
            #    buyButtonNoactive.draw(self.screen)

            # Przycisk końca tury
            if tour == True and player.moving == False:
                #card.update(player)

                if endthrowButton.draw(self.screen):
                    # Pdatek
                    if card.owner != player and card.owner != None:
                        card.pay(player)

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

            # Rysotaniwe graczy
            for p in self.players:
                p.update(self.board.cards)
                p.draw(self.screen)
            
            # Rysowanie statystyk graczy
            self.scoreboard.update(self.players)
            self.scoreboard.draw(self.screen)

            # Rysowanie karty na której znajduje się gracz
            card.draw_card_details(self.screen)

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
