import sys
import pygame

from scripts.utilities import image, images, Animation
from scripts.tilemap import Tilemap
from scripts.character_physics import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0))
        self.screen_size = self.screen.get_size()
        self.display = pygame.Surface((self.screen_size[0]/6, self.screen_size[1]/6))
        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]

        self.imgs = {
            "dirt": images("tiles/dirt"),
            "flowers": images("tiles/decor/flowers"),
            "large_decor": images("tiles/decor/large_decors"),
            "spikes": images("tiles/spikes"),
            "character_spawn": images("tiles/character_spawn"),
            "player/idle": Animation(images("characters/player/idle"), duration=6),
            "player/run": Animation(images("characters/player/run"), duration=5),
            "player/jump": Animation(images("characters/player/jump"), duration=10)
        }

        self.tilemap = Tilemap(self)
        self.player = Player(self, (0,0), (11, 11))
        self.load_map("00")

    def load_map(self, map):
        self.tilemap.load(f"assets/maps/{map}.json")
        self.player.position = self.tilemap.get_player_spawn()
        self.player.air_time = 0
        self.offset = [0, 0]
        self.dead = False
    
    def run(self):
        self.running = True
        while self.running:

            self.display.fill((0, 0, 255))
            
            if self.dead:
                self.load_map("00")
            
            character_rect = pygame.Rect(self.player.position[0], 
                                         self.player.position[1], 
                                         self.player.character_size[0], 
                                         self.player.character_size[1])
            self.offset[0] += (character_rect.centerx - self.display.get_width() / 2 - self.offset[0]) / 15
            self.offset[1] += (character_rect.centery - self.display.get_height() / 2 - self.offset[1]) / 15
            render_offset = (int(self.offset[0]), int(self.offset[1]))

            self.tilemap.render(self.display, render_offset)
            
            if not self.dead:
                self.player.update(self.tilemap, 
                                (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, render_offset)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.player.jump()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()