import pygame, random, math

class Ghost:
    def __init__(self, color, x, y, starting_dir):
        self.x = x
        self.y = y
        self.direction = starting_dir
        self.speed = 2.0
        self.color = color
        self.radius = 8
        self.calculate_path = True
        self.path = []
        self.edible = False
        self.was_edible_last_frame = False
        self.start_pos = (int(x / 20), int(y / 20))
        self.move_to_base = False

    def draw(self, screen):
        if self.edible:
            pygame.draw.rect(screen, (0,0,255), (self.x, self.y, self.radius * 2, self.radius * 2))
        else: 
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.radius * 2, self.radius * 2))
    
    def BFS(self, start, end, grid):
        queue = {start: [[start]]}
        visited = {start: set()}
        all_paths = []
        while any(queue.values()):
            for ghost, path_queue in queue.copy().items():
                path = path_queue.pop(0)
                node = path[-1]
                if node == end:
                    all_paths.append(path)
                elif node not in visited[ghost]:
                    visited[ghost].add(node)
                    random.shuffle([(0, -1), (0, 1), (-1, 0), (1, 0)])
                    for adjacent in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                        new_x = node[0] + adjacent[0]
                        new_y = node[1] + adjacent[1]
                        if (0 <= new_x < len(grid[0])) and (0 <= new_y < len(grid)) and grid[new_y][new_x] != "#":
                            new_path = list(path)
                            new_path.append((new_x, new_y))
                            if ghost not in queue:
                                queue[ghost] = []
                            queue[ghost].append(new_path)
        return all_paths

    def move(self):
        try:
            curr_arr = (int(round(self.x / 20)), int(round(self.y / 20)))
            next_node = self.path[0]

            if abs(self.x - next_node[0] * 20) < self.speed and abs(self.y - next_node[1] * 20) < self.speed:
                self.x = next_node[0] * 20
                self.y = next_node[1] * 20
                self.path.pop(0)

            else:
                dx = next_node[0] * 20 - self.x
                dy = next_node[1] * 20 - self.y
                distance = math.sqrt(dx ** 2 + dy ** 2)

                dx = dx / distance * self.speed
                dy = dy / distance * self.speed

                # Update the ghost's position
                self.x += dx
                self.y += dy

        except IndexError:
            self.calculate_path = True

    def behaviours(self, pacman, grid):
        if self.edible and not self.was_edible_last_frame:
            self.path = []
            self.calculate_path = True
        
        self.was_edible_last_frame = self.edible

        if random.randint(0, 100) == 0 and not self.edible:
            self.calculate_path = True
        if self.path is None or len(self.path) == 0 or (self.edible and len(self.path) <= 3):
            self.calculate_path = True
        
        if self.calculate_path and not self.edible:
            pacman_array = (int(pacman.x / 20), int(pacman.y / 20))
            ghost_array = (int(self.x / 20), int(self.y / 20))
            self.path = random.choice(self.BFS(ghost_array, pacman_array, grid.grid))
            self.calculate_path = False
        
        elif self.calculate_path and self.edible:
            ghost_array = (int(self.x / 20), int(self.y / 20))
            pacman_array = (int(pacman.x / 20), int(pacman.y / 20))
            while True:
                random_pos = (random.randint(0, 27), random.randint(0, 29))
                distance = abs(random_pos[0] - pacman_array[0]) + abs(random_pos[1] - pacman_array[1])
                err = []
                while grid.nodemap[random_pos[1]][random_pos[0]] == "#" and distance > 20:
                    random_pos = (random.randint(0, 26), random.randint(0, 29))
                
                err = self.BFS(ghost_array, random_pos, grid.grid)
                if err:
                    self.path = random.choice(err)
                    break
                else:
                    continue
            self.calculate_path = False