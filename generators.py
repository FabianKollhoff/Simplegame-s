# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 14:58:16 2018

@author: Fabian
"""
import random
import visuals

class Generator():
    
    def __init__(self, player, possibilityMovingblock = 6):
        
        #save properties of screen
        self.screenHeight = player.screenHeight
        self.screenWidth = player.screenWidth
    
class JumpGenerator(Generator):
    
    def __init__(self, player, possibilityMovingblock = 6):
        Generator.__init__(self, player, possibilityMovingblock)
        
        #save parameter for generation
        self.lastPositionX = player.x
        self.lastPositionY = 0
        
        #save calculate parameter for jump
        self.maximalJumpHeight = player.jump / player.gravity * player.jump / 2
        self.maximalJumpLengthD2 = player.jump / player.gravity * player.speed   
        self.maximalJumpLength = self.maximalJumpLengthD2 * 2
        
        self.maximalJumpHeight = int(self.maximalJumpHeight)
        self.maximalJumpLength = int(self.maximalJumpLength)
        self.maximalJumpLengthD2 = int(self.maximalJumpLengthD2)
        self.possibilityMovingblock = possibilityMovingblock
        
        self.stepSize = self.maximalJumpLengthD2
        
        #save parameter for restart
        self.startX = self.lastPositionX
        self.startY = 0
    
    
    #create Environment for a simple
    def createEnvironment(self):
        self.lastPositionX = self.startX
        self.lastPositionY = self.startY
        
        background = [visuals.Background(visuals.graphic.background_1, self.screenWidth, self.screenHeight, (0,self.screenHeight),0),visuals.Background(visuals.graphic.background_0, self.screenWidth, self.screenHeight, (0,self.screenHeight),0.2),visuals.Background(visuals.graphic.background_2, self.screenWidth, self.screenHeight, (0,self.screenHeight),0.5)]
        environment = []

        environment.append(visuals.Object(visuals.graphic.block_tom, self.screenWidth, self.screenHeight, (self.lastPositionX , self.screenHeight - self.lastPositionY)))
        
        return background, environment, []
    
    def genrateEnvironment(self, environment, positionOfViewX, bulletShooters):
        
        while self.lastPositionX - self.screenWidth < positionOfViewX:
            
            if random.randint(0,10) == False:
                bulletShooters.append(visuals.BulletShooter(visuals.graphic.canon, self.screenWidth, self.screenHeight, (self.lastPositionX-50+random.randint(0,100),50 + random.randint(0,300))))
            
            self.stepSize = random.randint(0 ,self.maximalJumpLength)
            
            if self.stepSize <= self.maximalJumpLengthD2:
                self.lastPositionY = random.randint(int(0+self.lastPositionY/4),self.lastPositionY + self.maximalJumpHeight)
            else:
                self.lastPositionY = random.randint(int(0+self.lastPositionY/2),int((self.maximalJumpHeight* ((self.maximalJumpLength - self.stepSize)/self.maximalJumpLengthD2) + self.lastPositionY) if int(self.stepSize) != self.maximalJumpLength else (self.lastPositionY)))
            
            self.lastPositionX += self.stepSize
            
            if random.randint(0,3) == False:
                environment.append(visuals.Coin(visuals.graphic.coin2, self.screenWidth, self.screenHeight, (self.lastPositionX + 7, self.screenHeight- self.lastPositionY - 50)))
                
            if random.randint(0,self.possibilityMovingblock) == False:         
                environment.append(visuals.MovingObject(visuals.graphic.block_tom, self.screenWidth, self.screenHeight, (self.lastPositionX , self.screenHeight- self.lastPositionY), self.lastPositionX + random.randint(40,200) ,random.randint(10,300)))
            else:
                environment.append(visuals.Object(visuals.graphic.block_tom, self.screenWidth, self.screenHeight, (self.lastPositionX , self.screenHeight- self.lastPositionY)))
            
            self.lastPositionX += environment[-1].obj_width
class SandboxGenerator():
    
    def __init__(self, player, possibilityMovingblock = 6):
        Generator.__init__(self, player, possibilityMovingblock)

    def createEnvironmentSandbox(self):  
        background = [visuals.Background(visuals.graphic.background0, self.screenWidth, self.screenHeight, (0,self.screenHeight),0),visuals.Background(visuals.graphic.background1, self.screenWidth, self.screenHeight, (0,self.screenHeight),0.2),visuals.Background(visuals.graphic.background2, self.screenWidth, self.screenHeight, (0,self.screenHeight),0.5)]
        environment = []
    
        for i_x in range(200):
            layer = []
            for i_y in range(20):
                layer.append(visuals.Object(visuals.graphic.block_black, self.screenWidth, self.screenHeight, (i_x*50 , self.screenHeight + i_y*50)))
            environment.append(layer)
    
        #reorganize environment
        return background,environment

class PvPGenerator():
    
    def __init__(self, player, possibilityMovingblock = 6):
        Generator.__init__(self, player, possibilityMovingblock)
    
    def createPvPEnvironment(self):
        background = [visuals.Background(visuals.graphic.background_1, self.screenWidth, self.screenHeight, (0,self.screenHeight),0),visuals.Background(visuals.graphic.background_0, self.screenWidth, self.screenHeight, (0,self.screenHeight),0.2),visuals.Background(visuals.graphic.background_2, self.screenWidth, self.screenHeight, (0,self.screenHeight),0.5)]
        environment = [visuals.Object(visuals.graphic.groundPvp, self.screenWidth, self.screenHeight, (0,self.screenHeight-100))]
        
        #reorganize environment
        return background,environment
    
class FlappyGenerator():
    
    def __init__(self, player, possibilityMovingblock = 6):
        Generator.__init__(self, player, possibilityMovingblock)
        self.lastPositionX = 0
    
    def createEnvironment(self):
        self.lastPositionX = 0
        background = [visuals.Background(visuals.graphic.background_1, self.screenWidth, self.screenHeight, (0,self.screenHeight),0),visuals.Background(visuals.graphic.background_0, self.screenWidth, self.screenHeight, (0,self.screenHeight),0.2),visuals.Background(visuals.graphic.background_2, self.screenWidth, self.screenHeight, (0,self.screenHeight),0.5)]
        environment = []
        
        #reorganize environment
        return background,environment
    
    def genrateEnvironment(self, environment, positionOfViewX):
        
        while self.lastPositionX - self.screenWidth < positionOfViewX:
            rand = int(random.randint(0,100)-100/2)
            
            rand1 = random.randint(0,self.screenHeight/2)
            
            #environment.append(visuals.FlappyObject(visuals.graphic.groundPvp, self.screenWidth, self.screenHeight, (0 + self.lastPositionX,self.screenHeight)))
            environment.append(visuals.FlappyObject(visuals.graphic.wall, self.screenWidth, self.screenHeight, (500 + self.lastPositionX, rand1 + rand)))
            environment.append(visuals.FlappyObject(visuals.graphic.wall, self.screenWidth, self.screenHeight, (500 + self.lastPositionX, self.screenHeight + rand1 - rand)))
            print("created: " + str(self.lastPositionX))
            self.lastPositionX += 600