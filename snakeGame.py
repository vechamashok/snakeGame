import pygame
import sys
import random

pygame.init()
HIGHSCORE = 0

# Select the speed of snake in game
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
snakeSpeed = 15

blackcolor = (0, 0, 0)
whitecolor = (255,255,255)
greencolor = (0, 255, 0)
redcolor = (255, 0, 0)
bluecolor = (0, 0, 255)
yellowcolor = (255, 255, 0)
windowWidth = 600
windowHeight = 600
snakeBlock = 10
snakeWidth = 15
appleSize = 15
topGap = 40
small_font = pygame.font.SysFont('Courier New', 25)
medium_font = pygame.font.SysFont('Courier New', 20, True)
large_font = pygame.font.SysFont('Courier New', 40, True, True)
clock = pygame.time.Clock()

background = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Snake Game')
snake_img = pygame.image.load('head.png')
apple_img = pygame.image.load('apple2.png')
tail_img = pygame.image.load('tail1.png')
play_img = pygame.image.load('play.png')
playrect = play_img.get_rect()
pause_img = pygame.image.load('pause.png')
pauserect = pause_img.get_rect()
whitecolor_img = pygame.image.load('white.png')

def start():
    background.fill(whitecolor)
    welcomeFont = large_font.render("Welcome to snake game", True, bluecolor)
    startGame = medium_font.render("Play Game", True, blackcolor, greencolor)
    quitGame = medium_font.render("Quit", True, redcolor, greencolor)

    welcomeFont_rect = welcomeFont.get_rect()
    startGame_rect = startGame.get_rect()
    quitGame_rect = quitGame.get_rect()
    
    welcomeFont_rect.center = (windowWidth/2, windowHeight/2 - 100)
    startGame_rect.center = (windowWidth/3 + 100, windowHeight/2 + 50)
    quitGame_rect.center = (windowWidth/3 + 100, windowHeight/2 + 100)
    
    background.blit(welcomeFont, welcomeFont_rect)
    background.blit(startGame, startGame_rect)
    background.blit(quitGame, quitGame_rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    gameloop()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x > startGame_rect.left and x < startGame_rect.right:
                    if y > startGame_rect.top and y < startGame_rect.bottom:
                        gameloop()
                if x > quitGame_rect.left and x < quitGame_rect.right:
                    if y > quitGame_rect.top and y < quitGame_rect.bottom:
                        pygame.quit()
                        sys.exit()

        pygame.display.update()

def gameover():
    global HIGHSCORE
    
    gameoverMsg = large_font.render('GAME OVER', True, redcolor)
    highScore = small_font.render("High Score : " + str(HIGHSCORE),True,bluecolor)
    
    playAgainMsg = medium_font.render("Press P to Play Again",True, greencolor)
    resetScoreMsg = medium_font.render("Press R to Reset the game Score & play",True,bluecolor)
    quitMsg = medium_font.render("Press Q to Quit the game",True,redcolor)

    background.blit(gameoverMsg, [windowWidth/3, windowHeight/3])
    background.blit(playAgainMsg, [windowWidth / 3 - 50, windowHeight / 3 + 50])
    background.blit(resetScoreMsg, [windowWidth / 3 - 100, windowHeight / 3 + 100])
    background.blit(quitMsg, [windowWidth / 3 - 50, windowHeight / 3 + 150])
    background.blit(whitecolor_img, (windowWidth - 50, 0))
    background.blit(highScore,(windowWidth / 3,10))
    
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    gameloop()
                if event.key == pygame.K_r:
                    HIGHSCORE = 0
                    gameloop()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

# For moving/rotating the head and tail of the snake
def snake(snakelist, direction):

    if direction == 'right':
        head = pygame.transform.rotate(snake_img, 270)
        tail = pygame.transform.rotate(tail_img, 270)
    if direction == 'left':
        head = pygame.transform.rotate(snake_img, 90)
        tail = pygame.transform.rotate(tail_img, 90)
    if direction == 'up':
        head = pygame.transform.rotate(snake_img, 0)
        tail = pygame.transform.rotate(tail_img, 0)
    if direction == 'down':
        head = pygame.transform.rotate(snake_img, 180)
        tail = pygame.transform.rotate(tail_img, 180)

    background.blit(head, snakelist[-1])
    background.blit(tail, snakelist[0])

    #Creating the body for the snake using rect function
    for XnY in snakelist[1:-1]:
        pygame.draw.rect(background, bluecolor, (XnY[0], XnY[1], snakeWidth, snakeWidth))


def pauseGame():

    paused_font1 = large_font.render("Game Paused", True, redcolor)
    quitMsg = medium_font.render("Press Q to Quit the game",True,redcolor)
    paused_font_rect1 = paused_font1.get_rect()
    paused_font_rect1.center = (windowWidth/2, windowHeight/2)
    background.blit(paused_font1, paused_font_rect1)
    background.blit(quitMsg,[windowWidth/3 - 50, windowHeight/2 + 50])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x > (windowWidth - 50) and x < windowWidth:
                    if y > 0 and y < 50:
                        return        
        pygame.display.update()

#Main logic
def gameloop():

    while True:

        X = windowWidth / 2 # Starting position of the snake
        Y = windowHeight / 2
        global HIGHSCORE
        direction = 'right'
        score = small_font.render("Score:0", True, bluecolor)
        food_X = random.randrange(0, windowWidth - 10, 10)
        food_Y = random.randrange(topGap, windowHeight - 10, 10)
        snakelist = []
        snakelength = 3

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # To restrict instantaneous movement of snake
                    if event.key == pygame.K_LEFT:
                        if direction == 'right':
                            pass
                        else:
                            direction = 'left'
                    if event.key == pygame.K_RIGHT:
                        if direction == 'left':
                            pass
                        else:
                            direction = 'right'
                    if event.key == pygame.K_UP:
                        if direction == 'down':
                            pass
                        else:
                            direction = 'up'
                    if event.key == pygame.K_DOWN:
                        if direction == 'up':
                            pass
                        else:
                            direction = 'down'
                # To Pause the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pause_xy = event.pos
                    if pause_xy[0] > (windowWidth - 50) and pause_xy[0] < windowWidth:
                        if pause_xy[1] > 0 and pause_xy[1] < 50:
                            background.blit(play_img, (windowWidth - 50, 0))
                            pauseGame()
            if direction == 'up':
                Y -= snakeBlock
                if Y < topGap:
                    gameover()
            if direction == 'down':
                Y += snakeBlock
                if Y > windowHeight - snakeWidth:
                    gameover()
            if direction == 'right':
                X += snakeBlock
                if X > windowWidth - snakeWidth:
                    gameover()
            if direction == 'left':
                X -= snakeBlock
                if X < 0:
                    gameover()
                            
            snakehead = []
            snakehead.append(X)
            snakehead.append(Y)
            snakelist.append(snakehead)

            snake_head_rect = pygame.Rect(X, Y, snakeWidth, snakeWidth)
            apple_rect = pygame.Rect(food_X, food_Y, appleSize, appleSize)

            # Game over if the snake touches itself
            if len(snakelist) > snakelength:
                del snakelist[0]
            for point in snakelist[:-1]:
                if point == snakehead:
                    gameover()

            background.fill(whitecolor)

            snake(snakelist, direction)
            if snake_head_rect.colliderect(apple_rect):
                food_X = random.randrange(0, windowWidth - 10, 10)
                food_Y = random.randrange(topGap, windowHeight - 10, 10)
                snakelength += 1
                score = small_font.render("Score:" + str(snakelength - 3), True, bluecolor)

            background.blit(score, (20, 10))
            if (snakelength - 3) > HIGHSCORE:
                HIGHSCORE = snakelength - 3
            pygame.draw.line(background, greencolor, (0, topGap), (windowWidth, topGap))
            background.blit(pause_img, (windowWidth - 50, 0))
            background.blit(apple_img, (food_X, food_Y))
            
            pygame.display.update()

            clock.tick(snakeSpeed)

start()
gameloop()
