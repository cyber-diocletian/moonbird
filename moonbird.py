import pygame
import random

#declaring variables
display_width = 800
display_height = 600
block_size = 41
blockY = 200
blockX = 200
FPS = 30
gameExit = False
gameOver = False
gravity = 11
velocity = 0
accelerationY = 0
columnX = 800
columnY = 300
moonX = 700
groundX = 0
enemyX = 10000
enemyY = random.randrange(100,500)
columnGap = 200
score = 0
highScore = 0
columnColor = (255,255,255)
titleScreen = True

#permanent score file
scoreFile = open("highscore.txt", 'r+')
highScore = int(scoreFile.read())

#initalizing objects and methods
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))                           #make sure this is a tuple!
pygame.display.set_caption("Moon Bird")
clock = pygame.time.Clock()
font = pygame.font.Font("emulogic.ttf", 20)

#loading sounds
jumpSound = pygame.mixer.Sound('jump.wav')
gameOverSound = pygame.mixer.Sound('gameover.wav')
titleSound = pygame.mixer.Sound('intro.wav')

#loading sprites
moon = pygame.image.load("moon.png").convert()
ground1 = pygame.image.load("ground.png").convert()
ground2 = pygame.image.load("ground.png").convert()
column = pygame.image.load("column.png").convert()
bird1 = pygame.image.load('bird1.png').convert()
bird1.set_colorkey((255,0,255))
bird2 = pygame.image.load('bird2.png').convert()
bird2.set_colorkey((255,0,255))
enemy = pygame.image.load('enemy.png').convert()
enemy.set_colorkey((255,0,255))

#icon
icon = pygame.image.load("icon.png").convert()
icon.set_colorkey((255,0,255))
pygame.display.set_icon(icon)

#methods

def scoreFunction(score, highScore):
    textScore = str(score)
    message_to_screen(textScore, (255,255,255), 0, 300)

def columns(columnX, columnY):
    gameDisplay.blit(column, [columnX,columnY-25,100,columnY])
    gameDisplay.blit(column, [columnX,columnY+columnGap,100,700])
    pygame.draw.rect(gameDisplay, (115,115,115), [columnX,0,10,columnY])
    pygame.draw.rect(gameDisplay, (115,115,115), [columnX,columnY+columnGap,10,700])
    pygame.draw.rect(gameDisplay, (182,198,251), [columnX+90,0,10,columnY])
    pygame.draw.rect(gameDisplay, (182,198,251), [columnX+90,columnY+columnGap,10,700])
        #surface, color, [X position, Y position, width, height]

def message_to_screen(msg, color, xDisplace, yDisplace):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [xDisplace, (300 - yDisplace)])

def draw_stars(starX, starY):
    pygame.draw.circle(gameDisplay, (random.randrange(50,255),random.randrange(100,255),random.randrange(100,255)), (starX,starY), 1, 1)

def title_screen():
    intro = True
    titleSound.play()
    while intro:
        gameDisplay.fill((0,0,24))
        message_to_screen("MOON BIRD", (255,255,255), 300, 100)
        message_to_screen("Press space to begin", (255,255,255), 200, 0)
        message_to_screen("Tyler Landry, 2017", (255,255,255), 200, -200)
        message_to_screen("TylerMLandry@outlook.com", (255,255,255), 150, -250)
        pygame.display.update()
        clock.tick(10)
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        intro = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()

title_screen()

