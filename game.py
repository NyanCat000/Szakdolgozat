import pygame
import os
import math

from scripts.utilities import image, images, Animation
from scripts.tilemap import Tilemap
from scripts.character_physics import Player, Ai
from scripts.clouds import Clouds
from scripts.button import Button

from scripts.pathfinding import Pathfinding

class Game:
    def __init__(self, screen, start_level = 0):
        pygame.init()
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.display = pygame.Surface((self.screen_size[0]//6, self.screen_size[1]//6))
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
            "player/jump": Animation(images("characters/player/jump"), duration=10),
            "ai/idle": Animation(images("characters/ai/idle"), duration=6),
            "ai/run": Animation(images("characters/ai/run"), duration=5),
            "ai/jump": Animation(images("characters/ai/jump"), duration=10)
        }

        self.ambience = pygame.mixer.Sound("assets/sound_effects/ambience.wav")
        self.die = pygame.mixer.Sound("assets/sound_effects/die.wav")
        self.finish_sfx = pygame.mixer.Sound("assets/sound_effects/finish.wav")
        self.jump = pygame.mixer.Sound("assets/sound_effects/jump.wav")
        self.walk = pygame.mixer.Sound("assets/sound_effects/walk.wav")
        self.ambience.set_volume(0.15)
        self.die.set_volume(0.15)
        self.finish_sfx.set_volume(0.8)
        self.jump.set_volume(0.15)
        self.walk.set_volume(0.1)

        self.clouds_close = Clouds(image("clouds/0.png"), type = 0, count=4)
        self.clouds_far = Clouds(image("clouds/1.png"), type = 1, count=3)
        self.tilemap = Tilemap(self)
        self.player = Player(self, (0,0), (11, 11))
        self.ai = Ai(self, (0,0), (11, 11))

        self.level = start_level
        self.load_map(self.level)

        self.path = None ##

    def load_map(self, map):
        self.tilemap.load(f"assets/maps/{map}.json")
        self.player.position = self.tilemap.get_player_spawn()
        self.player.air_time = 0

        self.offset = [0, 0]
        self.dead = False
        self.finish = False

        self.transition_step = 50
        self.transition = True
        self.transition_newmap = True

        self.pathfinding = Pathfinding(self.tilemap) ##
        self.debug_nodes = self.pathfinding.debug_nodes() ##

    def render_debug_nodes(self, offset = (0,0)): ##
        mx, my = pygame.mouse.get_pos()
        scale_x = self.screen.get_width() / self.display.get_width()
        scale_y = self.screen.get_height() / self.display.get_height()

        character_rect = pygame.Rect(self.player.position[0], 
                                            self.player.position[1], 
                                            self.player.character_size[0], 
                                            self.player.character_size[1])

        player_node = self.pathfinding.player_current_node(character_rect)
        finish_node = self.pathfinding.finish_node()
        
        if scale_x == 0 or scale_y == 0: return 

        world_mx = mx / scale_x + offset[0]
        world_my = my / scale_y + offset[1]

        closest_node = None
        min_dist = 1000
        tile_size = self.tilemap.tile_size
        
        for node in self.debug_nodes:
            px = node[0] * tile_size + tile_size // 2
            py = node[1] * tile_size + tile_size // 2
            
            dist = ((world_mx - px)**2 + (world_my - py)**2)**0.5
            
            if dist < 30: 
                if dist < min_dist:
                    min_dist = dist
                    closest_node = node

        for node in self.debug_nodes:
            px = node[0] * tile_size + tile_size // 2
            py = node[1] * tile_size + tile_size // 2

            screen_px = px - offset[0]
            screen_py = py - offset[1]
            
            if node == player_node:
                color = (0, 255, 255)
            elif node == finish_node:
                color = (100, 100, 100)
            elif node == closest_node:
                color = (255, 255, 0)
            else:
                color = (255, 0, 0) 

            pygame.draw.circle(self.display, color, (screen_px, screen_py), 2)

        if closest_node:
            cx, cy = closest_node
            start_pix = ((cx * tile_size + tile_size // 2) - offset[0], (cy * tile_size + tile_size // 2) - offset[1])

            def draw_links(neighbors, color):
                for n in neighbors:
                    end_pix = ((n[0] * tile_size + tile_size // 2) - offset[0], (n[1] * tile_size + tile_size // 2) - offset[1])
                    pygame.draw.line(self.display, color, start_pix, end_pix, 1)

            
            walks = self.pathfinding.walkable_neighbour_nodes((cx, cy))
            drops = self.pathfinding.drop_neighbour_nodes((cx, cy))
            jumps = self.pathfinding.jump_neighbour_nodes((cx, cy))

            
            draw_links(jumps, (255, 0, 255))
            draw_links(drops, (0, 100, 255))
            draw_links(walks, (0, 255, 0))
    
    def pause_buttons(self):
        button_names = ["resume", "settings", "controls", "return to main menu"]
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
        self.ambience.stop()
        self.die.stop()
        self.finish_sfx.stop()
        self.jump.stop()
        self.walk.stop()
        bgr = pygame.transform.scale(image("background/bgr_menu.png"), self.screen_size)
        bgr.set_alpha(100)

        pause_text = self.main_font.render("paused", True, (65,65,65))
        pause_text_rect = pause_text.get_rect(center=(self.screen.get_width() / 2, 100))
        self.screen.blit(bgr, (0,0))
        self.screen.blit(pause_text, pause_text_rect) 

        for button in self.buttons:
            button.draw(self.screen)
    
    def run(self):
        bgr = pygame.transform.scale(image("background/bgr_game.png"), self.display.get_size())

        while True:
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
                    if event.key == pygame.K_p: ##
                        character_rect = pygame.Rect(self.player.position[0], 
                                            self.player.position[1], 
                                            self.player.character_size[0], 
                                            self.player.character_size[1])

                        start = self.pathfinding.player_current_node(character_rect)
                        goal = self.pathfinding.finish_node()
                        self.ai.position = [start[0] * self.tilemap.tile_size, (start[1] + 1) * self.tilemap.tile_size - self.ai.character_size[1]]
                        self.ai.velocity = [0,0]
                        self.ai.collisions["down"] = True

                        print("START:", start)
                        print("GOAL:", goal)
                                            
                        if start and goal:
                            self.path = self.pathfinding.astar_pathfinding(start,goal)
                            print("PATH:", self.path)
                            if self.path:
                                self.ai.calculate_path(goal)
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
                                button.sound(event)
                                if button.rect.collidepoint(mouse_pos):
                                    if button.text == "resume":
                                        self.paused = False
                                    if button.text == "return to main menu":
                                        return "menu"
                                    if button.text == "settings":
                                        return "settings_game"
                                    if button.text == "controls":
                                        return "controls_game"

            if not self.paused:
                if self.ambience.get_num_channels() == 0:
                    self.ambience.play(-1)
                if self.finish:
                    if self.level < len(os.listdir("assets/maps")) - 1:
                        self.level += 1
                        self.load_map(self.level)
                    else:
                        return "levels"
                
                if self.transition:
                    if self.transition_newmap:
                        self.transition_step -= 1
                        if self.transition_step <= 0:
                            self.transition_step = 0
                            self.transition = False
                    else:
                        self.transition_step += 1
                        if self.transition_step >= 50:
                            self.transition_step = 50
                            self.transition = False
                    
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
                            self.die.play()
                            break

                self.clouds_far.update()
                self.clouds_close.update()
            
                if not self.dead:
                    self.player.update(self.tilemap, 
                                    (self.movement[1] - self.movement[0], 0))
                self.ai.update(self.tilemap)
                    
            self.display.blit(bgr, (0, 0))
            render_offset = (int(self.offset[0]), int(self.offset[1]))

            self.clouds_far.render(self.display, render_offset)
            self.clouds_close.render(self.display, render_offset)
            self.tilemap.render(self.display, render_offset)
            
            self.render_debug_nodes(render_offset) ##
            if self.path: ##
                self.ai.render(self.display, render_offset)
                for (node, action) in self.path:
                    x, y = node

                    px = (x * self.tilemap.tile_size + self.tilemap.tile_size // 2) - render_offset[0]
                    py = (y * self.tilemap.tile_size + self.tilemap.tile_size // 2) - render_offset[1]

                    pygame.draw.circle(
                        self.display,
                        (255, 255, 255),
                        (px, py),
                        3
                    )
            
            if not self.dead:
                self.player.render(self.display, render_offset)
            
            if self.transition_step:
                center_x = self.display.get_width() // 2
                center_y = self.display.get_height() // 2
                c_radius = math.sqrt(center_x**2 + center_y**2)

                transition_surface = pygame.Surface(self.display.get_size())
                transition_surface.fill((10, 10, 50))
                pygame.draw.circle(transition_surface, (0, 0, 0), 
                                   (self.display.get_width() // 2, self.display.get_height() // 2),
                                   ((50 - abs(self.transition_step)) / 50) * c_radius)
                transition_surface.set_colorkey((0, 0, 0))
                self.display.blit(transition_surface, (0, 0))
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            if self.paused:
                self.pause()

            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()