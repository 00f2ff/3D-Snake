from visual import *
from visual.controls import *
import random

"""
3D Snake by Duncan McIsaac

Citations:
VPython by Bruce Sherwood

Notes:
# I couldn't figure out how pickle works so the highscore list is local.
# This wasn't linted. I'm sorry.
"""



class PrismSnake(object):
    def __init__(self):
        print """
        ~~~~~ 3D SNAKE ~~~~~
        Instructions:
        WASD to move, mouse + right-click to rotate.
        Auto Resize:
         On:  Prism will resize in different directions as you eat food
         Off: Prism will not resize
        Pause: press 'p'
        Restart: press 'r'
        Important:
        1. On the positive and negative Y sides, controls are inverted.
        2. Auto Resize is 'On' by default.
        3. Auto Resize makes the game lag, so snake motion will not appear as
           fluid as it does when Auto Resize is off, and when you lose you might
           need to click on the screen to make the window respond.
        4. There is code to display high scores in the main file, however
           VPython runs through functions so many different times that data will
           be sent through the functions enough to skew the actual high score
           list. 
        
        Select resize setting, click on game window, and press 'p' to begin.
        """
        self.highScoreList = [1,1,1,1,1]
        self.initALL()

    def initALL(self):
        self.snake = []
        self.food = [0,0,0,0,0,0]
        self.range = 30
        self.isGameOver = False
        self.isPaused = True
        
        self.score = 0
        
        self.tempX = 20
        self.tempY = 20
        self.tempZ = 20
        # Only works with even values
        self.drawPrism_and_Score()
        
        self.prism.length = 20 # Might be redundant data
        self.prism.height = 20
        self.prism.width = 20
        
        # These need to be even
        self.deltaX = 0
        self.deltaY = 0
        self.deltaZ = 0
        
        self.xInfo = 0
        self.yInfo = 0
        self.zInfo = 0
        
        self.initInfo()
        self.dimensionControl = 'On'
        # This makes it so food does not occupy the
        # space which fails the autoResize
        self.initSnakeHead()
        self.placeFood()
        
        #self.pause_unpause()

        self.w = 450
        c = controls(x=self.w-19, y=0, width=self.w, height=self.w, range=50)
        m = menu(pos=(0,-20,0), height=8, width=50, text='Auto Resize')
        m.items.append(('On', lambda: toggleControl('On')))
        m.items.append(('Off', lambda: toggleControl('Off')))
        
        # Try to put high score list on here

        def toggleControl(state):
            if (state == 'On'):
                self.dimensionControl = 'On'
            else:
                self.dimensionControl = 'Off'
            #.value means 'On'

        self.run()


    def autoResize(self):
        a = random.randint(0,2)
        bigChangeList = [8,12,16,20]
        b = random.randint(0,3)
        bcl = bigChangeList[b]
        #change = random.randint(2,10)
        change = 2
        # has to be even because taken off both sides equally
        self.aList = [self.prism.length,self.prism.height,self.prism.width]
        while ((a == 0) and (abs(self.head.pos.x) == self.xc) or
               (a == 1) and (abs(self.head.pos.y) == self.yc) or
               (a == 2) and (abs(self.head.pos.z) == self.zc)):
            a = random.randint(0,2)
        if ((a == 0) and (((self.head.pos.y <= self.yc-change) and
            (self.head.pos.y >= -self.yc+change)) or
            ((self.head.pos.z <= self.zc-change) and
            (self.head.pos.z >= -self.zc+change)))):
            if (self.prism.length > 4 + change):
                self.prism.length -= change
            else: self.prism.length += bcl
            self.replaceInfo()
        elif ((a == 1) and (((self.head.pos.x <= self.xc-change) and
              (self.head.pos.x >= -self.xc+change)) or
              ((self.head.pos.z <= self.zc-change) and
              (self.head.pos.z >= -self.zc+change)))):
            if (self.prism.height > 4 + change):
                self.prism.height -= change
            else: self.prism.height += bcl
            self.replaceInfo()
        elif ((a == 2) and (((self.head.pos.x <= self.xc-change) and
              (self.head.pos.x >= -self.xc+change)) or
              ((self.head.pos.y <= self.yc-change) and
              (self.head.pos.y >= -self.yc+change)))):
            if (self.prism.width > 4 + change):
                self.prism.width -= change
            else: self.prism.width += bcl
            self.replaceInfo()
        else: pass
        
        

    def drawPrism_and_Score(self):
        self.prism = box(pos=(0,0,0), length=self.tempX, height=self.tempY,
                         width=self.tempZ)
        self.scoreLabel = label(pos=(-self.range/2.2,self.range/1.8,0),
                                text='Score: %d' % self.score, box=False)

    def replaceInfo(self):
        self.initInfo()
        for obj in self.food:
            obj.visible = False
            del obj
        self.placeFood()
        self.updateSnake()
        self.run()
        

    def initInfo(self):
        self.r = 1
        self.xb = self.prism.length / 2 # default of location information
        self.yb = self.prism.height / 2
        self.zb = self.prism.width / 2
        self.xc = self.xb + self.r # sphere location
        self.yc = self.yb + self.r
        self.zc = self.zb + self.r
        self.v = 1
        self.pauseV = self.v
        

    def initSnakeHead(self):
        #n = random.randint(-self.xb+1,self.xb-1)
        #m = random.randint(-self.yb+1,self.yb-1)
        #self.head = sphere(pos=(n,m,self.zc), radius=self.r, color=color.blue)
        self.head = sphere(pos=(0,0,self.zc), radius=self.r, color=color.blue)
        self.snake += [self.head]
        self.xVect = self.v
        self.yVect = 0
        self.zVect = 0
        self.head.velocity = vector(self.xVect,self.yVect,self.zVect)


    """ END INIT INFO """

    def placeFood(self):
        self.foodPosZ()
        self.foodNegZ()
        self.foodPosX()
        self.foodNegX()
        self.foodPosY()
        self.foodNegY()
        for i in self.snake: # Checks to make sure food is not on snake
            # This will only run through once. A while loop would make it
            # perfect but slow everything down.
            if (self.fpz.pos == i.pos):
                self.fpz.visible = False
                del self.fpz
                self.foodPosZ()
            elif (self.fnz.pos == i.pos):
                self.fnz.visible = False
                del self.fnz
                self.foodNegZ()
            elif (self.fpx.pos == i.pos):
                self.fpx.visible = False
                del self.fpx
                self.foodPosX()
            elif (self.fnx.pos == i.pos):
                self.fnx.visible = False
                del self.fnx
                self.foodNegX()
            elif (self.fpy.pos == i.pos):
                self.fpy.visible = False
                del self.fpy
                self.foodPosY()
            elif (self.fny.pos == i.pos):
                self.fny.visible = False
                del self.fny
                self.foodNegY()
    
    def foodPosZ(self): # randints are restricted to not include next to edge.
        if (self.dimensionControl == 'On'): d = 2
        else: d = 1
        x = random.randint(-self.xb+d,self.xb-d)
        y = random.randint(-self.yb+d,self.yb-d)
        self.fpz = sphere(pos=(x,y,self.zc), radius=self.r, color=color.green)
        self.food[0] = self.fpz

    def foodNegZ(self):
        if (self.dimensionControl == 'On'): d = 2
        else: d = 1
        x = random.randint(-self.xb+d,self.xb-d)
        y = random.randint(-self.yb+d,self.yb-d)
        self.fnz = sphere(pos=(x,y,-self.zc), radius=self.r, color=color.green)
        self.food[1] = self.fnz

    def foodPosX(self):
        if (self.dimensionControl == 'On'): d = 2
        else: d = 1
        y = random.randint(-self.yb+d,self.yb-d)
        z = random.randint(-self.zb+d,self.zb-d)
        self.fpx = sphere(pos=(self.xc,y,z), radius=self.r, color=color.green)
        self.food[2] = self.fpx

    def foodNegX(self):
        if (self.dimensionControl == 'On'): d = 2
        else: d = 1
        y = random.randint(-self.yb+d,self.yb-d)
        z = random.randint(-self.zb+d,self.zb-d)
        self.fnx = sphere(pos=(-self.xc,y,z), radius=self.r, color=color.green)
        self.food[3] = self.fnx

    def foodPosY(self):
        if (self.dimensionControl == 'On'): d = 2
        else: d = 1
        x = random.randint(-self.xb+d,self.xb-d)
        z = random.randint(-self.zb+d,self.zb-d)
        self.fpy = sphere(pos=(x,self.yc,z), radius=self.r, color=color.green)
        self.food[4] = self.fpy

    def foodNegY(self):
        if (self.dimensionControl == 'On'): d = 2
        else: d = 1
        x = random.randint(-self.xb+d,self.xb-d)
        z = random.randint(-self.zb+d,self.zb-d)
        self.fny = sphere(pos=(x,-self.yc,z), radius=self.r, color=color.green)
        self.food[5] = self.fny

    def eatFood(self): 
        # When food is eaten, generates new food and calls the function that
        # extends the snake (and increases the score)
        if (self.head.pos == self.fpz.pos):
            self.fpz.visible = False
            del self.fpz
            self.addBody()
            self.foodPosZ()
            if (self.dimensionControl == 'On'):
                self.autoResize()
        elif (self.head.pos == self.fnz.pos):
            self.fnz.visible = False
            del self.fnz
            self.addBody()
            self.foodNegZ()
            if (self.dimensionControl == 'On'):
                self.autoResize()
        elif (self.head.pos == self.fpx.pos):
            self.fpx.visible = False
            del self.fpx
            self.addBody()
            self.foodPosX()
            if (self.dimensionControl == 'On'):
                self.autoResize()
        elif (self.head.pos == self.fnx.pos):
            self.fnx.visible = False
            del self.fnx
            self.addBody()
            self.foodNegX()
            if (self.dimensionControl == 'On'):
                self.autoResize()
        elif (self.head.pos == self.fpy.pos):
            self.fpy.visible = False
            del self.fpy
            self.addBody()
            self.foodPosY()
            if (self.dimensionControl == 'On'):
                self.autoResize()
        elif (self.head.pos == self.fny.pos):
            self.fny.visible = False
            del self.fny
            self.addBody()
            self.foodNegY()
            if (self.dimensionControl == 'On'):
                self.autoResize()

    """ END FOOD STUFF """

    def updateSnake(self):
        if (len(self.snake) == 1): pass
        else:
            for i in xrange(len(self.snake)-1,0,-1):
                self.snake[i].pos = self.snake[i-1].pos

    def addBody(self):
        # This takes the suggestion of adding more to the body because of a big
        # playing surface
        self.score += 1
        self.showScore()
        oldTail = self.snake[-1]
        self.snake += [sphere(pos=oldTail.pos, radius=self.r/1.5,
                                 color=color.blue)]
        oldTail = self.snake[-1]
        self.snake += [sphere(pos=oldTail.pos, radius=self.r/1.5,
                                 color=color.blue)]
        oldTail = self.snake[-1]
        self.snake += [sphere(pos=oldTail.pos, radius=self.r/1.5,
                                 color=color.blue)]

    def showScore(self):
        self.scoreLabel.text='Score: %d' % self.score

    def moveSnake(self,event):
        # Depending on how the cube is rotated, inverting keyboard controls
        # doesn't always work.
        # That just makes it harder. I've laid out how I expect controls to
        # invert, however I can't account for everything, which just makes the
        # game hard, but it isn't an issue. I don't think there's a way for
        # VPython to know in what direction you're looking at your object.
        x = self.head.pos.x
        y = self.head.pos.y
        z = self.head.pos.z
        press = event.key
        if (self.isPaused == False):
            if ((z == self.zc) and (x > -self.xb) and (x < self.xb) and
                (y > -self.yb) and (y < self.yb)):
                self.moveOnPosZ(press)
                self.updateSnake()
            elif ((z == -self.zc) and (x > -self.xb) and (x < self.xb) and
                (y > -self.yb) and (y < self.yb)):
                self.moveOnNegZ(press)
                self.updateSnake()
            elif ((y == self.yc) and (z > -self.zb) and (z < self.zb) and
                 (x > -self.xb) and (x < self.xb)):
                self.moveOnPosY(press)
                self.updateSnake()
            elif ((y == -self.yc) and (z > -self.zb) and (z < self.zb) and
                  (x > -self.xb) and (x < self.xb)):
                self.moveOnNegY(press)
                self.updateSnake()
            elif ((x == self.xc) and (z > -self.zb) and (z < self.zb) and
                  (y > -self.yb) and (y < self.yb)):
                self.moveOnPosX(press)
                self.updateSnake()
            elif ((x == -self.xc) and (z > -self.zb) and (z < self.zb) and
                  (y > -self.yb) and (y < self.yb)):
                self.moveOnNegX(press)
                self.updateSnake()
        if (press == 'p'):
            if (self.isPaused == False):
                self.isPaused = True
            else:
                self.isPaused = False
            self.pause_unpause()
        if (press == 'r'): self.restart()
        self.head.velocity = vector(self.xVect,self.yVect,self.zVect)

    def restartMove(self, event):
        press = event.key
        if (press == 'r'):
            self.restart()
        
    
    def moveOnPosZ(self, press): # starting side
        if (press == 'w'):
            (self.xVect,self.yVect,self.zVect) = (0,+self.v,0)
        elif (press == 's'):
            (self.xVect,self.yVect,self.zVect) = (0,-self.v,0)
        elif (press == 'd'):
            (self.xVect,self.yVect,self.zVect) = (+self.v,0,0)
        elif (press == 'a'):
            (self.xVect,self.yVect,self.zVect) = (-self.v,0,0)
        self.head.velocity = vector(self.xVect,self.yVect,self.zVect)

    def moveOnNegZ(self, press):  # as if you go +z to +x to -z
        if (press == 'w'):
            (self.xVect,self.yVect,self.zVect) = (0,+self.v,0)
        elif (press == 's'):
            (self.xVect,self.yVect,self.zVect) = (0,-self.v,0)
        elif (press == 'd'):
            (self.xVect,self.yVect,self.zVect) = (+self.v,0,0)
        elif (press == 'a'):
            (self.xVect,self.yVect,self.zVect) = (-self.v,0,0)
        self.head.velocity = vector(self.xVect,self.yVect,self.zVect)

    def moveOnPosY(self, press): # as if you go +z to +y
        if (press == 'w'):
            (self.xVect,self.yVect,self.zVect) = (0,0,-self.v)
        elif (press == 's'):
            (self.xVect,self.yVect,self.zVect) = (0,0,+self.v)
        elif (press == 'd'):
            (self.xVect,self.yVect,self.zVect) = (+self.v,0,0)
        elif (press == 'a'):
            (self.xVect,self.yVect,self.zVect) = (-self.v,0,0)
        self.head.velocity = vector(self.xVect,self.yVect,self.zVect)

    def moveOnNegY(self, press): # as if you go +z to -y
        if (press == 'w'):
            (self.xVect,self.yVect,self.zVect) = (0,0,+self.v)
        elif (press == 's'):
            (self.xVect,self.yVect,self.zVect) = (0,0,-self.v)
        elif (press == 'd'):
            (self.xVect,self.yVect,self.zVect) = (+self.v,0,0)
        elif (press == 'a'):
            (self.xVect,self.yVect,self.zVect) = (-self.v,0,0)
        self.head.velocity = vector(self.xVect,self.yVect,self.zVect)

    def moveOnPosX(self, press): # as if you go +z to +x
        if (press == 'w'):
            (self.xVect,self.yVect,self.zVect) = (0,+self.v,0)
        elif (press == 's'):
            (self.xVect,self.yVect,self.zVect) = (0,-self.v,0)
        elif (press == 'd'):
            (self.xVect,self.yVect,self.zVect) = (0,0,-self.v)
        elif (press == 'a'):
            (self.xVect,self.yVect,self.zVect) = (0,0,+self.v)
        self.head.velocity = vector(self.xVect,self.yVect,self.zVect)

    def moveOnNegX(self, press): # as if you go +z to -x
        if (press == 'w'):
            (self.xVect,self.yVect,self.zVect) = (0,+self.v,0)
        elif (press == 's'):
            (self.xVect,self.yVect,self.zVect) = (0,-self.v,0)
        elif (press == 'd'):
            (self.xVect,self.yVect,self.zVect) = (0,0,+self.v)
        elif (press == 'a'):
            (self.xVect,self.yVect,self.zVect) = (0,0,-self.v)
        self.head.velocity = vector(self.xVect,self.yVect,self.zVect)
    
    

    """ END MOVE """
    

    def runIntoSelf(self):
        for i in xrange(2,len(self.snake)):
            if (self.head.pos == self.snake[i].pos):
                self.isGameOver = True

    def pause_unpause(self): # Why does it only pause on an even score?
        if (self.isPaused == True):
            self.pauseV = self.head.velocity
            self.head.velocity = vector(0,0,0)
            # updateSnake has a pause feature
        elif (self.isPaused == False):
            self.head.velocity = self.pauseV

    def restart(self):
        self.deleteAll()
        self.initALL()
        

    def deleteAll(self): 
        for obj in scene.objects:
            obj.visible = False
            del obj

    def run(self):
        def moveSnakeWrapper(event):
            self.moveSnake(event)
        scene.bind('keydown', moveSnakeWrapper)
        while True:
            rate(10)
            # Movement was glitching because r needs to be integer
            i = self.head
            if (self.isPaused == False):
                self.pause_unpause()
                if ((i.pos.z == self.zc) and (self.zVect == 0)): # on +z
                    if ((i.pos.x == -self.xc) or (i.pos.x == self.xc)):
                        (self.xVect,self.zVect) = (0,-self.v)
                        # If snake is on +z, when it reaches left/right edge,
                        # It will go toward -z along +-x
                    elif ((i.pos.y == self.yc) or (i.pos.y == -self.yc)):
                        (self.yVect,self.zVect) = (0,-self.v)
                        # If snake is on +z, when it reaches top/bottom edge,
                        # It will go toward -z along +-y
                elif ((i.pos.z == -self.zc) and (self.zVect == 0)): # on -z
                    if ((i.pos.x == self.xc) or (i.pos.x == -self.xc)):
                        (self.xVect,self.zVect) = (0,self.v)
                        # If snake is on -z, when it reaches left/right edge,
                        # It will go toward +z along +-x
                    elif ((i.pos.y == self.yc) or (i.pos.y == -self.yc)):
                        (self.yVect,self.zVect) = (0,self.v)
                        # If snake is on -z, when it reaches top/bottom edge,
                        # It will go toward +z along +-y

                elif ((i.pos.x == self.xc) and (self.xVect == 0)): # on +x
                    if ((i.pos.y == self.yc) or (i.pos.y == -self.yc)): # to +-y
                        (self.yVect,self.xVect) = (0,-self.v)
                    elif ((i.pos.z == self.zc) or (i.pos.z == -self.zc)): 
                        (self.zVect,self.xVect) = (0,-self.v) # to +-z
                elif ((i.pos.x == -self.xc) and (self.xVect == 0)): # on -x
                    if ((i.pos.y == self.yc) or (i.pos.y == -self.yc)): # to +-y
                        (self.yVect,self.xVect) = (0,self.v)
                    elif ((i.pos.z == self.zc) or (i.pos.z == -self.zc)): 
                        (self.zVect,self.xVect) = (0,self.v) # to +-z

                elif ((i.pos.y == self.yc) and (self.yVect == 0)): # on +y
                    if ((i.pos.x == self.xc) or (i.pos.x == -self.xc)): # to +-x
                        (self.xVect,self.yVect) = (0,-self.v)
                    elif ((i.pos.z == self.zc) or (i.pos.z == -self.zc)): 
                        (self.zVect,self.yVect) = (0,-self.v) # to +-z
                elif ((i.pos.y == -self.yc) and (self.yVect == 0)): # on -y
                    if ((i.pos.x == self.xc) or (i.pos.x == -self.xc)): # to +-x
                        (self.xVect,self.yVect) = (0,self.v)
                    elif ((i.pos.z == self.zc) or (i.pos.z == -self.zc)): 
                        (self.zVect,self.yVect) = (0,self.v) # to +-z
                
                i.velocity = vector(self.xVect,self.yVect,self.zVect) 
                i.pos += i.velocity
                self.pauseV = i.velocity
                self.updateSnake()
                self.runIntoSelf()
                # The while True didn't end on a False; break the loop.
                self.eatFood()
                #self.updateSnake()

                if (self.isGameOver == True):
                    self.scoreLabel.visible = False
                    scene.unbind('keydown', moveSnakeWrapper)
                    break
            else:
                pass
        self.gameOver()
        
    def gameOver(self):
        def restartWrapper(event):
            self.restartMove(event)
        scene.bind('keydown', restartWrapper)
        gameOverText = text(text='Game Over', font='times', depth=-1,
                            height=self.range/6, width=self.range/4,
                            color=color.magenta, pos=(0,0,self.range/2+self.r),
                            align='center')
        
        scoreText = text(text='Score:   %d' % self.score, font='times',
                         height=self.range/10, width=self.range/6,
                         color=color.magenta, pos=(0,-4,self.range/2+self.r),
                         align='center')

        #hs = self.highScoreList
        #self.cycleScores()
        # This is all commented out because although it works, VPython makes
        # text every time the highScoreList changes, which is when it goes
        # through the for loop, so multiple text objects get printed on one
        # another, making it really hard to read. This is the same for printing
        # out scores in the console.
        """
        highscoreText = text(text='Highscores:', font='times',
                             height=2.2, width=3,
                             color=color.yellow,
                             pos=(-20,20,self.range/2+self.r), align='center')
        first = text(text='1:     %d'%hs[0], font='times',height=2, width=2,
                   color=color.yellow, pos=(-22,16,self.range/2+self.r),
                   align='center')
        second = text(text='2:     %d'%hs[1], font='times',height=2, width=2,
                   color=color.yellow, pos=(-22,13,self.range/2+self.r),
                   align='center')
        third = text(text='3:     %d'%hs[2], font='times',height=2, width=2,
                   color=color.yellow, pos=(-22,10,self.range/2+self.r),
                   align='center')
        fourth = text(text='4:     %d'%hs[3], font='times',height=2, width=2,
                   color=color.yellow, pos=(-22,7,self.range/2+self.r),
                   align='center')
        fifth = text(text='5:     %d'%hs[4], font='times',height=2, width=2,
                   color=color.yellow, pos=(-22,4,self.range/2+self.r),
                   align='center')
        """
        """
        print 'High Scores:'
        print '1:   %d' % hs[0]
        print '2:   %d' % hs[1]
        print '3:   %d' % hs[2]
        print '4:   %d' % hs[3]
        print '5:   %d' % hs[4]
        #print hs
        """
    """
    def cycleScores(self):
        hs = self.highScoreList
        for i in xrange(len(hs)-1):
            if (self.score > hs[i]):
                self.highScoreList = hs[:i] + [self.score] + hs[i+1:]
                if (len(self.highScoreList) > 5):
                    self.highScoreList.pop()
                break
    """


PrismSnake()
