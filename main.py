# pac-man

import pygame, math, random, copy, pacmanclass, gridclass, ghostclass, fruitsclass

pygame.init()
clock = pygame.time.Clock()
fps = 75
size = [560, 640]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("pacman!!!!")

spawn_fruit = True

level = 0

pacman = pacmanclass.Pacman()

blinky = ghostclass.Ghost((255, 0, 0), (11*20)+4, (12*20)+4, "right")
pinky = ghostclass.Ghost((255, 184, 255), (16*20)+4, (12*20)+4, "left")
inky = ghostclass.Ghost((0, 255, 255), (11*20)+4, (14*20)+4, "right")
clyde = ghostclass.Ghost((255, 184, 82), (16*20)+4, (14*20)+4, "left")

ghosts = [blinky, pinky, inky, clyde]

fruit_order = [pygame.image.load("sprites/PM_Cherry.png"), pygame.image.load("sprites/PM_Strawberry.png"), pygame.image.load("sprites/PM_Orange.png"), pygame.image.load("sprites/PM_Apple.png"), pygame.image.load("sprites/PM_Melon.png"), pygame.image.load("sprites/PM_Galaxian.png"), pygame.image.load("sprites/PM_Bell.png"), pygame.image.load("sprites/PM_Key.png")]
fruit_points = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
fruits = []

grid = gridclass.Grid()

def update_all():
    global level, spawn_fruit
    dots_left = grid.dots_left()

    if (dots_left == 170 or dots_left == 70) and spawn_fruit:
        if level <= 7:
            fruits.append(fruitsclass.Fruit(fruit_order[level % 8], fruit_points[level % 8]))
        spawn_fruit = False
    else:
        spawn_fruit = True

    if dots_left == 0:
        level += 1
        pacman.x = 280
        pacman.y = 330
        for ghost in ghosts:
            ghost.x = ghost.start_pos[0] * 20
            ghost.y = ghost.start_pos[1] * 20
        grid.grid = copy.deepcopy(grid.copygrid)
    pacman.move()
    pacman.clamping(grid)
    pacman.eat_check(ghosts, grid, fps)
    pacman.power_pellet_timer(ghosts)
    pacman.animation()
    
    pacman.draw(screen)

    grid.draw(screen)

    for fruit in fruits:
        fruit.draw(screen)
        fruit.eat_check(pacman, len(fruits))

    for ghost in ghosts:
        ghost.behaviours(pacman, grid)
        ghost.move()
        ghost.draw(screen)

running = True

while running:
    screen.fill((0, 0, 0))

    update_all()

    #print(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            current_array = (int(pacman.x / 20), int(pacman.y / 20))
            if event.key == pygame.K_LEFT and grid.grid[int(pacman.y / 20)][int((pacman.x - 20) / 20)] != "#":
                pacman.direction = "left"
                pacman.x = current_array[0] * 20 + 10
                pacman.y = current_array[1] * 20 + 10
            if event.key == pygame.K_RIGHT and grid.grid[int(pacman.y / 20)][int((pacman.x + 20) / 20)] != "#":
                pacman.direction = "right"
                pacman.x = current_array[0] * 20 + 10
                pacman.y = current_array[1] * 20 + 10
            if event.key == pygame.K_UP and grid.grid[int((pacman.y - 20) / 20)][int((pacman.x) / 20)] != "#":
                pacman.direction = "up"
                pacman.x = current_array[0] * 20 + 10
                pacman.y = current_array[1] * 20 + 10
            if event.key == pygame.K_DOWN and grid.grid[int((pacman.y + 20) / 20)][int(pacman.x / 20)] != "#" and grid.grid[int((pacman.y + 20) / 20)][int(pacman.x / 20)] != "-":
                pacman.direction = "down"
                pacman.x = current_array[0] * 20 + 10
                pacman.y = current_array[1] * 20 + 10

    pygame.display.flip()
    clock.tick(fps)