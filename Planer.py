import time
import pygame
import math
from Bullet import Bullet


class Plane(pygame.sprite.Sprite):
    def __init__(self, res, pos, hp, delay_time_fire, model_img, bullet_img,bullet_damage, bullet_speed, explosion_img,
                 explosion_frame_height, explosion_frame_width):
        pygame.sprite.Sprite.__init__(self)

        self.res = res

        # initialisation bot(true) ou joueur(false)
        self.alive = True

        # caractéristiques techniques
        self.pos = pos
        self.speed = (0, 0)
        self.health_point_origin = hp
        self.health_point = hp
        self.rotation = 0
        self.angle_fire = 0
        self.direction = pygame.math.Vector2(0, 1)
        self.bullet_damage = bullet_damage
        self.bullet_speed = bullet_speed

        # ressources graphiques
        self.image_origin = model_img
        self.image = model_img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_origin = pygame.mask.from_surface(self.image_origin)
        self.bullet_img = bullet_img
        self.explosion_spritesheet = explosion_img
        self.explosion_frame_height = explosion_frame_height
        self.explosion_frame_width = explosion_frame_width
        self.frames_explosion = self.explosion()
        self.index_frame_explosion = 0

        # gestion des tires
        self.bullet_group = pygame.sprite.Group()
        self.timer_fire = time.time()
        self.duration_fire_off = delay_time_fire
        self.target = None

    def update(self, target_pos):
        if not self.alive and self.index_frame_explosion < len(self.frames_explosion):
            self.image = self.frames_explosion[self.index_frame_explosion]
            self.index_frame_explosion += 1
            if self.index_frame_explosion == len(self.frames_explosion):
                self.pos = (-100, -100)
        if self.alive:  # à verifier
            self.track_target(target_pos)

        self.rect = self.image.get_rect()
        self.rect.center = (self.pos[0], self.pos[1])
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, x, y):
        #delta_rotation = x * self.angle_speed
        #self.rotation -= delta_rotation
        vec = pygame.math.Vector2(0, 1)
        vec.x = x
        vec.y = y
        if x == 0 and y == 0:
            if self.speed[0] < -0.5:
                self.speed = (self.speed[0] + 0.05, self.speed[1])
            elif self.speed[0] > 0.5:
                self.speed = (self.speed[0] - 0.05, self.speed[1])
            else:
                self.speed = (0, self.speed[1])
            if self.speed[1] < -0.5:
                self.speed = (self.speed[0], self.speed[1] + 0.05)
            elif self.speed[1] > 0.5:
                self.speed = (self.speed[0], self.speed[1] - 0.05)
            else:
                self.speed = (self.speed[0], 0)
        else:
            self.speed += vec * 0.5
            self.speed = (min(max(-5, self.speed[0]), 5), min(max(-5, self.speed[1]), 5))
            # vec.rotate_ip(-self.rotation)
        self.pos = (self.pos[0] + vec.x + self.speed[0], self.pos[1] + vec.y + self.speed[1])

    def explosion(self):
        frames = []
        for x in range(0, self.explosion_spritesheet.get_width(), self.explosion_frame_width):
            for y in range(0, self.explosion_spritesheet.get_height(), self.explosion_frame_height):
                frame = self.explosion_spritesheet.subsurface(x, y, self.explosion_frame_height,
                                                              self.explosion_frame_width)
                frames.append(frame)
        return frames

    def track_target(self, target_pos):
        angle = math.degrees(math.atan2(target_pos[1] - self.pos[1], target_pos[0] - self.pos[0]))
        self.rotation = -angle - 90
        self.image = pygame.transform.rotate(self.image_origin, self.rotation)

        self.angle_fire = -angle-90
        self.direction = pygame.math.Vector2(0, 1)
        self.direction.rotate_ip(self.angle_fire)
        self.direction.normalize_ip()

    def fire(self, pos, bullet_pos, damage):
        mask_image = self.mask_origin.to_surface()
        bullet_size = pygame.transform.scale_by(self.bullet_img, min((mask_image.get_width() / 100)*50/self.bullet_img.get_width(), 0.7))
        bullet = Bullet(self.res, (pos[0], pos[1]), damage, bullet_pos, self.direction,
                        self.bullet_speed, bullet_size)
        self.bullet_group.add(bullet)
        bullet.update()

    def get_damaged(self, damage):
        self.health_point -= damage
        if self.health_point <= 0:
            self.alive = False
