import random
import time
import pygame


class Comete(pygame.sprite.Sprite):
    def __init__(self, res, img, explode):
        pygame.sprite.Sprite.__init__(self)
        self.res = res
        self.bords = [[-50, self.res[0] + 50],
                      [-50, self.res[1] + 50]]

        self.img = img
        self.explosion_spritesheet = explode
        self.velocity_x = random.randint(1,3)
        self.velocity_y = random.randint(1,3)
        self.frame_height = 128
        self.frame_width = 128
        self.timer = time.time()
        self.duration = 0.1
        self.pos = self.spawn(res)
        self.frame_comete = self.model()
        self.index_frame_comete = 0
        self.image = self.frame_comete[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = pygame.mask.Mask.to_surface(self.mask)
        self.rect = self.image.get_rect()
        self.alive = True
        self.frames_explosion = self.explosion()
        self.index_frame_explosion = 0

    def spawn(self, res):
        x = random.randint(-20,res[0]+20)
        y = [-20, res[1]+20]
        pos = (x, y[random.randint(0,1)])
        if pos[0] > 0:
            self.velocity_x *= -1
        if pos[1] > 0:
            self.velocity_y *= -1
        return pos


    def model(self):
        models = []
        for x in range(0, self.img.get_width(), self.frame_width):
            for y in range(0, self.img.get_height(), self.frame_height):
                frame = self.img.subsurface((x, y, self.frame_width, self.frame_height))
                frame = pygame.transform.rotozoom(frame, 0, 0.5)
                models.append(frame)
        return models


    def update(self):
        if not self.alive:
            self.velocity_x = 0
            self.velocity_y = 0
            self.image = self.frames_explosion[self.index_frame_explosion]
            self.index_frame_explosion += 1
            if self.index_frame_explosion == len(self.frames_explosion) - 1:
                self.kill()
        else:
            self.image = self.frame_comete[self.index_frame_comete]
            if time.time() - self.timer > self.duration:
                self.timer = time.time()
                self.index_frame_comete += 1
            if self.index_frame_comete == len(self.frame_comete)-1:
                self.index_frame_comete = 0
        #self.image = pygame.transform.rotate(self.image, 5)
        self.pos = (self.pos[0] + self.velocity_x, self.pos[1] + self.velocity_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = pygame.mask.Mask.to_surface(self.mask)
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos[0], self.pos[1])

    def explosion(self):
        frames = []
        for x in range(0, self.explosion_spritesheet.get_width(), 256):
            for y in range(0, self.explosion_spritesheet.get_height(), 256):
                frame = self.explosion_spritesheet.subsurface(x,y, 256, 256)
                frames.append(frame)
        return frames
