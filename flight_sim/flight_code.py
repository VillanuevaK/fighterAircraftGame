import pygame
import sys
import math
import pygame.sprite as sprite
import pygame.gfxdraw
import os
from collections import deque
from pygame.locals import*
from random import randint


pygame.init() ##easy way to initialize all the imported pygame modules
high = 0

def start():
    displayHeight = 600
    displayWidth= 800
    pixelAmnt = displayWidth*displayHeight
    display = pygame.display.set_mode((displayWidth,displayHeight)) #opens window
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,-50" #used for placing display
    pygame.display.set_caption("Don't crash noob")#title
    white = [255, 255, 255]
    red = [255, 0, 0]
    black = [0,0,0]
    comicFont = pygame.font.SysFont("comicsansms",20)
    def text_objects(text, color):
        textSurface = comicFont.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def messageToScreen(msg, color, y_displace):
        textSurf, textRect = text_objects(msg, color)
        textRect.center = (displayWidth/2), (displayHeight/2)+y_displace
        display.blit(textSurf, textRect)
        
    startScreen = True
    while startScreen:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):    
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and event.key == K_c):
                gameLoop()##########
                startScreen = False
        display.fill(white)
        messageToScreen("welcom to flite simulater 3000",red,-50)
        messageToScreen("Press c to play", black, 0)
        pygame.display.update()


