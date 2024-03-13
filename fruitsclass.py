import pygame

class Fruit:
    def __init__(self, sprite, fruit_score):
        self.sprite = sprite
        self.x = 280
        self.y = 330
        self.eaten = False
        self.initialise_timer = 10
        self.fruit_score = fruit_score

    def draw(self, screen):
        if not self.eaten:
            screen.blit(self.sprite, (self.x - 9, self.y - 9))
            self.initialise_timer -= 0.01       
        else:
            screen.blit(self.sprite, (self.x - 9, self.y - 9))     
    
    def eat_check(self, pacman, amount_of_fruits):
        distance = ((pacman.x - self.x) ** 2 + (pacman.y - self.y) ** 2) ** 0.5

        if distance <= 15:
            self.eaten = True
            self.x = 300 + (amount_of_fruits * 5)
            self.y = 600 
            pacman.score += self.fruit_score