class Pathfinding:
    def __init__(self, tilemap, tile_size = 12):
        self.tilemap = tilemap
        self.tile_size = tile_size

    def is_node(self, position):
        check_location = f"{position[0]};{position[1] + 1}"
        check_air_above_location = f"{position[0]};{position[1]}"
        if (check_location in self.tilemap.tilemap) and (self.tilemap.tilemap[check_location]["type"] == "dirt"):
            if (check_air_above_location not in self.tilemap.tilemap) or (self.tilemap.tilemap[check_air_above_location]["type"] in {"flowers","large_decor","finish"}):
                return True
        return False
    
    def walkable_neighbour_nodes(self, position):
        neightbours = []
        for direction in [-1, 1]:
            if self.is_node((position[0] + direction, position[1])):
                neightbours.append((position[0] + direction, position[1]))
        return neightbours
    
    def drop_neighbour_nodes(self, position):
        neighbours = []
        for direction in [-1, 1]:

            check_location = f"{position[0] + direction};{position[1]}"
            if (check_location in self.tilemap.tilemap) and (self.tilemap.tilemap[check_location]["type"] in {"dirt", "spike"}):
                continue

            if not self.is_node((position[0] + direction, position[1])):
                for y in range(100):
                    if self.is_node((position[0] + direction, position[1] + y)):
                        neighbours.append((position[0] + direction, position[1] + y))
                        break
        return neighbours
    
    def jump_neighbour_nodes(self, position):
        neighbours = []
        jump_height = 3
        jump_distance = 4
        jump_fall = 100

        for direction in [-1, 1]:
            for x in range(1, jump_distance + 1):
                goal_x = position[0] + (x * direction)
                for y in range(-jump_fall, jump_height + 1):
                    goal_y = position[1] - y
                    if self.is_node((goal_x, goal_y)):
                        if self.is_path_clear(position, (goal_x, goal_y), jump_height):
                            neighbours.append((goal_x, goal_y))
        return neighbours
    
    def is_path_clear(self, start_position, goal_position, jump_height):
        max_height = start_position[1] - jump_height
        
        if goal_position[0] > start_position[0]:
            direction = 1
        else: direction = -1
        for x in range(start_position[0], goal_position[0] + direction, direction):
            if x == start_position[0]:
                check_bottom = start_position[1]
            elif x == goal_position[0]:
                check_bottom = goal_position[1]
            else:
                check_bottom = max(start_position[1], goal_position[1])
            for y in range(max_height, check_bottom):
                check_location = f"{x};{y}"
                if (check_location in self.tilemap.tilemap) and (self.tilemap.tilemap[check_location]["type"] in {"dirt", "spike"}):
                    return False
        return True
    
    def neighbour_nodes(self, position):
        neighbours = []
        for nodes in self.walkable_neighbour_nodes(position):
            neighbours.append(nodes)
        for nodes in self.drop_neighbour_nodes(position):
            neighbours.append(nodes)
        for nodes in self.jump_neighbour_nodes(position):
            neighbours.append(nodes)

    def debug_nodes(self):
        nodes = []
        for loc in self.tilemap.tilemap:
            tile = self.tilemap.tilemap[loc]
            if tile['type'] == "dirt":
                x, y = tile['position']
                if self.is_node((x, y-1)):
                    nodes.append((x, y-1))
        return nodes

