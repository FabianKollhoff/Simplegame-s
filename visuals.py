# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 20:57:40 2018

@author: Fabian
"""

import pygame
import graphic

'''visual objects and inheritance classes'''
class Visual():
    
    def __init__(self, image, coordinates = (0,0), convertAble = False, ani_speed = 12):
        
        #coordinates
        self.x, self.y = coordinates
        self.image = image

        #time
        self.time = 0
        
        #displayed
        self.inScreen = True
        
        #animation
        self.ani_max = len(graphic.graphics[self.image])
        self.ani_pos = 0
        self.ani_speed = ani_speed
        
        #save size of object
        self.obj_width, self.obj_height = graphic.graphics[self.image][0].get_rect().size
            
        #apply change
        self.y -= self.obj_height
        
    def update(self, deltaTime, game_speed = 100):
        #update image
        self.time += deltaTime
        self.ani_pos = round(self.time*self.ani_speed*game_speed/100 % self.ani_max) - 1
        
    def draw(self, screen, positionOfScreenX = 0, positionOfScreenY = 0):
        #draw graphic at position
        if self.inScreen:
            obj = graphic.graphics[self.image][self.ani_pos]
            screen.blit(obj, (round(self.x - positionOfScreenX), round(self.y - positionOfScreenY)))
        
class Player(Visual):

    def __init__(self, objectType, game_speed, keyLeft, keyRight, keyUp, ground, screenHeight, screenWidth, border = 0, coordinates = (0,0), pvpMode = False):
                
        Visual.__init__(self, objectType, coordinates, False, 24)
        
        self.standing = Visual(graphic.hand_of_blood, coordinates, False, 24)
        
        self.x, self.y = coordinates
        
        #set keys to move
        self.keyLeft = keyLeft
        self.keyRight = keyRight
        self.keyUp = keyUp
        
        #spawn
        self.spawn = coordinates
        self.spawn_border = border
        
        #set running direction
        self.backward = False
        
        #counter coins
        self.counterCoins = 0
        
        #able to jump
        self.ableToJump = True
        
        #pyhsics
        self.force_up = 0
        self.gravity = 0.15
        self.speed = 4
        self.ground = ground
        self.lowestlayer = ground
        self.border = border
        self.jump = 5
        
        #save gamespeed
        self.game_speed = game_speed
        
        #screensize
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        
        self.mask = pygame.mask.from_surface(graphic.graphics[objectType][0])
        
        #for ai
        self.keyUp_pressed = 0
        self.fitness = 0
        
        self.timeBullet = 0
        self.shootingSpeed = 1
        self.pvpMode = pvpMode
    
    def update(self, deltaTime, game_speed, key, environment , bullets = [], overrideRight = 0, overrideUp = 0):
        
        Visual.update(self, deltaTime, game_speed)
        #update image
        self.standing.update(deltaTime, game_speed)
        
        #save last coordinates
        last_x = self.x
        last_y = self.y
        
        #update x
        self.movement = (-1 if key[self.keyLeft] else 1 if key[self.keyRight] or overrideRight else 0) * deltaTime * self.game_speed * self.speed
        
        #for ai to save player action
        '''
        if movement == 0:
            self.keyRight_pressed = 0
            self.keyLeft_pressed = 0
        elif movement == -1:
            self.keyRight_pressed = 0
            self.keyLeft_pressed = 1
        else:
            self.keyRight_pressed = 1
            self.keyLeft_pressed = 0
        '''
        
        #apply movement
        self.x += self.movement
        
        #update direction player is walking
        if self.movement > 0:
            self.backward = False
        elif self.movement < 0:
            self.backward = True
        
        #update border
        #if self.x <= self.border:
        #    self.x = self.border
        
        #update y
        #jump
        if (key[self.keyUp] or overrideUp) and self.ableToJump:
            self.force_up = self.jump
            self.ableToJump -= 1 
            
            #for ai
            self.keyUp_pressed = 1
        
        #apply force
        self.y -= self.force_up * deltaTime * self.game_speed
        
        #set ground to respawn point
        self.ground = self.lowestlayer
        
        #Correctioncounters
        correctioncounter = 0
        
        #collision
        for i in range(len(environment)):
            #check for collision
            i -= correctioncounter
            if environment[i].model == 0:
                continue
            if environment[i].model == 1:
                if environment[i].moveAble:
                    if environment[i].standingOn:
                        self.x -= (environment[i].last_x - environment[i].x)
                        print(environment[i].x - environment[i].last_x)
                        environment[i].standingOn = False

            #test for collision with player and environment
            if environment[i].x < self.x + self.obj_width and environment[i].x + environment[i].obj_width > self.x and environment[i].y - self.obj_height < self.y and environment[i].y > self.y - environment[i].obj_height:
                
                if self.pvpMode:
                    self.ground = environment[i].y - 0.0001
                    self.force_up = 0
                    continue
                
                if environment[i].model == 1:
                    #test for last position and correct position
                    
                    #check if object is able to move
                    if environment[i].moveAble:
                        
                        #use last positions to calculate position of player
                        if environment[i].last_y > last_y + self.obj_height:
                            self.ground = environment[i].y - 0.0001
                            self.force_up = 0
    
                        elif environment[i].last_y < last_y - environment[i].obj_height:
                            self.y = environment[i].y + environment[i].obj_height + 0.0001
                            
                        elif environment[i].last_x > last_x:
                            self.x = environment[i].x - self.obj_width - 0.0001
                            
                        elif environment[i].last_x + environment[i].obj_width < last_x:
                            self.x = environment[i].x + environment[i].obj_width + 0.0001
                            
                    else:
                        
                        #use last position of player and actuall position of the object to calculate position of player
                        if environment[i].y > last_y + self.obj_height:
                            self.ground = environment[i].y - 0.0001
                            self.force_up = 0
    
                        elif environment[i].y < last_y - environment[i].obj_height:
                            self.y = environment[i].y + environment[i].obj_height + 0.0001
                            self.force_up = 0
                            
                        elif environment[i].x > last_x:
                            self.x = environment[i].x - self.obj_width - 0.0001
                            
                        elif environment[i].x + environment[i].obj_width < last_x:
                            self.x = environment[i].x + environment[i].obj_width + 0.0001
                
                #check wether object is collect able
                if environment[i].model == 2:
                    #increase the correctioncounter to prevent the index from getting out of range
                    correctioncounter += 1
                    
                    #increase the counter of collected coins
                    self.counterCoins += 1
                    
                    #play sound
                    environment[i].playSound()
                    #remove obejct
                    environment.pop(i)
        
        #renew correctionCounter
        correctioncounter = 0
        
        #update bullets
        for i in range(len(bullets)):
            #apply correction counter to index
            i -= correctioncounter
            
            #check for bitmap collison with bullet
            if self.mask.overlap(bullets[i].mask, (round(bullets[i].x - self.x), round(bullets[i].y - self.y))):
                return True
            
            #remove bullet when it is out of screen or range
            if bullets[i].outOfRange:
                bullets.pop(i)
                correctioncounter += 1
            
        #add obj size
        self.ground -= self.obj_height
        
        #ground
        if self.y < self.ground:
            #apply gravity on force
            self.ableToJump = False
            self.force_up -= self.gravity * deltaTime * self.game_speed
        #reset ground
        elif self.y > self.ground:
            self.ableToJump = True
            self.force_up = 0
            self.y = self.ground - 0.0001
            
        #test if in the game
        if self.y > self.screenHeight:
            return True
        
        #store fitness
        self.fitness = self.x

        return False
            
    def draw(self, screen, positionOfScreenX, positionOfScreenY = 0):
        if self.movement != 0:
            obj = pygame.transform.flip(graphic.graphics[self.image][self.ani_pos], self.backward, False)
        else:
            obj = pygame.transform.flip(graphic.graphics[self.standing.image][self.ani_pos], self.backward, False)

        screen.blit(obj, (round(self.x - positionOfScreenX), round(self.y - positionOfScreenY)))
        
    def respawn(self):
        self.counterCoins = 0
        self.x, self.y = self.spawn
        self.border = self.spawn_border
        
    def shootBullet(self, bullets):
        print(self.time-self.timeBullet)
        if self.time-self.timeBullet >= self.shootingSpeed*100/self.game_speed:        
            self.timeBullet = self.time
            bullets.append(Bullet(graphic.bullet, (-30 if self.backward else 30,0), (self.x + self.obj_width,self.y + self.obj_height/2)))

class SandboxPlayer(Player):
    
    def __init__(self, objectType, screenHeight, screenWidth, game_speed, keyLeft, keyRight, keyUp, ground, border = 0, coordinates = (0,0)):
        #for hand
        self.hand = pygame.image.load("graphics/Player/0.png")
        self.backward = False
        
        #game properties
        self.buildRange = 1*50
        self.blocksInInventory = 0
        self.chosenBlock = 0
        
        Player.__init__(self, objectType, screenHeight, screenWidth, game_speed, keyLeft, keyRight, keyUp, ground, border, coordinates)
    
    def update(self, deltaTime, game_speed, key, environment, positionOfScreenX, positionOfScreenY, overrideSideways = 0, overrideUp = 0, mouse = None, mouse_pressed_left = 0, mouse_pressed_right = 0):
        self.rotation = 0 
        if mouse == None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if pygame.mouse.get_pressed()[0]:
                self.removeBlock(environment, positionOfScreenX, positionOfScreenY)
        
            if pygame.mouse.get_pressed()[2]:
                self.setBlock(environment, positionOfScreenX, positionOfScreenY)
        else:
            mouse_x, mouse_y = mouse
            
            print(mouse_pressed_left)
            
            if mouse_pressed_left:
                self.removeBlock(environment, positionOfScreenX, positionOfScreenY)
        
            if mouse_pressed_right:
                self.setBlock(environment, positionOfScreenX, positionOfScreenY)
        
        #update image        
        Visual.update(self, deltaTime, game_speed)
        
        #save last coordinates
        last_x = self.x
        last_y = self.y
        
        #update x
        self.movement = (-1 if (key[self.keyLeft] or overrideSideways == -1) else 1 if (key[self.keyRight] or overrideSideways == 1) else 0) * deltaTime * self.game_speed * self.speed
        self.x += self.movement
        if self.movement > 0:
            self.backward = False
        elif self.movement < 0:
            self.backward = True
        
        if self.x <= self.border:
            self.x = self.border
        
        #update y
        #jump
        if (key[self.keyUp] or overrideUp)and self.ableToJump:
            self.force_up = self.jump
            self.ableToJump -= 1            
        
        #apply force
        self.y -= self.force_up * deltaTime * self.game_speed

        self.ground = self.lowestlayer
        
        #Correctioncounters
        correctioncounter = 0
        
        #collision
        for i in range(round(self.x/50) -2, (round(self.x/50) + 2) if round(self.x/50) + 2 <= len(environment) else len(environment)):
            for i_y in range(len(environment[i])):
                #check for collision
                i_y -= correctioncounter
                if environment[i][i_y].model == 0:
                    continue
    
                #test for collision
                if environment[i][i_y].x < self.x + self.obj_width and environment[i][i_y].x + environment[i][i_y].obj_width > self.x and environment[i][i_y].y - self.obj_height < self.y and environment[i][i_y].y > self.y - environment[i][i_y].obj_height + 0.0001:
                    
                    if environment[i][i_y].model == 1:
                        #test for last position and correct position
                        if environment[i][i_y].y > last_y + self.obj_height:
                            self.ground = environment[i][i_y].y
                            self.force_up = 0
                            #print("Up")
    
                        elif environment[i][i_y].y <= last_y - environment[i][i_y].obj_height + 0.0001:
                            self.y = environment[i][i_y].y + environment[i][i_y].obj_height - 0.0001
                            self.force_up = 0
                            #print("Down")
                            
                        elif environment[i][i_y].x > last_x:
                            self.x = environment[i][i_y].x - self.obj_width
                            #print("Left")
                            
                        else: #environment[i][i_y].x + environment[i][i_y].obj_width > last_x:
                            self.x = environment[i][i_y].x + environment[i][i_y].obj_width
                            #print("Right")    
                            
                    if environment[i][i_y].model == 2:
                        correctioncounter += 1
                        #self.jump += 1 / self.jump
                        environment[i][i_y].playSound()
                        environment[i].pop(i_y)

        #add obj size
        self.ground -= self.obj_height
        
        #ground
        if self.y < self.ground:
            #apply gravity on force
            self.ableToJump = False
            self.force_up -= self.gravity * deltaTime * self.game_speed
        #reset ground
        elif self.y > self.ground:
            self.ableToJump = True
            self.force_up = 0
            self.y = self.ground - 0.0001
        
    def removeBlock(self, environment, positionOfScreenX, positionOfScreenY):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x = positionOfScreenX + mouse_x
        y = positionOfScreenY + mouse_y
        if int(x/50) >= len(environment):
            return
        i_x = int(x/50)
        i_y = int(y/50)
        correctioncounter = 0
        #check for collision
        for i_y in range(len(environment[i_x])):
            i_y -= correctioncounter            
            if environment[i_x][i_y].model == 0:
                continue
            
            if environment[i_x][i_y].x <= i_x*50 and environment[i_x][i_y].x + environment[i_x][i_y].obj_width >= i_x*50 and environment[i_x][i_y].y <= y and environment[i_x][i_y].y >= y - environment[i_x][i_y].obj_height:
                distanceToPlayerX = self.x - x
                distanceToPlayerY = self.y - y
                if distanceToPlayerX < -self.buildRange - self.obj_width or distanceToPlayerX > self.buildRange or distanceToPlayerY < -self.buildRange - self.obj_height or distanceToPlayerY > self.buildRange:
                    return
                environment[i_x].pop(i_y)
                correctioncounter += 1
                self.blocksInInventory += 1
    
    def setBlock(self, environment, positionOfScreenX, positionOfScreenY):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x = positionOfScreenX + mouse_x
        y = positionOfScreenY + mouse_y
        if int(x/50) >= len(environment) or self.blocksInInventory <= 0:
            return
        i_x = int(x/50) 
        correctioncounter = 0
        #check for collision
        for i_y in range(len(environment[i_x])):
            i_y -= correctioncounter            
            if environment[i_x][i_y].model == 0:
                continue
            
            #check if in range
            if environment[i_x][i_y].x < x and environment[i_x][i_y].x + environment[i_x][i_y].obj_width > x and environment[i_x][i_y].y < y and environment[i_x][i_y].y > y - environment[i_x][i_y].obj_height:
                return
        i_y = int(y/50) + 1
        environment[i_x].append(Object(graphic.block_black, self.screenWidth, self.screenHeight, (i_x*50 , i_y*50)))
        self.blocksInInventory -= 1

    def draw(self, screen, positionOfScreenX, positionOfScreenY = 0):
        #draw graphic at position
        if self.inScreen:
            Player.draw(self, screen, positionOfScreenX, positionOfScreenY)
            
class Bird(Visual):
    
    def __init__(self, objectType, game_speed, keyUp, screenHeight, screenWidth, coordinates = (0,0)):
        Visual.__init__(self, objectType, coordinates)
        
        #save key
        self.keyUp = keyUp
        
        #save gamespeed
        self.game_speed = game_speed
        
        #screensize
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        
        self.mask = pygame.mask.from_surface(graphic.graphics[self.image][0])

        self.keyUpPressed = False
        self.forceUp = 0
        
        self.strength = 7
        self.gravity = 0.15
        
    def update(self, deltaTime, key, environment):
        #update image        
        Visual.update(self, deltaTime, self.game_speed)  
        
        if key[self.keyUp]:
            if self.keyUpPressed == False:
                self.keyUpPressed = True
                self.forceUp += self.strength
        else:      
            self.keyUpPressed = False
            
        self.y -= self.forceUp * deltaTime* self.game_speed
        self.forceUp -= self.gravity * deltaTime* self.game_speed
        
        self.x += 3 * deltaTime* self.game_speed
        
        if self.y >= self.screenHeight or self.y <= 0:
           return True
            
        correctionCounter = 0    
        
        for i in range(len(environment)):
            
            i -= correctionCounter
            
            if self.mask.overlap(environment[i].mask, (round(environment[i].x - self.x), round(environment[i].y - self.y))):
                return True
            
            if environment[i].x + environment[i].obj_width <= self.x-200:  #bad code
                environment.pop(i)
                correctionCounter += 1
                

    def draw(self, screen, positionOfScreenX, positionOfScreenY = 0):
        #obj = pygame.transform.flip(graphic.graphics[self.image][self.ani_pos], self.backward, False)
        screen.blit(graphic.graphics[self.image][self.ani_pos], (round(self.x - positionOfScreenX), round(self.y - positionOfScreenY)))    
        
    def respawn(self):
        self.x = 0
        self.y = self.screenHeight/2
            
class Environment(Visual):
    
    def __init__(self, image, screenWidth, screenHeight, coordinates, convertAble = True, model = 1, channel = 0, moveAble = False, ani_speed = 10):
        Visual.__init__(self, image, coordinates, convertAble, ani_speed)
        
        #save data to display
        self.moveAble = moveAble
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.model = model
        self.channel = channel
    
    def update(self, deltaTime, game_speed, positionOfScreenX, positionOfScreenY = 0):
        #update image
        Visual.update(self, deltaTime, game_speed)
        
        #check wether object is in view
        x_view = self.x - positionOfScreenX
        y_view = self.y - positionOfScreenY
        
        if x_view < -self.obj_width or x_view > self.screenWidth:
            self.inScreen = False
        else:
            if y_view < -self.obj_height - 1 or y_view > self.screenHeight- 1:
                self.inScreen = False
            else:
                self.inScreen = True
        
class Background(Environment):
    
    def __init__(self, image, screenWidth, screenHeight, coordinates, distance):
        self.distance = distance
        self.correction = 0
        Environment.__init__(self, image, screenWidth, screenHeight, coordinates,True, 0, distance)
    
    def update(self, deltaTime, game_speed, positionOfScreenX, positionOfScreenY = 0):
        Environment.update(self, deltaTime, game_speed, 0)
        
    def draw(self, screen, positionOfScreenX, positionOfScreenY = 0):
        if self.distance != 0:
            if positionOfScreenX*self.distance + self.correction >= self.obj_width:
                self.correction -= self.obj_width
            elif positionOfScreenX*self.distance + self.correction <= 0:
                self.correction += self.obj_width
            Environment.draw(self, screen, (positionOfScreenX*self.distance) + self.correction - self.obj_width, positionOfScreenY)            
        Environment.draw(self, screen, (positionOfScreenX*self.distance) + self.correction, positionOfScreenY)
        
class Object(Environment):
    
    def __init__(self, image, screenWidth, screenHeight, coordinates, model = 1):
        Environment.__init__(self, image, screenWidth, screenHeight,  coordinates, False, model, 1)
        
class MovingObject(Environment):
    
    def __init__(self, image, screenWidth, screenHeight, coordinates, end_x, speed, model = 1): 
        Environment.__init__(self, image, screenWidth, screenHeight,  coordinates, False, model, 1, True)
       
        self.standingOn = False
        self.start_x = self.x
        self.end_x = end_x
        self.speed = speed
        self.distance = self.end_x - self.start_x
        self.last_x = self.x
        self.last_y = self.y
        
    def update(self, deltaTime, game_speed, positionOfScreenX, positionOfScreenY = 0):
        #save last position
        self.last_x = self.x
        self.last_y = self.y
        
        try:
            movement = (self.time*self.speed*100/game_speed) % (self.distance*2)
        except ZeroDivisionError:
            movement = 0
        
        self.x = (movement if movement <= self.distance else -movement + self.distance*2) + self.start_x
        
        Environment.update(self, deltaTime, game_speed, positionOfScreenX, positionOfScreenY)
        
class Coin(Object):
    
    def __init__(self, image, screenWidth, screenHeight, coordinates):
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        self.sound = pygame.mixer.Sound("sounds/coin.wav")
        Environment.__init__(self, image, screenWidth, screenHeight, coordinates, False, 2, 2, 50)
        #re coin
        self.y += self.obj_height
        
        for i in range(len(graphic.graphics[self.image])):
            graphic.graphics[self.image][i] = pygame.transform.scale(graphic.graphics[self.image][i], (50,50))
        self.obj_height = 50
        self.y -= self.obj_height
        self.obj_width = 50
                    
    def playSound(self):
        pygame.mixer.Sound.play(self.sound)
        
class Bullet(Visual):
    
    def __init__(self, image, force = (100,0), coordinates = (0,0)):
        Visual.__init__(self, image, coordinates, True)
        
        #force
        self.force_x, self.force_y = force
        
        #for mask collision
        self.mask = pygame.mask.from_surface(graphic.graphics[self.image][0])
        self.outOfRange = False
        
    def update(self, deltaTime, player):
        self.x += self.force_x*deltaTime*player.game_speed
        
        self.force_y += player.gravity*deltaTime*player.game_speed
        self.y += self.force_y*deltaTime*player.game_speed
        Visual.update(self, player.game_speed, deltaTime)
        
    def draw(self, screen, positionOfScreenX = 0, positionOfScreenY = 0):
        Visual.draw(self, screen, positionOfScreenX, positionOfScreenY)
        if self.y <= 0 or self.y >= 900:
            self.outOfRange = True
            print("destroyed")
        
class BulletShooter(Object):
    
    def __init__(self, image, screenWidth, screenHeight, coordinates):
        self.maxBullets = 10
        self.bullets = 0
        self.shootingSpeed = 2
        self.time = 0
        
        Object.__init__(self, image, screenWidth, screenHeight, coordinates)
    
    def update(self, deltaTime, game_speed, bullets, positionOfScreenX, player):
        Object.update(self, deltaTime, game_speed, positionOfScreenX)

        if self.inScreen:        
            self.time += deltaTime
            self.time_last = self.time
            self.time %= self.shootingSpeed*100/ player.game_speed
            if self.time != self.time_last:
                bullets.append(Bullet(graphic.bullet,(-3,((player.y)-self.y)/(((player.x)-self.x))*-3) if player.x-self.x <= 0 else (3,((player.y)-self.y)/(((player.x)-self.x))*3),(self.x+self.obj_width/2,self.y+self.obj_height/2)))
                self.bullets += 1
            if self.bullets == self.maxBullets:
                self.time = 0
                self.bullets = 0
                
class FlappyObject(Environment):
    
    def __init__(self, image, screenWidth, screenHeight, coordinates = (0,0)):
        Environment.__init__(self, image, screenWidth, screenHeight, coordinates) 
        self.mask = pygame.mask.from_surface(graphic.graphics[self.image][0])
        
''' Menue '''
class MenueElement():
    
    def __init__(self, name, coordinates = (0,0)):

        self.name = name
        self.onItem = 0
        self.makesSound = False
        self.pressed = False
        
        self.width , self.height = graphic.graphics[name][0].get_rect().size
        
        #adjust coordinates
        coordinates = list(coordinates)
        coordinates[0]-= self.width/2
        coordinates = tuple(coordinates)
        
        self.coordinates = coordinates
                
    def loadSound(self, sound):
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        self.makesSound = True
        self.sound = pygame.mixer.Sound("sounds/" + sound + ".wav")
        return self

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.coordinates[0] < mouse_x and self.coordinates[0] + self.width > mouse_x and self.coordinates[1] < mouse_y and self.coordinates[1] > mouse_y - self.height:
            if self.makesSound and pygame.mixer.get_busy() == False and self.onItem == 0:
                pygame.mixer.Sound.play(self.sound)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    self.pressed = False
                    return True
                self.onItem = 1
        else:
            if self.makesSound and pygame.mixer.get_busy():
                pygame.mixer.Sound.stop(self.sound)
            self.onItem = 0
            self.pressed = False
        return False

    def draw(self, screen):
        obj = graphic.graphics[self.name][self.onItem]
        screen.blit(obj, self.coordinates)
        
class MenueBar():
    
    def __init__(self, speed, height, minWidth, maxWidth, coordinates = (0,0)):
        self.time = 0
        self.speed = speed
        self.coordinates = coordinates
        self.minWidth = minWidth
        self.maxWidth = maxWidth
        self.width = self.minWidth
        self.height = height
        self.pressed = False
    
    def update(self, deltaTime):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.coordinates[0] < mouse_x and self.coordinates[0] + self.width > mouse_x and self.coordinates[1] < mouse_y and self.coordinates[1] > mouse_y - self.height:
            if self.width < self.maxWidth:
                self.width += deltaTime * self.speed
                if self.width > self.maxWidth:
                    self.width = self.maxWidth
            else:
                return True
        else:               
            if self.width > self.minWidth:
                self.width -= deltaTime * self.speed
                if self.width < self.minWidth:
                    self.width = self.minWidth
        return False
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), (0,0,round(self.width),900), 0)
        
''' display text on screen '''
		
def displayText(screen, font, text, x = 0, y = 0, color = (255,255,255)):
    screen.blit(font.render(text, True, color),(x,y))   
    
class blinkingText():
    
    def __init__(self, font, text, x = 0, y = 0, speed = 20, color = (255,255,255)):
        self.font = font
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        
        #time
        self.time = 0
        
    def update(self, deltaTime):
        #update image
        self.time += deltaTime
        self.on = round(self.time*self.speed % 2) - 1

    def draw(self, screen):
        if self.on:
            screen.blit(self.font.render(self.text, True, self.color),(self.x,self.y))