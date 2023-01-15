from email.mime import audio
import pygame, sys, os.path, random
from config import *
from block import Block
from enemy import Enemy
from item import Item

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Run!")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.enemySpawnTime = 2000
        self.timer = pygame.time.set_timer(pygame.USEREVENT, self.enemySpawnTime)
        self.font = pygame.font.SysFont(None, 40, True, False)

        self.blocks = pygame.sprite.Group()
        b = Block()
        self.blocks.add(b)

        self.enemies = pygame.sprite.Group()

        self.items = pygame.sprite.Group()
        item = Item()
        self.items.add(item)

        self.state = states.get("READY")
        self.score = 0
        self.level = 1
        self.lastIndex = -1

    def update(self):
        if self.state == states.get("READY"):
            pygame.mixer.music.load(Game.accessFile("music.mp3"))
            pygame.mixer.music.play(-1)
            self.handleReadyKeyPressed()
            self.enemies.empty()

        elif self.state == states.get("GAME"):
            self.level = (self.score // 5) + 1
            self.blocks.update()
            self.enemies.update()
            self.checkCollisions()
        
    def drawText(self):
        if self.state == states.get("READY"):
            textPrompt = self.font.render("PRESS SPACEBAR TO START", True, (255,255,255))
            promptRect = textPrompt.get_rect()
            promptRect.center = (WIDTH / 2, HEIGHT / 2)
            self.screen.blit(textPrompt, (promptRect.left, HEIGHT / 2))

        textScore = self.font.render(f"Score: {self.score}", True, (255,255,255))
        self.screen.blit(textScore, (0, 0))

        textLevel = self.font.render(f"Level: {self.level}", True, (255,255,255))
        levelRect = textLevel.get_rect()
        levelRect.topright = (WIDTH, 0)
        self.screen.blit(textLevel, (levelRect.left, 0))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT and self.state == states.get("GAME"):
                    enemy = Enemy()
                    self.enemies.add(enemy)
            
            self.screen.fill("black")
            self.update()

            self.blocks.draw(self.screen)
            self.items.draw(self.screen)
            self.enemies.draw(self.screen)

            self.drawText()
            pygame.display.update()
            self.clock.tick(FPS)

    def handleReadyKeyPressed(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.state = states.get("GAME")

    def checkCollisions(self):
        for block in self.blocks:
            enemyCollision = pygame.sprite.spritecollide(block, self.enemies, True)
            if enemyCollision:
                self.items.empty()

                pygame.mixer.music.fadeout(750)
                loseSound = pygame.mixer.Sound(Game.accessFile("lose.wav"))
                loseSound.play()
                
                self.__init__()

            itemCollision = pygame.sprite.spritecollide(block, self.items, False)
            if itemCollision:
                self.score += 1
                self.playCollectSound()

                if self.score % 5 == 0:
                    self.enemySpawnTime *= 0.95
                    #Enemies will initially spawn every 2 seconds, -5% spawn time for every level
                    self.timer = pygame.time.set_timer(pygame.USEREVENT, int(self.enemySpawnTime))

                self.items.empty()
                item = Item()
                self.items.add(item)
    
    def playCollectSound(self):
        while True:
            index = random.randint(0, 6)
            if index != self.lastIndex:
                self.lastIndex = index
                break

        collectSound = pygame.mixer.Sound(Game.accessFile(audioFiles[index]))
        collectSound.play()
    
    @staticmethod
    def accessFile(filename:str) -> str:
        cwd = os.path.dirname(__file__)
        path = f"{cwd}/Run! Assets/{filename}"
        return path

if __name__ == "__main__":
    game = Game()
    game.run()