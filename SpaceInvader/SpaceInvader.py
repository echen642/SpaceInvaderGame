import pygame
import sys
import random
import math
from pygame import mixer
import os



class Game:
    def __init__(self):
        pygame.init()  # Initializing pygame
        os.chdir("C:\\Users\\Eddie\\GitHub\\SpaceInvaderGame\\SpaceInvader")

        self.running = True

        # Score
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # Game Over Font and Button
        self.gameOverFont = pygame.font.Font("freesansbold.ttf", 64)
        self.restartButton = pygame.Rect(250, 325, 120, 60)
        self.quitButton = pygame.Rect(425, 325, 120, 60)

        # Creating game window
        self.screen = pygame.display.set_mode((800, 600))

        # Background Image
        self.background = pygame.image.load("background.jpg")

        # Title and Icon
        pygame.display.set_caption("Space Invaders")
        icon = pygame.image.load("001-spaceship.png")
        pygame.display.set_icon(icon)

        # Player Icon
        self.playerImg = pygame.image.load("player.png")
        self.playerX = 370
        self.playerY = 480
        self.playerX_change = 0

        # Bullet Icon
        self.bulletImg = pygame.image.load("bullet.png")
        self.bulletX = 0
        self.bulletY = 480
        self.bulletY_change = 0.5
        self.bulletReady = True

        # Alien Icon
        self.alienImgs = []
        self.alienX = []
        self.alienY = []
        self.alienX_change = []
        self.alienY_change = []
        self.numAliens = 10

        # Generating Aliens to fight
        for i in range(self.numAliens):
            self.alienImgs.append(pygame.image.load("alien1.png"))
            self.alienX.append(random.randint(0, 736))
            self.alienY.append(random.randint(50, 150))
            self.alienX_change.append(0.3)
            self.alienY_change.append(40)

    def drawScore(self, x, y):
        scoreText = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(scoreText, (x, y))

    def drawPlayer(self, x, y):
        self.screen.blit(self.playerImg, (x, y))

    def drawAlien(self, x, y, i):
        self.screen.blit(self.alienImgs[i], (x, y))

    def drawBullet(self, x, y):
        self.bulletReady = False
        self.screen.blit(self.bulletImg, (x + 16, y + 10))

    def isCollision(self, x1, x2, y1, y2):
        if self.bulletReady is False:
            distance = math.sqrt((math.pow(x2 - x1, 2)) + (math.pow(y2 - y1, 2)))
            if distance < 27:
                return True
            else:
                return False

    def isButtonCollision(self, x1, x2, y1, y2):
        distance = math.sqrt((math.pow(x2 - x1, 2)) + (math.pow(y2 - y1, 2)))
        if distance < 60:
            return True
        else:
            return False

    def gameOverScreen(self):
        gameOverText = self.gameOverFont.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(gameOverText, (200, 250))

        pygame.draw.rect(self.screen, (255, 255, 255), self.restartButton, 2)
        restartText = self.font.render("Retry?", True, (255, 255, 255))
        self.screen.blit(restartText, (268, 335))

        pygame.draw.rect(self.screen, (255, 255, 255), self.quitButton, 2)
        quitText = self.font.render("Quit?", True, (255, 255, 255))
        self.screen.blit(quitText, (450, 335))

        quitCollision = self.isButtonCollision(self.bulletX, 450, self.bulletY, 335)
        retryCollision = self.isButtonCollision(self.bulletX, 268, self.bulletY, 335)

        if quitCollision:
            pygame.quit()
            sys.exit()

        if retryCollision:
            newGame = Game()
            newGame.run()

    def run(self):
        # Implement the game loop
        while self.running:
            # screen.fill((100, 0, 0))

            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.playerX_change = -0.1
                    if event.key == pygame.K_d:
                        self.playerX_change = 0.1
                    if event.key == pygame.K_SPACE and self.bulletReady is True:
                        mixer.Sound("Shooting.wav").play()
                        self.bulletX = self.playerX
                        self.drawBullet(self.bulletX, self.bulletY)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        self.playerX_change = 0

            self.playerX += self.playerX_change

            # Checking Player Boundaries
            if self.playerX >= 736:
                self.playerX = 736
            elif self.playerX <= 0:
                self.playerX = 0

            # Checking AlienY Boundaries
            for i in range(self.numAliens):
                if self.alienY[i] >= 416:
                    for j in range(self.numAliens):
                        self.alienY[j] = 2000
                    self.gameOverScreen()
                    break

                self.alienX[i] += self.alienX_change[i]

                # Alien Movement
                if self.alienX[i] >= 736 or self.alienX[i] <= 0:
                    self.alienX_change[i] = -self.alienX_change[i]
                    self.alienY[i] += self.alienY_change[i]

                # Collision Detection
                collision = self.isCollision(self.bulletX, self.alienX[i], self.bulletY, self.alienY[i])
                if collision:
                    explosionSound = mixer.Sound("Explosion.wav")
                    explosionSound.play()
                    self.bulletY = 480
                    self.bulletReady = True
                    self.score += 1
                    self.alienX[i] = random.randint(0, 736)
                    self.alienY[i] = random.randint(50, 150)

                self.drawAlien(self.alienX[i], self.alienY[i], i)

            # Bullet Movement
            if self.bulletReady is False:
                self.drawBullet(self.bulletX, self.bulletY)
                self.bulletY -= self.bulletY_change
                if self.bulletY <= -32:
                    self.bulletReady = True
                    self.bulletY = 470

            self.drawPlayer(self.playerX, self.playerY)
            self.drawScore(10, 10)

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
