import heapq

class Pathfinding:
    def __init__(self, tilemap):
        self.tilemap = tilemap

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
            if (check_location in self.tilemap.tilemap) and (self.tilemap.tilemap[check_location]["type"] in {"dirt", "spikes"}):
                continue

            if not self.is_node((position[0] + direction, position[1])):
                for y in range(100):
                    check_location = f"{position[0] + direction};{position[1] + y}"
                    if (check_location in self.tilemap.tilemap) and (self.tilemap.tilemap[check_location]["type"] == "spikes"):
                        break
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
        max_height = min(start_position[1], goal_position[1]) - jump_height
        
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
                if (check_location in self.tilemap.tilemap) and (self.tilemap.tilemap[check_location]["type"] in {"dirt", "spikes"}):
                    return False
        return True
    
    def neighbour_nodes(self, position):
        neighbours = []
        for nodes in self.walkable_neighbour_nodes(position):
            neighbours.append((nodes, "walk"))
        for nodes in self.drop_neighbour_nodes(position):
            neighbours.append((nodes, "drop"))
        for nodes in self.jump_neighbour_nodes(position):
            neighbours.append((nodes, "jump"))
        return neighbours

    def debug_nodes(self):
        nodes = []
        for loc in self.tilemap.tilemap:
            tile = self.tilemap.tilemap[loc]
            if tile['type'] == "dirt":
                x, y = tile['position']
                if self.is_node((x, y-1)):
                    nodes.append((x, y-1))
        return nodes

    def player_current_node(self, player_rect):
        player_x = int(player_rect.centerx / self.tilemap.tile_size)
        player_y = int((player_rect.bottom - 1) / self.tilemap.tile_size)
        for y in range(100):
            if self.is_node((player_x,player_y + y)):
                return ((player_x,player_y))
        return None
        
    def finish_node(self):
        for rect in self.tilemap.finish_tile():
            finish_x = int(rect.centerx / self.tilemap.tile_size)
            finish_y = int((rect.bottom - 1) / self.tilemap.tile_size)
            if self.is_node((finish_x,finish_y)):
                return ((finish_x,finish_y))
        return None

    def reconstruct_path(self, came_from, start, goal):
        path = []
        current = goal
        while current != start:
            previous_node, action = came_from[current]
            path.append((current, action))
            current = previous_node
        path.append((start, ""))
        path.reverse()
        return path

    def move_cost(self, node_a, node_b):
        distance = abs(node_a[0] - node_b[0]) 
        if (abs(node_a[0] - node_b[0]) == 1) and (node_a[1] == node_b[1]):
            return 1
        return distance + 6
    
    def manhattan_distance(self, node_a, node_b):
        return abs(node_a[0] - node_b[0]) + abs(node_a[1] - node_b[1])
    
    def astar_pathfinding(self, start, goal):
        frontier = []
        heapq.heappush(frontier, (0, start))

        came_from = {}
        g_cost = {start: 0}
        closed = set()

        while len(frontier) > 0:
            f_current, current = heapq.heappop(frontier)

            if current in closed:
                continue

            closed.add(current)

            if current == goal:
                return self.reconstruct_path(came_from, start, goal)

            neighbours = self.neighbour_nodes(current)
            i = 0
            while i < len(neighbours):
                neighbour, action = neighbours[i]

                if neighbour in closed:
                    i += 1
                    continue

                tentative_g = g_cost[current] + self.move_cost(current, neighbour)

                if neighbour not in g_cost or tentative_g < g_cost[neighbour]:
                    g_cost[neighbour] = tentative_g
                    came_from[neighbour] = (current, action)

                    f = g_cost[neighbour] + self.manhattan_distance(neighbour, goal)
                    heapq.heappush(frontier, (f, neighbour))
                i += 1

        return None
