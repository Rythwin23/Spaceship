import math
import time

import pygame
import random
from Planer import Plane


class Player(Plane):
    def __init__(self, res, pos):

        self.all_models = model_futuristes()
        self.all_bullets_models = bullet_futuristes()
        self.player_explosion_spritesheet = pygame.image.load("./assets/explosion_model3.png")
        self.current_model = self.all_models[0]
        self.bullet_model = self.all_bullets_models[random.randint(1, 9)]
        self.bullets_pos = [[(0, 0)],
                      [(-32, 0), (32, 0)],
                      [(45, 0), (-45, 0)],
                      [(60, 0), (0, 20), (-60, 0)],
                      [(50, 0), (0, -25), (-50, 0)],
                      [(55, 0), (0, -20), (-55, 0)],
                      [(54, 0), (30, -20), (-30, -20), (-54, 0)],
                      [(60, -50), (20, 0), (-20, 0), (-60, -50)]]

        self.niveau = 0
        self.total_score = 0
        self.current_score = 0
        self.total_damage = 5
        self.delay_time_fire = 0.9

        Plane.__init__(self, res, pos, 50, self.delay_time_fire, self.current_model, self.bullet_model, 5,
                       10, self.player_explosion_spritesheet, 256, 256)

        # self.angle_speed = 4   #rotation clavier

    def increase_level(self, score):
        self.current_score += score
        self.total_score += score
        if self.current_score > 4:
            self.current_score = 0
            if self.niveau < 7:
                self.niveau += 1
                self.total_damage += 5
                self.health_point_origin += 20
                self.health_point = self.health_point_origin + 20

                self.image = self.all_models[self.niveau]  # on charge le model de plane suivant
                self.image_origin = self.image  # on change l'image d'origine avec le changement de model
                self.mask_origin = pygame.mask.from_surface(self.image_origin)  # changer le mask d'origine

                # self.current_bullet = pygame.image.load("./assets/bullet_player.png")  # self.load_bullet_model()
                self.bullet_img = self.all_bullets_models[random.randint(1, 9)]  # pour l'instant on utilise qu'un seul model de bullet
                self.bullet_damage = self.total_damage / len(self.bullets_pos[self.niveau])
                self.bullet_speed += 0.5
                self.delay_time_fire = max(self.delay_time_fire - 0.05, 0)
                self.duration_fire_off = self.delay_time_fire

                print("nb de tire :", len(self.bullets_pos[self.niveau]), "dégat :", self.bullet_damage, "total :",
                      self.bullet_damage * len(self.bullets_pos[self.niveau]))
                print(self.health_point)

    def move(self, x, y):
        # delta_rotation = x * self.angle_speed    #rotation clavier
        # self.rotation -= delta_rotation          #rotation clavier
        vec = pygame.math.Vector2(0, 1)
        vec.x = x * 0.6
        vec.y = y * 0.6
        if x == 0 and y == 0:
            if self.speed[0] < -0.5:
                self.speed = (self.speed[0] + 0.06, self.speed[1])
            elif self.speed[0] > 0.5:
                self.speed = (self.speed[0] - 0.06, self.speed[1])
            else:
                self.speed = (0, self.speed[1])
            if self.speed[1] < -0.5:
                self.speed = (self.speed[0], self.speed[1] + 0.06)
            elif self.speed[1] > 0.5:
                self.speed = (self.speed[0], self.speed[1] - 0.06)
            else:
                self.speed = (self.speed[0], 0)
        else:
            self.speed += vec * 0.5
            self.speed = (min(max(-5, self.speed[0]), 5), min(max(-5, self.speed[1]), 5))
            # vec.rotate_ip(-self.rotation)     #rotation clavier
        self.pos = (self.pos[0] + vec.x + self.speed[0], self.pos[1] + vec.y + self.speed[1])

    def load_plane_model(self):
        pass

    def load_bullet_model(self):
        pass

    def prefire(self):
        if time.time() - self.timer_fire > self.duration_fire_off:
            self.timer_fire = time.time()
            for i in range(0, len(self.bullets_pos[self.niveau])):
                bullet_pos = (self.pos[0] - self.bullets_pos[self.niveau][i][0]/3,
                              self.pos[1] - self.bullets_pos[self.niveau][i][1]/3)
                self.fire(self.pos, bullet_pos, self.bullet_damage)

    def health_barre(self):
        percent = (200 * self.health_point) / self.health_point_origin
        return [30, 30, percent, 5]


def model_pixels():
    img = pygame.image.load("./assets/planes_models_pixelart.png")
    models = []
    for y in range(0, img.get_height() - 134, 134):
        models.append(pygame.transform.scale_by(img.subsurface(0, y, 151, 134), 0.7))
    return models


def model_classiques():
    img = pygame.image.load("./assets/plane_models_classique.png")
    models = []
    for y in range(0, img.get_height() - 134, 134):
        models.append(pygame.transform.scale_by(img.subsurface(0, y, 151, 134), 0.7))
    return models


def model_futuristes():
    img = pygame.image.load("./assets/plane_models_futuristes.png")
    models = []
    for y in range(0, img.get_height() - 134, 134):
        models.append(pygame.transform.scale_by(img.subsurface(0, y, 151, 134), 0.7))
    return models


def bullet_futuristes():
    img = pygame.image.load("./assets/bullet_test.png")
    bullets = []
    for x in range(0, 1533 - 153, 153):
        bullets.append(img.subsurface(x, 0, 153, 300))
    return bullets


"""
    self.bullets_model_coor = [((351, 2328), (38, 58), 1, [(0, 0)]),
                               ((323, 1542), (52, 76), 1, [(0, 0)]),
                               ((299, 1317), (103, 74), 2, [(-32, 0), (32, 0)]),
                               ((267, 283), (136, 76), 2, [(45, 0), (-45, 0)]),
                               ((285, 35), (121, 57), 4, [(55, -30), (30, 10), (-30, 10), (-55, -30)]),
                               ((254, 481), (198, 120), 3, [(60, 0), (0, 20), (-60, 0)]),
                               ((329, 808), (82, 71), 2, [(23, 0), (-23, 0)]),
                               ((304, 1050), (121, 66), 3, [(50, 0), (0, -25), (-50, 0)]),
                               ((305, 2082), (131, 77), 3, [(55, 0), (0, -20), (-55, 0)]),
                               ((302, 1807), (133, 96), 4, [(54, 0), (30, -20), (-30, -20), (-54, 0)]),
                               ((266, 2607), (190, 102), 4, [(60, -50), (20, 0), (-20, 0), (-60, -50)])]"""
