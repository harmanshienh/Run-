import pygame, os.path, random
from config import *
class Enemy(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        #Generating a random enemy
        filename = enemyImgFiles[random.randint(0, (len(enemyImgFiles) - 1))]
        self.image = pygame.image.load(Enemy.accessFile(filename)).convert_alpha()
        self.rect = self.image.get_rect()
        self.ypos = random.choice([0, HEIGHT])

        if self.ypos == 0:
            self.rect.bottomright = pygame.Vector2(self.determineXPos(),0)
        elif self.ypos == HEIGHT:
            self.rect.topright = pygame.Vector2(self.determineXPos(), HEIGHT)

        self.speed = self.determineSpeed()

    def update(self):
        self.rect.center += self.speed
        if self.ypos == 0:
            if self.rect.top > HEIGHT:
                self.remove()
        elif self.ypos == HEIGHT:
            if self.rect.bottom < 0:
                self.remove()

    #Determining speed of enemy based on spawn location
    def determineSpeed(self) -> pygame.Vector2():

        #Enemy will always go either straight up or across the screen
        if self.rect.right <= WIDTH / 2:
            xspeed = random.randint(0, 5)
        elif self.rect.right >= WIDTH / 2:
            xspeed = random.randint(-5, 0)
        
        if self.ypos == 0:
            self.speed = pygame.Vector2(xspeed, 5)
        elif self.ypos == HEIGHT:
            self.speed = pygame.Vector2(xspeed, -5)
        return self.speed

    def determineXPos(self) -> float:
        enemy_radius = self.image.get_width() / 2
        center = random.randint((0 + enemy_radius), (WIDTH - enemy_radius))
        return center + enemy_radius

    @staticmethod
    def accessFile(filename:str) -> str:
        cwd = os.path.dirname(__file__)
        path = f"{cwd}/Run! Assets/{filename}"
        return path