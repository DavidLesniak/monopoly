import pygame as pg
import random
import os
from card_deck import *
from button import *
from setup import *

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
        self.cash = 3000

    def move(self, steps):
        self.destination = (self.position + steps) % 36
        
    def update(self, cards):
        if self.position != self.destination:
            self.position = (self.position+1) % 36
            pg.time.delay(200)

        self.rect.center = cards[self.position].fieldRect.center
            

    def draw(self, surface):
        surface.blit(self.image, self.rect)



class Card(pg.sprite.Sprite):
    def __init__(self, tlx, tly, index, color='red', name='', sticky=False, price=0):
        self.index = index
        self.color = color
        self.price = price
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

        cardInfoRect.center = 300, 400
        cardInfoBarRect.topleft = cardInfoRect.topleft

        # Umieszczenie nazwy pola
        cardName = TextCenter(self.name, 'black', cardInfoBarRect.centerx, cardInfoBarRect.centery, 20)

        # Umieszczenie szczegółów karty na ekranie
        surface.blit(cardInfo, cardInfoRect)
        surface.blit(cardInfoBar, cardInfoBarRect)

        # Wyświetlenie ceny
        cardInfoPrice = TextCenter(str(self.price)+'$', 'black', cardInfoBarRect.centerx, cardInfoBarRect.bottom+15, 24)

        if self.owner != None:
            cardInforPlayerName = TextCenter('Właściciel: '+str(self.owner.name), 'black', cardInfoBarRect.centerx, cardInfoBarRect.bottom+35, 16)
            cardInforPlayerName.draw(surface)

        cardInfoPrice.draw(surface)
        cardName.draw(surface)


        # Menu akcji
        buttonBuy = pg.Surface((140, 40))
        buttonBuy.fill('#F7F7F7')
        buttonBuyRect = buttonBuy.get_rect()
        buttonBuyRect.top = cardInfoRect.top
        buttonBuyRect.left = cardInfoRect.right+40

        buttonBuyText = TextCenter("Kup", 'black', buttonBuyRect.centerx, buttonBuyRect.centery, 20)

        surface.blit(buttonBuy, buttonBuyRect)
        buttonBuyText.draw(surface)


        buttonUpgrade = pg.Surface((140, 40))
        buttonUpgrade.fill('#F7F7F7')
        buttonUpgradeRect = buttonUpgrade.get_rect()
        buttonUpgradeRect.top = buttonBuyRect.bottom+20
        buttonUpgradeRect.left = cardInfoRect.right+40

        buttonUpgradeText = TextCenter("Ulepsz", 'black', buttonUpgradeRect.centerx, buttonUpgradeRect.centery, 20)

        surface.blit(buttonUpgrade, buttonUpgradeRect)
        buttonUpgradeText.draw(surface)

    def buy(self, player):
        self.owner = player
        self.field.fill('#c1ff72')

    def draw(self, surface):
        surface.blit(self.border, self.borderRect)
        surface.blit(self.field, self.fieldRect)

        if self.sticky != None:
            surface.blit(self.bar, self.barRect)
        
        #TextCenter(self.index, 'black', self.fieldRect.centerx, self.fieldRect.centery, 20).draw(surface)

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
                self.cards.append(Card(j*80, 0, index=index, color=CARDS[index]['color'], name=CARDS[index]['name'], sticky='S', price=CARDS[index]['price']))
            else:
                self.cards.append(Card(j*80, 0, index=index, color=CARDS[index]['color'], name=CARDS[index]['name'], sticky=None, price=CARDS[index]['price']))
            index+=1

        for j in range(9):
            if CARDS[index]['special'] == False:
                self.cards.append(Card(720, j*80, index=index, color=CARDS[index]['color'], name=CARDS[index]['name'], sticky='W', price=CARDS[index]['price']))
            else:
                self.cards.append(Card(720, j*80, index=index, color=CARDS[index]['color'], name=CARDS[index]['name'], sticky=None, price=CARDS[index]['price']))
            index+=1

        for j in reversed(range(9)):
            if CARDS[index]['special'] == False:
                self.cards.append(Card((j*80)+80, 720, index=index, color=CARDS[index]['color'], name=CARDS[index]['name'], sticky='N', price=CARDS[index]['price']))
            else:
                self.cards.append(Card((j*80)+80, 720, index=index, color=CARDS[index]['color'], name=CARDS[index]['name'], sticky=None, price=CARDS[index]['price']))
            index+=1

        for j in reversed(range(9)):
            if CARDS[index]['special'] == False:
                self.cards.append(Card(0, (j*80)+80, index=index, color=CARDS[index]['color'], name=CARDS[index]['name'], sticky='E', price=CARDS[index]['price']))
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
        self.current_player_index = -1
        self.playerTourText = TextCenter('Tura gracza: '+self.players[0].name, 'black', 400, 120, 30)
        self.playerCashText = [TextCenter(player.name+': '+str(player.cash)+'$', 'black', 200, 150+(25*i), 25) for i, player in enumerate(self.players)]


        self.init_players()
        #self.draw_board()
        #self.draw_players()
        #self.gui.draw(self.screen)
       # self.update()

    def init_players(self):
        for player in self.players:
            player.move(0)
            player.update(self.board.cards)

    def run(self):
        run = True

        while run:
            self.screen.fill('#000000')

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.current_player_index = (self.current_player_index+1) % len(self.players)
                        self.playerTourText.text = 'Rzuca gracz: '+self.players[self.current_player_index].name
                        player = self.players[self.current_player_index]
                        self.dice.roll()
                        player.move(self.dice.total)

                    if event.key == pg.K_b:
                        if self.board.cards[self.current_player_index].owner == None:
                            self.board.cards[self.players[self.current_player_index].destination].buy(self.players[self.current_player_index])

                            if self.board.cards[self.current_player_index].owner == None:
                                self.players[self.current_player_index].cash -= self.board.cards[self.players[self.current_player_index].destination].price
                                self.playerCashText = [TextCenter(player.name+': '+str(player.cash)+'$', 'black', 200, 150+(25*i), 25) for i, player in enumerate(self.players)]
                            print(self.players[self.current_player_index].cash)
                        
                        


            # Rysowanie planszy
            self.board.draw(self.screen)
            #self.board.cards[self.players[self.current_player_index].position].draw_card_details(self.screen)

            # Rysotaniwe graczy
            for player in self.players:
                player.update(self.board.cards)
                player.draw(self.screen)
            
            # Rysowanie komunikatu
            #self.playerTourText.update()
            #self.playerTourText.draw(self.screen)

            # Rysowanie stanu konta
            #for text in self.playerCashText:
            #    text.update()
            #    text.draw(self.screen)
            self.scoreboard.update(self.players)
            self.scoreboard.draw(self.screen)
            pg.display.update()
            clock.tick(60)

    def draw_board(self):
        self.board.draw(self.screen)

    def draw_players(self):
        for player in self.players:
            player.draw(self.screen)

    def update(self):
        pg.display.update()
    

if __name__ == '__main__':
    start_button = Button(start_x, start_y, start_img, start_hover_img, 1)
    setup_button = Button(setup_x, setup_y, setup_img, setup_hover_img, 1)
    exit_button = Button(exit_x, exit_y, exit_img, exit_hover_img, 1)

    run = True
    while run:
        screen.fill((202, 228, 241))
        if start_button.draw(screen):
            game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, screen)
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
