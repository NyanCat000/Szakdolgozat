import pygame

class Physics:
    def __init__(self, game, character_type, position, character_size):
        self.game = game
        self.character_type = character_type
        self.position = list(position)
        self.character_size = character_size

        self.velocity = [0, 0]
        self.collisions = {"left": False, "right": False, "up": False, "down": False}
        
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {"left": False, "right": False, "up": False, "down": False}
        frame_movement = (movement[0] + self.velocity[0], 
                          movement[1] + self.velocity[1])

        self.position[0] += frame_movement[0]
        character_rect = pygame.Rect(self.position[0], 
                           self.position[1], 
                           self.character_size[0], 
                           self.character_size[1])
        for rect in tilemap.neighbouring_dirt_tiles(self.position):
            if character_rect.colliderect(rect):
                if frame_movement[0] < 0:
                    character_rect.left = rect.right
                    self.collisions['left'] = True
                if frame_movement[0] > 0:
                    character_rect.right = rect.left
                    self.collisions['right'] = True
                self.position[0] = character_rect.x
        
        self.position[1] += frame_movement[1]
        character_rect = pygame.Rect(self.position[0], 
                           self.position[1], 
                           self.character_size[0], 
                           self.character_size[1])
        for rect in tilemap.neighbouring_dirt_tiles(self.position):
            if character_rect.colliderect(rect):
                if frame_movement[1] < 0:
                    character_rect.top = rect.bottom
                    self.collisions['up'] = True
                if frame_movement[1] > 0:
                    character_rect.bottom = rect.top
                    self.collisions['down'] = True
                self.position[1] = character_rect.y
        
        self.velocity[1] += 0.2
        
        if self.collisions['up'] or self.collisions['down']:
            self.velocity[1] = 0
        
    def render(self, surface, offset=(0, 0)):
        surface.blit(self.game.imgs['player'], (self.position[0] - offset[0], self.position[1] - offset[1]))
        