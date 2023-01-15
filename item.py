import pygame, os.path, random
from config import *
class Item(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        #Extracting a random item from spritesheet and scaling dimensions up to desired size
        self.itemsSpritesheet = pygame.image.load(Item.accessFile("items.png")).convert_alpha()
        self.col = random.randint(0, 15)
        self.image = Item.getImage(self.itemsSpritesheet, 9, self.col, 32, 32)
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()

        self.rect.right = random.randint(self.rect.width, WIDTH)
        self.rect.bottom = random.randint(self.rect.height, HEIGHT)

    @staticmethod
    def getImage(spritesheet, row, col, width, height):
        img = pygame.Surface((width, height), pygame.SRCALPHA, 32) 
        x = col * width
        y = row * height
        img.blit(spritesheet, (0,0), (x,y,width,height))
        return img

    @staticmethod
    def accessFile(filename:str) -> str:
        cwd = os.path.dirname(__file__)
        path = f"{cwd}/Run! Assets/{filename}"
        return path