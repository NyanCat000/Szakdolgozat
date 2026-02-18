import sys
import pygame

from scripts.utilities import images
from scripts.tilemap import Tilemap

class Editor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0))
        self.screen_size = self.screen.get_size()
        self.display = pygame.Surface((self.screen_size[0]/3, self.screen_size[1]/3))
        self.clock = pygame.time.Clock()
        
        self.movement = [False, False, False, False]
        self.offset = [0, 0]
        
        self.imgs = {
            "dirt": images("tiles/dirt"),
            "flowers": images("tiles/decor/flowers"),
            "large_decor": images("tiles/decor/large_decors"),
            "spikes": images("tiles/spikes"),
            "character_spawn": images("tiles/character_spawn"),
            "finish": images("tiles/finish")
        }
        
        self.tilemap = Tilemap(self)
        
        try:
            self.tilemap.load("assets/maps/0.json")
        except FileNotFoundError:
            pass
        
        self.list = list(self.imgs)
        self.type = 0
        self.variant = 0
        
        self.put_down_tile = False
        self.delete_tile = False
        self.ongrid = True
        
    
    def run(self):
        while True:
            self.display.fill((0, 0, 255))
            
            self.offset[0] += (self.movement[1] - self.movement[0]) * 2
            self.offset[1] += (self.movement[3] - self.movement[2]) * 2
            render_offset = (int(self.offset[0]), int(self.offset[1]))
            
            self.tilemap.render(self.display, render_offset)
            
            current_tile = self.imgs[self.list[self.type]][self.variant].copy()
            
            mouse_position = (pygame.mouse.get_pos()[0] / 3, pygame.mouse.get_pos()[1] / 3)
            tile_position = (int((mouse_position[0] + self.offset[0]) // self.tilemap.tile_size), 
                             int((mouse_position[1] + self.offset[1]) // self.tilemap.tile_size))
            
            if mouse_position[1] > 50:
                if self.ongrid:
                    self.display.blit(current_tile, (tile_position[0] * self.tilemap.tile_size - self.offset[0], 
                                                     tile_position[1] * self.tilemap.tile_size - self.offset[1]))
                else:
                    self.display.blit(current_tile, mouse_position)
                
                if self.put_down_tile:
                    if self.ongrid:
                        self.tilemap.tilemap[f"{tile_position[0]};{tile_position[1]}"] = {"type": self.list[self.type],
                                                                                          "variant": self.variant,
                                                                                          "position": tile_position}
                    else:
                        self.tilemap.offgrid_tiles.append({"type": self.list[self.type], 
                                                           "variant": self.variant,
                                                           "position": (mouse_position[0] + self.offset[0],
                                                                        mouse_position[1] + self.offset[1])})

                if self.delete_tile:
                    location = f"{tile_position[0]};{tile_position[1]}"
                    if location in self.tilemap.tilemap:
                        del self.tilemap.tilemap[location]
                    for offgrid_tile in self.tilemap.offgrid_tiles.copy():
                        tile = self.imgs[offgrid_tile["type"]][offgrid_tile["variant"]]
                        tile_rect = pygame.Rect(offgrid_tile["position"][0] - self.offset[0],
                                                offgrid_tile["position"][1] - self.offset[1],
                                                tile.get_width(), tile.get_height())
                        if tile_rect.collidepoint(mouse_position):
                            self.tilemap.offgrid_tiles.remove(offgrid_tile)
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.put_down_tile = True
                    if event.button == 3:
                        self.delete_tile = True
                    if event.button == 4:
                        self.variant += 1
                        if self.variant >= len(self.imgs[self.list[self.type]]):
                            self.variant = 0
                    if event.button == 5:
                        self.variant -= 1
                        if self.variant < 0:
                            self.variant = len(self.imgs[self.list[self.type]]) - 1
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.put_down_tile = False
                    if event.button == 3:
                        self.delete_tile = False
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_s:
                        self.tilemap.save("assets/maps/0.json")
                    if event.key == pygame.K_1:
                        self.type = 0
                        self.variant = 0
                    if event.key == pygame.K_2:
                        self.type = 1
                        self.variant = 0
                    if event.key == pygame.K_3:
                        self.type = 2
                        self.variant = 0
                    if event.key == pygame.K_4:
                        self.type = 3
                        self.variant = 0
                    if event.key == pygame.K_5:
                        self.type = 4
                        self.variant = 0
                    if event.key == pygame.K_6:
                        self.type = 5
                        self.variant = 0
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False
            
            pygame.draw.rect(self.display, pygame.Color("aquamarine2"), (0, 0, self.screen_size[0] / 3, 25), border_radius=20)
            tile_offset = 20
            for tile_type in self.list:
                tile = self.imgs[tile_type][0]
                self.display.blit(tile, (tile_offset, 25 / 2 - tile.get_height() / 2))
                tile_offset += 50

            pygame.draw.rect(self.display, pygame.Color("aquamarine"), (0, 25, self.screen_size[0] / 3, 25), border_radius=20)
            tile_offset = 20
            current_type = self.list[self.type]
            for variant in self.imgs[current_type]:
                if variant.get_height() > 16:
                    variant = pygame.transform.scale(variant, (16,16))
                self.display.blit(variant, (tile_offset, 25 / 2 - variant.get_height() / 2 + 25))
                tile_offset += 50

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()