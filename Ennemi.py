import pygame

from Planer import *
import random


class Ennemi(Plane):
    def __init__(self, res, pos, hp, velocity, delay_time_fire, model_img, bullet_img, bullet_damage, bullet_speed,
                 explosion_img, explosion_frame_height, explosion_frame_width):

        # deplacement
        self.vx = random.randint(1, 1) * velocity[0]  # Composante de la vitesse en x
        self.vy = random.randint(1, 1) * velocity[1]  # Composante de la vitesse en y
        self.acceleration = 5  # Accélération

        Plane.__init__(self, res, pos, hp, delay_time_fire, model_img, bullet_img, bullet_damage, bullet_speed,
                       explosion_img, explosion_frame_height, explosion_frame_width)

    def pre_update(self, target_pos):
        if self.alive:
            self.target = target_pos
            self.pos = (self.pos[0] + self.vx, self.pos[1] + self.vy)
            if time.time() - self.timer_fire > self.duration_fire_off:
                self.timer_fire = time.time()
                self.fire(self.pos, self.pos, self.bullet_damage)
        self.update(target_pos)

    def health_barre(self):
        percent = (self.image_origin.get_width() * self.health_point) / self.health_point_origin
        return [self.rect.bottomleft[0], self.rect.bottomleft[1], percent, 2]


"""
    def mise_en_orbite(self, target_pos):
        print("mise orbit")

        pos_x = self.axe_long * math.cos(self.angle) + target_pos[0]/2
        pos_y = self.axe_little * math.sin(self.angle) + target_pos[1]/2

        if self.pos[0] < pos_x:
            pos_x = self.pos[0] + self.acceleration
        else:
            pos_x = self.pos[0] - self.acceleration
        if self.pos[1] < pos_y:
            pos_y = self.pos[0] + self.acceleration
        else:
            pos_y = self.pos[0] - self.acceleration

        self.pos = lerp(self.pos[0], pos_x, self.lerp_factor), lerp(self.pos[1], pos_y, self.lerp_factor)

        print(self.pos, (pos_x, pos_y))

        if abs(self.pos[0] - pos_x) < 5 and abs(self.pos[1] - pos_y) < 5:
            self.orbite = True
            self.timer = time.time()
            print(self.timer)



    def trajectoire_epelleptique(self, target_pos):
        print("orbite")
        # Calculer la nouvelle position en fonction de l'angle
        pos_x = self.axe_long * math.cos(self.angle) + target_pos[0]/2
        pos_y = self.axe_little * math.sin(self.angle) + target_pos[1]/2
        self.angle += self.omega

        pos_x = min(max(pos_x, 0), self.res[0])
        pos_y = min(max(pos_y, 0), self.res[1])

        self.last_pos = self.pos
        self.pos = (pos_x, pos_y)
        self.direction_x = self.pos[0] - self.last_pos[0]
        self.direction_y = self.pos[1] - self.last_pos[1]



    def calibrage_mouvement(self):
        print("calibrage")
        # Si la vitesse est inférieure à la vitesse maximale, augmentez la vitesse
        if math.sqrt(self.vx**2 + self.vy**2) > 2:
            if self.vx > 0:
                self.vx -= self.acceleration
            elif self.vx < 0:
                self.vx += self.acceleration
            if self.vy > 0:
                self.vy -= self.acceleration
            elif self.vy < 0:
                self.vy += self.acceleration
        else:
            self.calibrage = False


        # Calculer la nouvelle position en fonction de la vitesse
        new_x = self.pos[0] + self.vx
        new_y = self.pos[1] + self.vy

        # Limiter la position du vaisseau ennemi pour éviter de sortir du cadre
        new_x = min(max(new_x, 0), self.res[0])
        new_y = min(max(new_y, 0), self.res[1])

        # Appliquer l'interpolation linéaire (lerp) pour adoucir le mouvement
        self.pos = lerp(self.pos[0], new_x, self.lerp_factor), lerp(self.pos[1], new_y, self.lerp_factor)



    def ajuster_trajectoire(self):
        print("adjust")
        # Ajuster la trajectoire en utilisant la direction spécifiée
        self.vx = 10 * (abs(self.direction_x)/self.direction_x)
        self.vy = 10 * (abs(self.direction_y)/self.direction_y)


def lerp(a, b, t):
    return a + t * (b - a)
"""
