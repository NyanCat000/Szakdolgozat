import pygame

NEIGHBOUR_TILES = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]

class Tilemap:
    def __init__(self, game, tile_size=12):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'dirt', 'variant': 1, 'position': (3 + i, 10)}
            self.tilemap['10;' + str(5 + i)] = {'type': 'dirt', 'variant': 1, 'position': (10, 5 + i)}
    
    def neighbouring_tiles(self, position):
        tiles = []
        tile_location = (int(position[0] // self.tile_size), int(position[1] // self.tile_size))
        for neighbour in NEIGHBOUR_TILES:
            check_location = str(tile_location[0] + neighbour[0]) + ';' + str(tile_location[1] + neighbour[1])
            if check_location in self.tilemap:
                tiles.append(self.tilemap[check_location])
        return tiles
    
    def neighbouring_dirt_tiles(self, position):
        rects = []
        for tile in self.neighbouring_tiles(position):
            if tile['type'] == "dirt":
                rects.append(pygame.Rect(tile['position'][0] * self.tile_size, 
                                         tile['position'][1] * self.tile_size, 
                                         self.tile_size, 
                                         self.tile_size))
        return rects

    def render(self, surface, offset=(0, 0)):
        for location in self.tilemap:
            tile = self.tilemap[location]
            surface.blit(self.game.imgs[tile['type']][tile['variant']], 
                         (tile['position'][0] * self.tile_size - offset[0], 
                          tile['position'][1] * self.tile_size - offset[1]))

        for tile in self.offgrid_tiles:
            surface.blit(self.game.imgs[tile['type']][tile['variant']], 
                         (tile['position'][0] - offset[0], tile['position'][1] - offset[1]))