import pygame, sys, time, random
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()

#Constant of the board of the game
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
SIZESIDES = 20
MIDDLESIZE = 10

#Speed of the game constants
FPS = 40
PADDLESPEED = 20

#Rects of the board of the game
TOPSIDE = pygame.Rect(0, 0, WINDOWWIDTH, SIZESIDES)
BOTTOMSIDE = pygame.Rect(0, WINDOWHEIGHT - SIZESIDES, WINDOWWIDTH, SIZESIDES)
MIDDLE = []
for i in range(0, 31):
    MIDDLE.append(pygame.Rect(WINDOWWIDTH/2 - MIDDLESIZE/2,15 + i*20, MIDDLESIZE, MIDDLESIZE))    

windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

pygame.display.set_caption('Running_window')

BLACK = (0, 0, 0)
DEEPSKYBLUE = (0,191,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
LIMEGREEN = (50,205,50)
RED = (255,0,0)


gameIsPlaying = False

#These are used to print the scores
CHIFFRES =[
'''WWWWW
W   W
W   W
W   W
WWWWW''',
'''    W
    W
    W
    W
    W''',
'''WWWWW
    W
WWWWW
W    
WWWWW''',
'''WWWWW
    W
WWWWW
    W
WWWWW''',
'''W   W
W   W
WWWWW
    W
    W''',
'''WWWWW
W    
WWWWW
    W
WWWWW''',
'''WWWWW
W    
WWWWW
W   W
WWWWW''',
'''WWWWW
    W
  WWW
    W
    W''',
'''WWWWW
W   W
WWWWW
W   W
WWWWW''',
'''WWWWW
W   W
WWWWW
    W
WWWWW''',
'''''']

#Functions

    #Draw the score (in fact return a list with the rect to draw, drawn later with drawGame())
def drawChiffre(a, x, y):
    countx = 0
    county = 0
    rectList = []
    for piece in CHIFFRES[a]:
        if countx % 7 == 5 or countx % 7 == 6:
            countx +=1
            county +=0.5
        if piece == '''W''':
            rectList.append(pygame.Rect(x + (countx%7)*10, y + county*15, MIDDLESIZE, MIDDLESIZE*1.5))
            countx +=1
        elif piece == ''' ''':
            countx +=1
    return rectList

    #Doesn't work, meant to change the score in case of a win from either side
def score(ball, scoreP1, scoreP2):
    if ball.l <= 0:
        scoreP1 +=1
        ball = Ball(WINDOWHEIGHT/2, WINDOWWIDTH/2, 15, 15, 5, 5)
    if ball.l >= WINDOWWIDTH:
        scoreP2 +=1
        ball = Ball(WINDOWHEIGHT/2, WINDOWWIDTH/2, 15, 15, 5, 5)

    #This function draws everything in the game. 
def drawGame(Paddle1, scoreP1, Paddle2, scoreP2, Ball):
    windowSurface.fill(BLACK)

    Paddle1.draw()
    Paddle2.draw()
    Ball.draw() 

    drawScoreP2 = drawChiffre(scoreP2, 450, 50)
    for piece in drawScoreP2:
        pygame.draw.rect(windowSurface, LIMEGREEN, piece)

    drawScoreP1 = drawChiffre(scoreP1, 300, 50)
    for piece in drawScoreP1:
        pygame.draw.rect(windowSurface, YELLOW, piece)
        
    pygame.draw.rect(windowSurface, WHITE, TOPSIDE) 
    pygame.draw.rect(windowSurface, WHITE, BOTTOMSIDE)

    for piece in MIDDLE :
        pygame.draw.rect(windowSurface, WHITE, piece)

    pygame.display.update()

    #A function for writing a text with the most basic font
def write(text, fontSize, x, y):
    font = pygame.font.SysFont(None, fontSize)
    
    textR = font.render(text, True, DEEPSKYBLUE, None)
    textRect = textR.get_rect()
    textRect.centerx = x
    textRect.centery = y
    windowSurface.blit(textR, textRect)

#Classes
        
    #The paddles
class Paddle:
    rect = pygame.Rect(0, 0, 0, 0)
    movement = 0

    def __init__(self, l, t, w, h):
        self.l = l
        self.t = t
        self.w = w
        self.h = h
    def setRect(self):
        self.rect = pygame.Rect(self.l, self.t, self.w, self.h)
    def setPosition(self):
        self.position = self.t
    def setMovement(self, x):
        self.movement = x
    def move(self):
        self.t = self.t + self.movement*PADDLESPEED
        self.setPosition()
        self.setRect()
    def draw(self):
        pygame.draw.rect(windowSurface, WHITE, self.rect)
    def collideWithSide(self, upSide, downSide):
        if (self.t + self.h) > downSide:
            self.setMovement(0)
        if (self.t) < upSide:
            self.setMovement(0)

    #The ball
class Ball:
    rect = pygame.Rect(0, 0, 0, 0)
    position = [0, 0]

    def __init__(self, l, t, w, h, x, y):
        self.speed = [x, y]
        self.l = l
        self.t = t
        self.w = w
        self.h = h
    def setRect(self):
        self.rect = pygame.Rect(self.l, self.t, self.w, self.h)
    def setPosition(self):
        self.position = [self.l, self.t]
    def setSpeed(self, x, y):
        self.speed = [x, y]
    def draw(self):
        pygame.draw.rect(windowSurface, RED, self.rect)
    def move(self):
        self.l = self.l + self.speed[0]
        self.t = self.t + self.speed[1]
        self.setRect()
        self.setPosition()
    def bounce(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.setSpeed(-self.speed[0], self.speed[1])
    def collideWithSide(self, upSide, downSide):
        if (self.t + self.h) > downSide or (self.t) < upSide:
            self.setSpeed(self.speed[0], -self.speed[1])

#Now the core of the game
while True:

    #Initialization of the score and of the paddles and ball
    scoreP1 = 0
    scoreP2 = 0

    paddle1 = Paddle(0, WINDOWHEIGHT/2 - 40, 15, 80)
    paddle2 = Paddle(WINDOWWIDTH - 15, WINDOWHEIGHT/2 - 40, 15, 80)
    ball = Ball(WINDOWWIDTH/2, WINDOWHEIGHT/2, 15, 15, 5, 5)

    #This is the "menu"
    while not gameIsPlaying:
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == ord('s'):
                        gameIsPlaying = True
                if event.type == KEYUP:
                    if event.key == ord('q'):
                        pygame.quit()
                        sys.exit()
        

        drawGame(paddle1, scoreP1, paddle2, scoreP2, ball)

        write('Press s', 120, WINDOWWIDTH/4, WINDOWHEIGHT/2)
        write('to play!', 120, 3*WINDOWWIDTH/4, WINDOWHEIGHT/2)

        write('Press q', 60, 3*WINDOWWIDTH/8, 3*WINDOWHEIGHT/4)
        write('to quit.', 60, 5*WINDOWWIDTH/8, 3*WINDOWHEIGHT/4)

        write('UP', 30, 20, WINDOWHEIGHT/4)
        write('DOWN', 30, 36, 3*WINDOWHEIGHT/4)
        
        write('e', 60, WINDOWWIDTH - 15, WINDOWHEIGHT/4)
        write('d', 60, WINDOWWIDTH - 15, 3*WINDOWHEIGHT/4)

        pygame.display.update()
        mainClock.tick(FPS)
        
    #This is the game playing
    while gameIsPlaying:

    
    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == ord('a'):
                    gameIsPlaying = False
                if event.key == K_UP:
                    paddle1.setMovement(-1)
                if event.key == K_DOWN:
                    paddle1.setMovement(1)
                if event.key == ord('e'):
                    paddle2.setMovement(-1)
                if event.key == ord('d'):
                    paddle2.setMovement(1)
            if event.type == KEYUP:
                if event.key == K_UP:
                    paddle1.setMovement(0)
                if event.key == K_DOWN:
                    paddle1.setMovement(0)
                if event.key == ord('e'):
                    paddle2.setMovement(0)
                if event.key == ord('d'):
                    paddle2.setMovement(0)
                

        #Move the ball and the paddles
        paddle1.move()
        paddle2.move()
        ball.move()

        #Collision between the ball and the paddles
        ball.bounce(paddle1)
        ball.bounce(paddle2)

        #Check if score and incrementation
        if ball.l <= 0:
            scoreP2 +=1
            ball = Ball(WINDOWWIDTH/2, WINDOWHEIGHT/2, 15, 15, random.randint(3, 5), random.randint(3, 5))
        if ball.l >= WINDOWWIDTH:
            scoreP1 +=1
            ball = Ball(WINDOWWIDTH/2, WINDOWHEIGHT/2, 15, 15, random.randint(3, 5), random.randint(3, 5))

        #Check if winner and displaying and back to the menu
        if scoreP1 >= 10:
            write('YOU WIN', 60, WINDOWWIDTH/8, 2*WINDOWHEIGHT/8)
            pygame.display.update()
            time.sleep(1)
            gameIsPlaying = False

        if scoreP2 >= 10:
            write('YOU WIN', 60, 5*WINDOWWIDTH/8, 2*WINDOWHEIGHT/8)
            pygame.display.update()
            time.sleep(1)
            gameIsPlaying = False
            
        #Collision of the paddles and the ball with the sides
        paddle1.collideWithSide(20, 580)
        paddle2.collideWithSide(20, 580)
        ball.collideWithSide(20, 580)

        
        drawGame(paddle1, scoreP1, paddle2, scoreP2, ball)

        #Acceleration of the ball
        ball.setSpeed(ball.speed[0]*1.002 , ball.speed[1])

        write('Press escape to give up this game', 15, WINDOWWIDTH/8, WINDOWHEIGHT-SIZESIDES*2)

        pygame.display.update()
        mainClock.tick(FPS)

    pygame.display.update()
    mainClock.tick(FPS)