def gameLoop():
    #Set up
    gameOver = False
    gameOn= True
    stop = False
    
    displayHeight = 600
    displayWidth= 800
    pixelAmnt = displayWidth*displayHeight
    display = pygame.display.set_mode((displayWidth,displayHeight)) #opens window
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,-50" #used for placing display
    pygame.display.set_caption("Don't crash noob")#title
    white = [255, 255, 255]
    red = [255, 0, 0]
    black = [0,0,0]
    comicFont = pygame.font.SysFont("comicsansms",20)
    
    plane = pygame.image.load("plane2.png").convert_alpha()
    fuel = pygame.image.load("fuel.png").convert_alpha()
    missile = pygame.image.load("missile.png").convert_alpha()
    pepe = pygame.image.load("pepeWar.png").convert_alpha()
    print "plane size",plane.get_size()
    print "missile size",missile.get_size()
    print "fuel size",fuel.get_size()

    explosion9 = pygame.image.load("explosion.png").convert_alpha()
    explosion8 = pygame.image.load("explosion1.png").convert_alpha()
    explosion7 = pygame.image.load("explosion2.png").convert_alpha()
    explosion6 = pygame.image.load("explosion3.png").convert_alpha()
    explosion5 = pygame.image.load("explosion4.png").convert_alpha()
    explosion4 = pygame.image.load("explosion5.png").convert_alpha()
    explosion3 = pygame.image.load("explosion6.png").convert_alpha()
    explosion2 = pygame.image.load("explosion7.png").convert_alpha()
    explosion1 = pygame.image.load("explosion8.png").convert_alpha()
    explosion = pygame.image.load("explosion9.png").convert_alpha()

    #scrolling background stuff
    clock = pygame.time.Clock()#time in miliseconds, clock tracks time, useful for frame rate
    fps =120 #BetterThanCOD
    backG = pygame.image.load("warBackground.png").convert() #loads background and converts into image for pygame
    posX = 0 

    #Events
    def handleEvents(): #event queue - what to do with given events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):    
    #if the event type is QUIT (you press upper left x) or press escape (down means just when the key is being pressed as apposed to KEYUP which is when u let it go)
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and event.key == K_c):
                gameLoop()

    class Player(pygame.sprite.Sprite):   
        def init(self):
            self.fuelCount=30
        def reduceFuel(self, y):
            if self.fuelCount > 0:
                self.fuelCount += y
        def fuelLeft(self):
            return self.fuelCount
        @property
        def image(self):
            return plane#NOTE IF COLLISION DETECTION FAILS, PROB BC THIS
        @property
        def rect(self):
            return Rect(self.x,self.y,174,28)#174,30
        def setLocation(self, x, y):
            self.x = x
            self.y = y
        def keys(self):
            k = pygame.key.get_pressed()
            
            if k[K_LEFT] and self.x < 0:
                self.x-=0
            elif k[K_LEFT]:
                self.x-=5#5
                
            if k[K_RIGHT] and self.x > 605:
                self.x+=0   
            elif k[K_RIGHT]:
                self.x+=5#5
                                                                                                                                                                        
            if k[K_DOWN] and self.y > 550:
                self.y+=0
            elif k[K_DOWN]:
                self.y+=3#3
                               
            if self.fuelCount>0:
                if k[K_UP] and self.y < 0:
                    self.y-=0
                elif k[K_UP]:
                    self.y-=5
                
        def down(self):
            self.y+=0.5
        def left(self):
            self.x-=0.3
                
        def draw(self):
            display = pygame.display.get_surface()
            display.blit(plane,(self.x,self.y))
        def do(self):
            self.draw()
            if stop != True:
                self.keys()
                self.down()
                self.left()
        def posY(self):
            if self.y > 590:
                return True
        def posX(self):
            if self.x < -150:
                return True

    p = Player()
    p.init()
    p.setLocation(100,100)

    class Objects(pygame.sprite.Sprite):
        def setLocation(self, xPos, yPos):
            self.xPos = xPos
            self.yPos = yPos
        @property
        def image(self):
            return missile
        @property
        def rect(self):
            return Rect(self.xPos,self.yPos,78,7) #78,10
        def displayMissile(self):
            display = pygame.display.get_surface()
            display.blit(missile,(self.xPos,self.yPos))
        def move(self):
            self.xPos -= 7.4#7
        def collision(self, p):
            return pygame.sprite.collide_rect(self, p)
        def doM(self, p):
            if stop != True:
                self.move()
            self.displayMissile()
            self.collision(p)
        @property
        def imageFuel(self):
            return fuel
        @property
        def rectFuel(self):
            return Rect(self.xPos, self.yPos, 70, 70)
        def displayFuel(self):
            display = pygame.display.get_surface()
            display.blit(fuel,(self.xPos,self.yPos))
        def moveFuel(self):
            self.xPos -= 4
        def doF(self, p):
            if stop != True:
                self.moveFuel()
            self.displayFuel()
            self.collision(p)
        def away(self,p):
            if self.xPos>p.x:
                self.xPos+=10
            else:
                self.xPos-=10
            if self.yPos>p.y:
                self.yPos+=10
            else:
                self.yPos-=10
        @property
        def imagePepe(self):
            return pepe
        def displayPepe(self):
            display = pygame.display.get_surface()
            display.blit(pepe,(self.xPos,self.yPos))
        def doP(self, p):
            if stop != True:
                self.moveFuel()
            self.displayPepe()
            self.collision(p)
    pepes = list()
    fuels = list()
                

    def text_objects(text, color):
        textSurface = comicFont.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def messageToScreen(msg, color, y_displace):
        textSurf, textRect = text_objects(msg, color)
        textRect.center = (displayWidth/2), (displayHeight/2)+y_displace
        display.blit(textSurf, textRect)

    missiles = list() #collection of missiles       
    
    frameClock = 0
    realClock = 0
    cond1 = False
    cond2 = False
    cond3 = False
    cond4 = False
    cond5 = False
    cond6 = False
    cond7 = False
    cond8 = False
    cond9 = False
    cond10 = False
    missileCollision=False
    moses = False
    clock3=0
    global high 
    while gameOn:#loops while game is happening
        handleEvents() #key presses and what not

        #NOTE: THINGS THAT ARE INFRONT GO IN DOWN TO UP ORDER
        

        #Background movement
        if stop != True:
            posX -= 3 #moves background image
            if moses:
                posX -=6
        
        relativePosX = posX%backG.get_rect().width #stops bluring from happening
                            #\/ subtract to have moving image in correct window
        display.blit(backG,(relativePosX - backG.get_rect().width,0))#blit just copies image and moves it slightly almost as if movement is occuring
        if relativePosX < displayWidth:
            display.blit(backG,(relativePosX,0))#Moves back to start to help stop more bluring

        
        p.do() #plane stuff

        if(frameClock%30==0):#missile stuff
            missileYpos = randint(0,600)
            m = Objects()
            m.setLocation(820,missileYpos)
            missiles.append(m)
        for mis in missiles:
            mis.doM(p)
            if moses:
                if ((abs(mis.yPos-p.y)<70)):
                    mis.away(p)
                if (abs(mis.xPos-p.x)<70):
                    display.blit(explosion9,(mis.xPos,mis.yPos))
                    missiles.remove(mis)
            if stop:
                mis.away(p)
            if mis.collision(p):
                missileCollision = True
        if missileCollision or p.posY() or p.posX():
            stop = True
            realClock += 1
            if(realClock%1==0):
                cond1 = True
            if cond1 == True:  
                display.blit(explosion,(p.x,p.y-80))
            if(realClock%2==0):
                cond2 = True
            if cond2== True:
                display.blit(explosion1,(p.x,p.y-80))
            if(realClock%3==0):
                cond3 =True
            if cond3 == True:
                display.blit(explosion2,(p.x,p.y-80))
            if(realClock%4==0):
                cond4 = True
            if cond4 == True:
                display.blit(explosion3,(p.x-10,p.y-89))
            if(realClock%5==0):
                cond5 = True
            if cond5 == True:
                display.blit(explosion4,(p.x-14,p.y-90))
            if(realClock%6==0):
                cond6 = True
            if cond6 == True:
                display.blit(explosion5,(p.x-16,p.y-90))
            if(realClock%7==0):
                cond7 = True
            if cond7 == True:
                display.blit(explosion6,(p.x-20,p.y-94))
            if(realClock%8==0):
                cond8 = True
            if cond8 == True:
                display.blit(explosion7,(p.x-18,p.y-90))
            if(realClock%9==0):
                cond9= True
            if cond9 == True:
                display.blit(explosion8,(p.x-17,p.y-90))
            if(realClock%10==0):
                cond10 = True
            if cond10 == True:
                display.blit(explosion9,(p.x-16,p.y-90))
            if(realClock%50==0):
                gameOver = True
                gameOn= False
                startScreen= False

        messageToScreen(str(frameClock),red,-250)

        if(frameClock%800==0):
            fuelYpos = randint(0,600)
            f = Objects()
            f.setLocation(820,fuelYpos)
            fuels.append(f)
        for fuse in fuels:
            fuse.doF(p)
            if(fuse.collision(p)):
                p.reduceFuel(10)
                fuels.remove(fuse)
            if stop:
                fuse.away(p)
                
        if(frameClock%1000==0):
            fuelYpos = randint(0,600)
            pe = Objects()
            pe.setLocation(820,fuelYpos)
            pepes.append(pe)
        for peps in pepes:
            peps.doP(p)
            if(peps.collision(p)):
                moses = True
                pepes.remove(peps)
            if stop:
                peps.away(p)
            
        
        messageToScreen("Fuel left: "+str(p.fuelLeft()),red, -230)
        if(frameClock%50==0):
            p.reduceFuel(-1)

        pygame.display.update()#updates portions of the screen or the whole screen if no arguments are passed
        #^also stops the flickering that worse languages like java have
        clock.tick(fps)#max fps it will go
        if(moses):
            clock3+=1
        if stop != True:
            frameClock+=1
        if(clock3==400):
            moses = False
            clock3=0
    
    while gameOver:
        handleEvents()
        display.fill(white)
        if frameClock>high:
            high = frameClock
        messageToScreen("you died",red,-50)
        messageToScreen("Press c to play again or escape to quit", black, 0)
        messageToScreen(str(frameClock),red,-250)
        messageToScreen("highscore: "+str(high),red,-200)
        pygame.display.update()
start()


