import pygame, os.path
from config import *
class Block(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(Block.accessFile("blockup.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
    
    def update(self):
        self.handleKeyPressed()
        self.boundary()

    def handleKeyPressed(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.rect.center += pygame.Vector2(0, 10)
            self.image = pygame.image.load(Block.accessFile("blockdown.png")).convert_alpha()

        elif keys[pygame.K_UP]:
            self.rect.center += pygame.Vector2(0, -10)
            self.image = pygame.image.load(Block.accessFile("blockup.png")).convert_alpha()

        elif keys[pygame.K_RIGHT]:
            self.rect.center += pygame.Vector2(10, 0)
            self.image = pygame.image.load(Block.accessFile("blockright.png")).convert_alpha()
            
        elif keys[pygame.K_LEFT]:
            self.rect.center += pygame.Vector2(-10, 0)
            self.image = pygame.image.load(Block.accessFile("blockleft.png")).convert_alpha()
    
    def boundary(self):
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH

        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        
    @staticmethod
    def accessFile(filename:str) -> str:
        cwd = os.path.dirname(__file__)
        path = f"{cwd}/Run! Assets/{filename}"
        return path