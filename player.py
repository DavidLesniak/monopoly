import pygame as pg
from text import Text, TextCenter

pg.mixer.init()


class Player(pg.sprite.Sprite):
    sound_effect = pg.mixer.Sound("soundtracks\\retro-coin-4-236671.mp3")
    sound_effect_police = pg.mixer.Sound("soundtracks\\police-intro-sfx-323774.mp3")

    def __init__(self, name, image=None):
        self.image = image
        self.rect = self.image.get_rect()
        self.name = name
        self.position = 0
        self.destination = 0
        self.moving = False
        self.cash = 3000
        self.animation = False
        self._animationTextGroup = []
        self.jail = 0


    def move(self, steps):
        # Sprawdzenie czy gracz jest w więzieniu
        if self.jail > 0:
            self.jail -= 1
        else:
            self.moving = True
            self.destination = (self.position + steps) % 36

    def actionAnimation(self, text='', color='black', size=25):
        self.animation = True
        self._animationTextGroup.append(TextCenter(text, color, self.rect.centerx, self.rect.centery, size))

    def update(self, cards):
        # Aktualizacaj pozycji jeśli gracz nie dotarł na wyznaczone pole
        if self.position != self.destination:
            Player.sound_effect.play()

            # Dodanie wpłaty na konto po przejściu przez start
            if self.position == 0 and self.position != self.destination:
                self.actionAnimation('+400$', 'green', 30)
                self.cash += 400

            self.position = (self.position+1) % 36
            pg.time.delay(100)

        else:
            self.moving = False

        # Przeniesienia gracza do więzienia jesli staną na odpowienim polu
        if self.destination == 27 and self.moving == False:
                self.position = 9
                self.destination = 9
                self.jail = 1
                Player.sound_effect_police.play()

        self.rect.center = cards[self.position].fieldRect.center

        if self.animation:
            for textObject in self._animationTextGroup:
                if self.moving:
                    textObject.cx = self.rect.centerx
                    textObject.cy = self.rect.centery
                textObject.cy -= 0.7
                textObject.update()

                if textObject.cy < self.rect.centery-40:
                    self._animationTextGroup.remove(textObject)
                    
        if len(self._animationTextGroup) == 0:
            animation = False


    def draw(self, surface):
        surface.blit(self.image, self.rect)

        if self.animation:
            for animation in self._animationTextGroup:
                animation.draw(surface)