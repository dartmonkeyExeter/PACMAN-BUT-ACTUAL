import pygame, math

class Pacman:
    def __init__(self):
        self.x = 280
        self.y = 330
        self.radius = 8
        self.color = (255, 255, 0)
        self.direction = "left"
        self.speed = 2.25
        self.direction_to_angle_dict = {"right": 0, "down": 90, "left": 180, "up": 270}
        self.animation_frame = 0
        self.animate_backwards = False
        self.moving = True
        self.power_pellet_clock = 0
        self.score = 0
        self.ghosts_eaten = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        start_angle = math.radians((-0 - self.animation_frame) + self.direction_to_angle_dict[self.direction])
        end_angle = math.radians((0 + self.animation_frame) + self.direction_to_angle_dict[self.direction])
        center = (self.x, self.y)
        vertices = [center]
        num_vertices = 30 
        angle_step = (end_angle - start_angle) / num_vertices
        for i in range(num_vertices + 1):
            angle = start_angle + i * angle_step
            x = center[0] + self.radius * math.cos(angle)
            y = center[1] + self.radius * math.sin(angle)
            vertices.append((x, y))

        pygame.draw.polygon(screen, (0, 0, 0), vertices)

    def move(self):
        if self.direction == "right":
            self.x += self.speed
        if self.direction == "left":
            self.x -= self.speed
        if self.direction == "up":
            self.y -= self.speed
        if self.direction == "down":
            self.y += self.speed

        if self.x > 560:
            self.x = 0
        if self.x < 0:
            self.x = 560

    def clamping(self, grid):
        current_array = grid.grid[int(self.y / 20)]
        if self.direction == "right":
            if current_array[int((self.x + self.radius) / 20)] == "#":
                self.x -= self.speed
                self.moving = False
            else:
                self.moving = True
        if self.direction == "left":
            if current_array[int((self.x - self.radius) / 20)] == "#":
                self.x += self.speed
                self.moving = False
            else:
                self.moving = True
        if self.direction == "down":
            if grid.grid[int((self.y + self.radius) / 20)][int(self.x / 20)] == "#" or grid.grid[int((self.y + self.radius) / 20)][int(self.x / 20)] == "-":
                self.y -= self.speed
                self.moving = False
            else:
                self.moving = True
        if self.direction == "up":
            if grid.grid[int((self.y - self.radius) / 20)][int(self.x / 20)] == "#":
                self.y += self.speed
                self.moving = False
            else:
                self.moving = True

    def eat_check(self, ghost_list, grid, frames_per_second):
        reset = False
        current_array = list(grid.grid[int(self.y / 20)])  # Convert string to list
        ghost_positions = [(int(ghost.x / 20), int(ghost.y / 20)) for ghost in ghost_list]
        if current_array[int(self.x / 20)] == ".":
            current_array[int(self.x / 20)] = " "
            self.score += 10
        if current_array[int(self.x / 20)] == "*":
            current_array[int(self.x / 20)] = " "
            for ghost in ghost_list:
                ghost.edible = True
            self.power_pellet_clock = frames_per_second * 10
            self.score += 50
        
        grid.grid[int(self.y / 20)] = "".join(current_array)

        for ghost in ghost_list:
            if (int(ghost.x / 20), int(ghost.y / 20)) == (int(self.x / 20), int(self.y / 20)) and not ghost.edible:
                self.x = 280
                self.y = 330
                self.score -= 100
                reset = True
            elif (int(ghost.x / 20), int(ghost.y / 20)) == (int(self.x / 20), int(self.y / 20)) and ghost.edible:
                ghost.x = ghost.start_pos[0] * 20
                ghost.y = ghost.start_pos[1] * 20
                ghost.edible = False
                ghost.path = None
                self.score += 200 * (self.ghosts_eaten + 1)
                self.ghosts_eaten += 1

        if reset:
            for ghost in ghost_list:
                ghost.x = ghost.start_pos[0] * 20
                ghost.y = ghost.start_pos[1] * 20
                ghost.edible = False
                ghost.path = None


    def power_pellet_timer(self, ghost_list):
        if self.power_pellet_clock > 0:
            self.power_pellet_clock -= 1
        else:
            self.ghosts_eaten = 0
            for ghost in ghost_list:
                ghost.edible = False

    def animation(self):
        if self.moving:
            if self.animation_frame == 45:
                self.animate_backwards = True
            if self.animation_frame == 0:
                self.animate_backwards = False
            if self.animate_backwards:
                self.animation_frame -= 5
            else:
                self.animation_frame += 5
        