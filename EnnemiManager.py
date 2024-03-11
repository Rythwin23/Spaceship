import random
import pygame

from Ennemi import Ennemi
from Comete import Comete
import time


class EnnemiManager:
    def __init__(self, res):
        self.res = res
        self.bords = [[-20, self.res[0] + 20],
                      [-20, self.res[1] + 20]]
        self.timer_ennemi = time.time()
        self.delay_ennemi = 2

        self.timer_comete = time.time()
        self.delay_comete = 5

        # groupe d'entités gérés par le manager
        self.ennemi_sprite_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.cometes_group = pygame.sprite.Group()

        # ressources graphiques
        self.bullet_img = pygame.image.load("./assets/bulletmodel.png")
        self.ennemi_spritesheet = pygame.image.load("./assets/spritesheet_model_special_ennemi.png")
        self.ennemi_boss = ((self.ennemi_spritesheet.subsurface(288, 8, 193, 261), 30, 10, 0.3, 10),   #sprite, hp, degats, nb bullet, speed bullet
                            (self.ennemi_spritesheet.subsurface(6, 43, 265, 192), 30, 10, 0.3, 10),
                            (self.ennemi_spritesheet.subsurface(500, 11, 134, 258), 50, 20, 0.45, 10),
                            (self.ennemi_spritesheet.subsurface(473, 379, 144, 170), 75, 20, 0.45, 10),
                            (self.ennemi_spritesheet.subsurface(665, 10, 201, 266), 100, 25, 0.5, 12),
                            (self.ennemi_spritesheet.subsurface(688, 364, 172, 190), 150, 30, 0.5, 13),
                            (self.ennemi_spritesheet.subsurface(688, 577, 180, 266), 200, 40, 0.6, 14),
                            (self.ennemi_spritesheet.subsurface(438, 583, 207, 260), 250, 45, 0.6, 15),
                            (self.ennemi_spritesheet.subsurface(21, 370, 402, 509), 300, 50, 0.7, 15))

        self.model_explosion = pygame.image.load("./assets/explosion_model3.png")

        # cometes
        self.comete_spritesheet = pygame.image.load("./assets/comets.png")
        self.comete_explosion_spritesheet = pygame.image.load("./assets/explosion_model3.png")

    def update(self, player):
        if time.time() - self.timer_ennemi > self.delay_ennemi and len(self.ennemi_sprite_group) < 2:
            self.timer_ennemi = time.time()
            self.spawn_ennemi()

        if time.time() - self.timer_comete > self.delay_comete:
            self.timer_comete = time.time()
            self.spawn_comete()

        for ennemi in self.ennemi_sprite_group:
            for bullet in ennemi.bullet_group:
                if bullet not in self.bullet_group:
                    bullet_copy = bullet
                    self.bullet_group.add(bullet_copy)

        self.clear_ennemi()
        self.clear_cometes()
        self.bullet_group.update()
        self.cometes_group.update()
        for ennemi in self.ennemi_sprite_group:
            ennemi.pre_update(player.pos)

    def spawn_ennemi(self):
        x = random.randint(-20, self.res[0] + 20)
        y = [-20, self.res[1] + 20]
        pos = (x, y[random.randint(0, 1)])
        if pos[0] > 0:
            velocity_x = -1
        else:
            velocity_x = 1
        if pos[1] > 0:
            velocity_y = -1
        else:
            velocity_y = 1
        index_ennemi_model = random.randint(0, 2)  #len(self.ennemi_boss)-1)
        ennemi_model = self.ennemi_boss[index_ennemi_model]  #sprite, hp, degats, taille, speed bullet
        ennemi = Ennemi(self.res, pos, ennemi_model[1], (velocity_x, velocity_y), random.randint(2, 3),
                        pygame.transform.scale_by(ennemi_model[0], ennemi_model[3]), self.bullet_img, ennemi_model[2],
                        ennemi_model[4], self.model_explosion, 256, 256)

        self.ennemi_sprite_group.add(ennemi)

    def spawn_comete(self):
        self.cometes_group.add(Comete(self.res, self.comete_spritesheet, self.comete_explosion_spritesheet))

    def clear_cometes(self):
        for comete in self.cometes_group.sprites():
            if comete.rect.centerx < self.bords[0][0] or comete.rect.centerx > self.bords[0][1]:
                self.cometes_group.remove(comete)
            elif comete.rect.centery < self.bords[1][0] or comete.rect.centery > self.bords[1][1]:
                self.cometes_group.remove(comete)
            if comete not in self.cometes_group.sprites():
                comete.kill()

    def clear_ennemi(self):
        for ennemi in self.ennemi_sprite_group.sprites():
            if ennemi.rect.centerx < self.bords[0][0] or ennemi.rect.centerx > self.bords[0][1]:
                if len(ennemi.bullet_group) == 0:
                    self.ennemi_sprite_group.remove(ennemi)
            elif ennemi.rect.centery < self.bords[1][0] or ennemi.rect.centery > self.bords[1][1]:
                if len(ennemi.bullet_group) == 0:
                    self.ennemi_sprite_group.remove(ennemi)
            if ennemi not in self.ennemi_sprite_group:
                ennemi.kill()
