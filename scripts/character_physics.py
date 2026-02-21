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
        image = pygame.transform.flip(self.animation.current_image(), self.flip, False)
    
        if self.enter_finish:
            scaled_width = image.get_width() * self.scale
            scaled_height = image.get_height() * self.scale
            scaled = pygame.transform.scale(image, (scaled_width, scaled_height))

            surface.blit(scaled, (self.position[0] - offset[0],
                                    self.position[1] - offset[1]))

        else:
            surface.blit(image, 
                     (self.position[0] - offset[0], 
                      self.position[1] - offset[1]))
        
class Player(Physics):
    def __init__(self, game, position, character_size):
        super().__init__(game, "player", position, character_size)
        self.air_time = 0
        self.jumps = 1

        self.enter_finish = False
        self.finish_center = None
        self.scale = 1
        self.finish_animation_done = False

    def update(self, tilemap, movement=(0, 0)):
        if self.enter_finish:
            character_center_x = self.position[0] + self.character_size[0] // 2
            character_center_y = self.position[1] + self.character_size[1] // 2
            self.position[0] += (self.finish_center[0] - character_center_x) * 0.05
            self.position[1] += (self.finish_center[1] - character_center_y) * 0.05
            
            if not self.finish_animation_done:
                if self.scale > 0:
                    self.scale -= 0.02
                else:
                    self.finish_animation_done = True
                    self.game.finish = True
                    self.enter_finish = False
                    self.scale = 1
                    self.finish_animation_done = False
            return
            
        super().update(tilemap, movement)
        
        if self.collisions["down"]:
            self.air_time = 0
            self.jumps = 1
        else:
            self.air_time += 1

        if self.air_time > 100:
            self.game.dead = True
            self.game.die.play()

        if movement[0] != 0:
            if self.game.walk.get_num_channels() == 0:
                self.game.walk.play(-1)
        else:
            self.game.walk.stop()
        
        if self.air_time > 3:
            self.game.walk.stop()
            self.current_action("jump")
        elif movement[0] != 0:
            self.current_action("run")
        else:
            self.current_action("idle")

        image = self.animation.current_image()
        if self.flip:
            image = pygame.transform.flip(image, True, False)
        self.mask = pygame.mask.from_surface(image)

        character_rect = pygame.Rect(self.position[0], 
                           self.position[1], 
                           self.character_size[0], 
                           self.character_size[1])
        for rect in tilemap.finish_tile():
            if character_rect.colliderect(rect) and not self.enter_finish:
                self.enter_finish = True
                self.finish_center = rect.center

                self.game.transition = True
                self.game.transition_newmap = False
                
                self.game.walk.stop()
                self.game.finish_sfx.play()

    def jump(self):
        if self.enter_finish:
            return
        if self.air_time < 4:
            if self.jumps > 0:
                self.velocity[1] = -4
                self.jumps -= 1
                self.air_time = 4
                self.game.jump.play()

class Ai(Physics):
    def __init__(self, game, position, character_size):
        super().__init__(game, "ai", position, character_size)
        self.path = []
        self.enter_finish = False
        self.jump_target = None

    def update(self, tilemap):
        movement = [0,0]
        if self.path:
            target_node, action = self.path[0]
            target_x = target_node[0] * tilemap.tile_size + tilemap.tile_size // 2
            character_x = self.position[0] + self.character_size[0] // 2
            
            dist_x = abs(character_x - target_x)
            dist_y = abs(self.position[1] + self.character_size[1] - (target_node[1] + 1) * tilemap.tile_size)
            
            if dist_x > 2:
                if character_x < target_x:
                    movement[0] = 1
                else: 
                    movement[0] = -1
            if action == "jump":
                if self.jump_target != target_node:
                    if self.collisions["down"]:
                        self.velocity[1] = -4
                        self.jump_target = target_node

            if action == "drop":
                if character_x < target_x:
                    movement[0] = 1
                else: movement[0] = -1 

            if self.collisions["down"]:
                self.air_time = 0
            else:
                self.air_time += 1

            if self.air_time >3:
                self.current_action("jump")
            elif movement[0] != 0:
                self.current_action("run")
            else:
                self.current_action("idle")
            
            if dist_x < 4 and dist_y < 2 and self.collisions["down"]:
                self.path.pop(0)

        super().update(tilemap, movement)
    
    def calculate_path(self, goal):
        character_rect = pygame.Rect(self.position[0], 
                           self.position[1], 
                           self.character_size[0], 
                           self.character_size[1])
        player_node = self.game.pathfinding.player_current_node(character_rect)
        if player_node:
            path = self.game.pathfinding.astar_pathfinding(player_node, goal)
            if path:
                self.path = path
                if len(self.path) > 0:
                    self.path.pop(0)
   