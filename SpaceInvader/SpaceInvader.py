import pygame
import random
import math
from pygame import mixer

# Initializing pygame
pygame.init()

# Creating game window
screen = pygame.display.set_mode((800, 600))

# Background Image
background = pygame.image.load("background.jpg")

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("001-spaceship.png")
pygame.display.set_icon(icon)

# Player Icon
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Bullet Icon
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 0.5
bulletReady = True

# Alien Icon
alienImgs = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
numAliens = 10

# Generating Aliens to fight
for i in range(numAliens):
    alienImgs.append(pygame.image.load("alien1.png"))
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(50, 150))
    alienX_change.append(0.3)
    alienY_change.append(40)

score = 0
font = pygame.font.SysFont("Arial", 30)

# Game Over Font and Button
gameOverFont = pygame.font.Font("freesansbold.ttf", 64)
restartButton = pygame.Rect(250, 325, 120, 60)
quitButton = pygame.Rect(425, 325, 120, 60)

def drawScore(x, y):
    scoreText = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(scoreText, (x, y))


def drawPlayer(x, y):
    screen.blit(playerImg, (x, y))


def drawAlien(x, y, i):
    screen.blit(alienImgs[i], (x, y))


def drawBullet(x, y):
    global bulletReady
    bulletReady = False
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x2 - x1, 2)) + (math.pow(y2 - y1, 2)))
    if distance < 27:
        return True
    else:
        return False

def isButtonCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x2 - x1, 2)) + (math.pow(y2 - y1, 2)))
    if distance < 60:
        return True
    else:
        return False


def gameOverScreen():
    gameOverText = gameOverFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gameOverText, (200, 250))

    pygame.draw.rect(screen, (255, 255, 255), restartButton, 2)
    restartText = font.render("Retry?", True, (255, 255, 255))
    screen.blit(restartText, (268, 335))

    pygame.draw.rect(screen, (255, 255, 255), quitButton, 2)
    quitText = font.render("Quit?", True, (255, 255, 255))
    screen.blit(quitText, (450, 335))

    quitCollision = isButtonCollision(bulletX, 450, bulletY, 335)
    # retryCollision = isButtonCollision(bulletX, 268, bulletY, 335)

    if quitCollision:
        global running
        running = False



# Game loop
running = True


# Implement the game loop
while running:
    # screen.fill((100, 0, 0))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -0.1
            if event.key == pygame.K_d:
                playerX_change = 0.1
            if event.key == pygame.K_SPACE and bulletReady is True:
                mixer.Sound("Shooting.wav").play()
                bulletX = playerX
                drawBullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    playerX += playerX_change

    # Checking Player Boundaries
    if playerX >= 736:
        playerX = 736
    elif playerX <= 0:
        playerX = 0

    for i in range(numAliens):

        if alienY[i] >= 200:
            for j in range(numAliens):
                alienY[j] = 2000
            gameOverScreen()
            break

        alienX[i] += alienX_change[i]

        # Checking Alien Boundaries
        if alienX[i] >= 736 or alienX[i] <= 0:
            alienX_change[i] = -alienX_change[i]
            alienY[i] += alienY_change[i]

        # Collision Detection
        collision = isCollision(bulletX, alienX[i], bulletY, alienY[i])
        if collision:
            explosionSound = mixer.Sound("Explosion.wav")
            explosionSound.play()
            bulletY = 480
            bulletReady = True
            score += 1
            alienX[i] = random.randint(0, 736)
            alienY[i] = random.randint(50, 150)

        drawAlien(alienX[i], alienY[i], i)

    # Bullet Movement
    if bulletReady is False:
        drawBullet(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY <= -32:
            bulletReady = True
            bulletY = 480

    drawPlayer(playerX, playerY)
    drawScore(10, 10)

    pygame.display.update()
