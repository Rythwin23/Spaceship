import pygame
from Player import Player
from pygame.locals import *
from EnnemiManager import EnnemiManager
import psutil


def mouse_position():
    return pygame.mouse.get_pos()


class Game:
    def __init__(self, res):
        self.screen = None
        self.player = None
        self.res = res
        self.windows_title = "Skidbladnir"
        self.background = pygame.image.load("./assets/space.png")
        self.background = pygame.transform.scale_by(self.background, 1.2)
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.score = 0

        '''
        # chargement de player
        self.player_model = None
        self.player = None
        self.player_bullet_img = None
        self.player_explosion_spritesheet = None
        '''

        # chargement de l'ennemiManager
        self.ennemi_manager = EnnemiManager(self.res)
        self.init_player()
        self.start()

    def init_player(self):
        '''
        self.player_model = pygame.image.load("./assets/planeModel3.png")
        self.player_explosion_spritesheet = pygame.image.load("./assets/explosion_model3.png")
        self.player_bullet_img = pygame.image.load("./assets/player_bullet_model.png")
        '''
        #self.player = Plane(self.res, (self.res[0] / 2, self.res[1] / 2), 0.2, self.player_model, self.player_bullet_img, 15, self.player_explosion_spritesheet, 256, 256)
        self.player = Player(self.res, (self.res[0] / 2, self.res[1] / 2))
        self.player.increase_level(0)



    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption(self.windows_title)
        self.run()

    def run(self):
        while self.is_running:
            if self.player.alive:
                self.manage_pressed_key()
            for event in pygame.event.get():
                self.manage_events(event)
            self.update()
        self.quit()

    def manage_events(self, event):
        if event.type == QUIT:
            self.is_running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                self.player.prefire()
            if event.key == K_c:
                self.ennemi_manager.spawn_comete()
            if event.key == K_e:
                self.ennemi_manager.spawn_ennemi()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.player.prefire()
            if event.button == 3:
                pass

    def manage_pressed_key(self):
        keys = pygame.key.get_pressed()
        vector = [0, 0]
        if keys[pygame.K_q]:
            vector[0] -= 1
        if keys[pygame.K_d]:
            vector[0] += 1
        if keys[pygame.K_z]:
            vector[1] -= 1
        if keys[pygame.K_s]:
            vector[1] += 1
        self.player.move(vector[0], vector[1])

    def draw(self):
        if self.player.index_frame_explosion == len(self.player.frames_explosion):
            self.init_player()
            for ennemi in self.ennemi_manager.ennemi_sprite_group:
                ennemi.kill()
            for bullet in self.ennemi_manager.bullet_group:
                bullet.kill()


        # affichage de tout les objets
        self.screen.blit(self.player.image, self.player.rect)
        self.player.bullet_group.draw(self.screen)
        pygame.draw.rect(self.screen,"green", self.player.health_barre())
        self.ennemi_manager.cometes_group.draw(self.screen)
        self.ennemi_manager.ennemi_sprite_group.draw(self.screen)
        for ennemi in self.ennemi_manager.ennemi_sprite_group.sprites():
            ennemi.bullet_group.draw(self.screen)
            pygame.draw.rect(self.screen,"red", ennemi.health_barre())

    def manage_collision(self):

        # ennemi - bullet_player
        collisions_ennemi_bulletplayer = pygame.sprite.groupcollide(self.ennemi_manager.ennemi_sprite_group,
                                                                    self.player.bullet_group, False, False)
        for ennemi, bullets in collisions_ennemi_bulletplayer.items():
            for bullet in bullets:
                if pygame.sprite.collide_mask(ennemi, bullet):
                    if ennemi.alive:
                        bullet.kill()
                        ennemi.get_damaged(bullet.damage)
                        if not ennemi.alive:
                            self.player.increase_level(5)



        # player _ ennemi_bullet
        collisions_player_bulletennemi = pygame.sprite.spritecollide(self.player, self.ennemi_manager.bullet_group,False)

        if self.player.alive:
            if len(collisions_player_bulletennemi) > 0:
                for bullet in collisions_player_bulletennemi:
                    if pygame.sprite.collide_mask(self.player, bullet):
                        self.player.get_damaged(bullet.damage)
                        bullet.kill()



        # comete_bullet_player
        collision_comete_bullet_player = pygame.sprite.groupcollide(self.player.bullet_group,
                                                                    self.ennemi_manager.cometes_group, False, False)
        for bullet, cometes in collision_comete_bullet_player.items():
            for comete in cometes:
                if pygame.sprite.collide_mask(bullet, comete):
                    if comete.alive:
                        bullet.kill()
                        comete.alive = False
                        self.player.increase_level(2)

    def update(self):

        # update de l'affichage
        self.screen.blit(self.background, self.background.get_rect())

        # Verification de collision
        self.manage_collision()

        # mise à jour des objets
        self.player.update(mouse_position())
        self.player.bullet_group.update()
        self.ennemi_manager.update(self.player)

        # affichage des objets
        #self.screen.blit(self.player.mask_image, self.player.pos)
        self.draw()


        memory_info = psutil.Process().memory_info()


        police = pygame.font.Font(None, 18)
        text_memoire = police.render(f"Consommation de mémoire : {memory_info.rss / (1024 * 1024)} Mo", True, "red")
        self.screen.blit(text_memoire, (50,70))

        # pygame.display.update()
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    def quit(self):
        pygame.display.quit()
        pygame.quit()
        del self
