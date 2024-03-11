import math

import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, res, pos, damage, bullet_pos, direction, velocity, img):
        pygame.sprite.Sprite.__init__(self)
        self.bords = self.bords = [[-10, res[0] + 10],
                                   [-10, res[1] + 10]]

        #caractéristique technique
        self.velocity = velocity
        self.damage = damage

        #mise en place de l'affichage
        self.rotation = 0
        self.direction = pygame.math.Vector2(direction[0], direction[1])
        self.position = self.set_position(pos, bullet_pos)
        self.image = img
        self.rotation = -self.direction.angle_to(pygame.math.Vector2(0, 1))
        self.image = pygame.transform.rotozoom(self.image, self.rotation, 0.5)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update(self):
        self.clear()
        self.position = (self.position[0] + self.velocity * self.direction[0], self.position[1] - self.velocity * self.direction[1])
        self.rect.center = self.position
        self.mask = pygame.mask.from_surface(self.image)

    def clear(self):
        if self.rect.centerx < self.bords[0][0] or self.rect.centerx > self.bords[0][1]:
            self.kill()
        elif self.rect.centery < self.bords[1][0] or self.rect.centery > self.bords[1][1]:
            self.kill()

    def set_position(self, pos, bullet_pos):
        #calculer l'angle
        y_axis = pygame.math.Vector2(0, +1)
        dot_product = self.direction.dot(y_axis)
        angle = math.radians((-math.degrees(math.atan2(y_axis.x * self.direction.y - y_axis.y * self.direction.x, dot_product)) )% 360.0)
        #calculer les nouvelles coordonées
        x_prime = (bullet_pos[0]-pos[0]) * math.cos(angle) - (bullet_pos[1]-pos[1]) * math.sin(angle) + pos[0]
        y_prime = (bullet_pos[0]-pos[0]) * math.sin(angle) + (bullet_pos[1]-pos[1]) * math.cos(angle) + pos[1]
        return x_prime,y_prime
