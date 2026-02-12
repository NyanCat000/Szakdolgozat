import pygame

class Physics:
    def __init__(self, game, character_type, position, character_size):
        self.game = game
        self.character_type = character_type
        self.position = list(position)
        self.character_size = character_size

        self.velocity = [0, 0]
        self.collisions = {"left": False, "right": False, "up": False, "down": False}

        self.action = ""
        self.flip = False
        self.current_action("idle")

    def current_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.imgs[self.character_type + "/" + self.action].copy()
        
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
                    self.collisions["left"] = True
                if frame_movement[0] > 0:
                    character_rect.right = rect.left
                    self.collisions["right"] = True
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
                    self.collisions["up"] = True
                if frame_movement[1] > 0:
                    character_rect.bottom = rect.top
                    self.collisions["down"] = True
                self.position[1] = character_rect.y
        
        self.velocity[1] += 0.2
        
        if self.collisions["up"] or self.collisions["down"]:
            self.velocity[1] = 0

        if movement[0] < 0:
            self.flip = True
        elif movement[0] > 0:
            self.flip = False

        self.animation.update()
        
    def render(self, surface, offset=(0, 0)):
        surface.blit(pygame.transform.flip(self.animation.current_image(), self.flip, False), 
                     (self.position[0] - offset[0], 
                      self.position[1] - offset[1]))
        
class Player(Physics):
    def __init__(self, game, position, character_size):
        super().__init__(game, "player", position, character_size)
        self.air_time = 0
        self.jumps = 1

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)
        
        if self.collisions["down"]:
            self.air_time = 0
            self.jumps = 1
        else:
            self.air_time += 1

        if self.air_time > 100:
            self.game.dead = True

        if self.air_time > 3:
            self.current_action("jump")
        elif movement[0] != 0:
            self.current_action("run")
        else:
            self.current_action("idle")

        image = self.animation.current_image()
        if self.flip:
            image = pygame.transform.flip(image, True, False)
        self.mask = pygame.mask.from_surface(image)

    def jump(self):
        if self.air_time < 4:
            if self.jumps > 0:
                self.velocity[1] = -4
                self.jumps -= 1
                self.air_time = 4

    
        