#main game loop    
while not gameExit:
                    
    if gameOver == True:
        gameOverSound.play()
    
    while gameOver == True:
            gameDisplay.fill((0,0,24))
            message_to_screen("Game over. your score was " + str(score), (255,255,255), 100, 200)
            message_to_screen("The high score is " + str(highScore), (255,255,255), 150, 100)
            message_to_screen("Press Q to quit or C to play again", (255,255,255), 50, 0)
            if score >= highScore and score > 0:
                 message_to_screen("New High Score! :)", (255,0,255), 200, -100)
            
            #get high score, save high score to file
            if score > highScore:
                highScore = score
                scoreFile.seek(0)
                scoreFile.truncate()
                scoreFile.write(str(highScore))
                scoreFile.close()     
                
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameOver = False
                        gameExit = True
                    if event.key == pygame.K_c:
                        #reset game variables
                        groundX = 0
                        columnX = 800
                        columnY = 300
                        blockY = 200
                        enemyX = 10000
                        score = 0
                        accelerationY  = 0
                        velocity = 0
                        FPS = 30
                        gameOver = False
                        gameExit = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                        
    while gameOver == False:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jumpSound.play()
                    accelerationY = 14
                    velocity = 40
                if event.key == pygame.K_q:
                    gameOver = True
                    gameExit = True
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #jumping
        if accelerationY > 0:
            accelerationY -= 1
            velocity -= 3
        if accelerationY == 0:
            velocity = 0
        blockY -= velocity
        blockY += gravity

        #block and game display
        gameDisplay.fill((0,0,24))
        
        #display ground
        if groundX > -1600:
            groundX -= 5
        else:
            groundX = 0
        gameDisplay.blit(ground1, (groundX, 550)) 
        gameDisplay.blit(ground2, (groundX+1600, 550))
        
        #display moon
        if moonX > -200:
            moonX -= .25
        else:
            moonX = 800
        gameDisplay.blit(moon, (moonX, 200))
        #display bird
        if accelerationY > 0:
            gameDisplay.blit(bird2, [blockX,blockY,block_size,block_size])
        else:
            gameDisplay.blit(bird1, [blockX,blockY,block_size,block_size])

        #display enemy
        if enemyX > -100:
            enemyX -= 15
            enemyY += random.randrange(4)
            enemyY -= random.randrange(4)
        else:
            enemyX = 2500
            enemyY = random.randrange(100,500)
        gameDisplay.blit(enemy, [enemyX,enemyY,15,15])
                                                

        #columns score detection and regeneration
        if columnX > -100:
            columnX -= 10   
        else:
            columnX = 800
            columnY = random.randrange(375)
            columnColor = (random.randrange(255),random.randrange(200,255),random.randrange(100,255))
        columns(columnX, columnY)

        #falling off the screen detection
        if blockY > 600:
            gameOver = True
        #if blockY < 0:
        #    gameOver = True

        #collision detection
        if blockY < columnY and blockX > columnX and blockX < columnX + 100 or blockY + block_size < columnY and blockX + block_size > columnX and blockX + block_size < columnX + 100:
            gameOver = True
        if blockY > columnY+columnGap and blockX > columnX and blockX < columnX + 100 or blockY + block_size > columnY+columnGap and blockX + block_size > columnX and blockX + block_size < columnX + 100:
            gameOver = True

        #enemy collision detection
        if enemyX > blockX and enemyX < blockX + block_size and enemyY > blockY and enemyY < blockY + block_size:
            gameOver = True
        
        #score
        if columnX == 100:
            score += 1

        #increase fps
        if score == 5:
            FPS = 32
        elif score == 10:
            FPS = 34
        elif score == 15:
            FPS = 36
        elif score == 20:
            FPS = 38
        elif score == 25:
            FPS = 40
        elif score == 30:
            FPS = 42
        elif score == 35:
            FPS = 44
        elif score == 40:
            FPS = 46
        elif score == 45:
            FPS = 48
        elif score == 50:
            FPS = 50
        elif score == 55:
            FPS = 52
        elif score == 60:
            FPS = 54
        elif score == 65:
            FPS = 56
        elif score == 70:
            FPS = 58
        elif score == 75:
            FPS = 60
        
        scoreFunction(score, highScore)
        pygame.display.update()
        clock.tick(FPS)

pygame.display.update()
print(fps)
pygame.quit()
quit()
