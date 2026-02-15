import pygame
import os

from scripts.utilities import image, images, Animation
from scripts.tilemap import Tilemap
from scripts.character_physics import Player
from scripts.clouds import Clouds
from scripts.button import Button

class Game:
    def __init__(self, start_level = 0):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0))
        self.screen_size = self.screen.get_size()
        self.display = pygame.Surface((self.screen_size[0]/6, self.screen_size[1]/6))
        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]

        self.main_font = pygame.font.Font("assets/fonts/PermanentMarker-Regular.ttf", 80)
        self.button_font = pygame.font.Font("assets/fonts/PermanentMarker-Regular.ttf", 50)
        
        self.paused = False
        self.buttons = []
        self.pause_buttons()

        self.imgs = {
            "dirt": images("tiles/dirt"),
            "flowers": images("tiles/decor/flowers"),
            "large_decor": images("tiles/decor/large_decors"),
            "spikes": images("tiles/spikes"),
            "character_spawn": images("tiles/character_spawn"),
            "finish": images("tiles/finish"),
            "player/idle": Animation(images("characters/player/idle"), duration=6),
            "player/run": Animation(images("characters/player/run"), duration=5),
            "player/jump": Animation(images("characters/player/jump"), duration=10)
        }
        
        self.clouds_close = Clouds(image("clouds/0.png"), type = 0, count=4)
        self.clouds_far = Clouds(image("clouds/1.png"), type = 1, count=3)
        self.tilemap = Tilemap(self)
        self.player = Player(self, (0,0), (11, 11))

        self.level = start_level
        self.load_map(self.level)

    def load_map(self, map):
        self.tilemap.load(f"assets/maps/{map}.json")
        self.player.position = self.tilemap.get_player_spawn()
        self.player.air_time = 0
        self.offset = [0, 0]
        self.dead = False
        self.finish = False
    
    def pause_buttons(self):
        button_names = ["resume", "options", "controls", "return to main menu"]
        center_y = self.screen.get_height() / 2 - 75
        y_offset = 150

        for i in range(len(button_names)):
            name = button_names[i]
            button_rect = pygame.Rect(0, 0, 550, 100)
            button_rect.centerx = self.screen.get_width() / 2
            button_rect.centery = center_y + i * y_offset

            button = Button(button_rect, name, self.button_font, border_radius=150)
            self.buttons.append(button)

    def pause(self):
        bgr = pygame.transform.scale(image("background/bgr_menu.png"), self.screen_size)
        bgr.set_alpha(100)

        pause_text = self.main_font.render("paused", True, (65,65,65))
        pause_text_rect = pause_text.get_rect(center=(self.screen.get_width() / 2, 100))
        self.screen.blit(bgr, (0,0))
        self.screen.blit(pause_text, pause_text_rect) 

        for button in self.buttons:
            button.draw(self.screen)
    
    def run(self):
        self.running = True
        bgr = pygame.transform.scale(image("background/bgr_game.png"), self.display.get_size())
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.player.jump()
                    if event.key == pygame.K_ESCAPE:
                        self.movement[0] = False
                        self.movement[1] = False 
                        self.paused = not self.paused
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                if self.paused:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if event.button == 1:
                            for button in self.buttons:
                                if button.rect.collidepoint(mouse_pos):
                                    if button.text == "resume":
                                        self.paused = False
                                    if button.text == "return to main menu":
                                        return "menu"

            if not self.paused:

                if self.finish:
                    if self.level < len(os.listdir("assets/maps")) - 1:
                        self.level += 1
                        self.load_map(self.level)
                    else:
                        return "levels"
            
                if self.dead:
                    self.load_map(self.level)
            
                character_rect = pygame.Rect(self.player.position[0], 
                                            self.player.position[1], 
                                            self.player.character_size[0], 
                                            self.player.character_size[1])
                self.offset[0] += (character_rect.centerx - self.display.get_width() / 2 - self.offset[0]) / 15
                self.offset[1] += (character_rect.centery - self.display.get_height() / 2 - self.offset[1]) / 15

                for spike in self.tilemap.neighbouring_spikes(self.player.position):
                    if character_rect.colliderect(spike["rect"]):
                        offset = (spike["rect"].x - self.player.position[0],
                                    spike["rect"].y - self.player.position[1])

                        if self.player.mask.overlap(spike["mask"], offset):
                            self.dead = True
                            break

                self.clouds_far.update()
                self.clouds_close.update()
            
                if not self.dead:
                    self.player.update(self.tilemap, 
                                    (self.movement[1] - self.movement[0], 0))
                    
            self.display.blit(bgr, (0, 0))
            render_offset = (int(self.offset[0]), int(self.offset[1]))

            self.clouds_far.render(self.display, render_offset)
            self.clouds_close.render(self.display, render_offset)
            self.tilemap.render(self.display, render_offset)
            
            if not self.dead:
                self.player.render(self.display, render_offset)
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            if self.paused:
                self.pause()

            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()