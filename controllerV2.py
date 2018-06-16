# -*- coding: utf-8 -*-
"""
Created on Fri May 11 10:44:25 2018

@author: Fabian
"""

import pygame
import os
import time

#import own modules
import client
import visuals
import generators

def leaveSystem():
    os._exit(0) 

if __name__ == '__main__':
    #define size of window
    width = 1800
    height = 900
    
    #set window position
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
    #center window on screen
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    #create screen
    
    pygame.init()
    
    screen = pygame.display.set_mode((width,height))
    
    socket = client.SimpleTcpClient()
    socket.startListenerForServer()
    
    running = True
    lastFrameTime = 0

    players = [visuals.SandboxPlayer("hand_of_blood", 100, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, height * 3, height, width, 0,(200, height-300))]
    
    #create player
    player = visuals.SandboxPlayer("hand_of_blood", 100, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, height * 3, height, width, 0,(200, height-300))
    generator = generators.Generator(player)
    
    #position of background
    positionOfViewX = player.x - width/2
    positionOfViewY = player.y - height/2
    
    #create sandbox environment
    background,environment = generator.createEnvironmentSandbox()
    
    #update time
    deltaTime = (time.clock() - lastFrameTime)
    lastFrameTime = time.clock()
    
    #subsystem running loop
    while running:
        #wait for exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                socket.close()
                leaveSystem()
        
        key = pygame.key.get_pressed()
        
        msg = "0 0"
        
        if key[pygame.K_d]:
            msg = "1 "
        elif key[pygame.K_a]:
            msg = "-1 "
        else:
            msg = "0 "
        
        if key[pygame.K_w]:
            msg = msg + "1 "
        else:
            msg = msg + "0 "

        x, y = pygame.mouse.get_pos()
        
        msg = msg + str(x) + " " + str(y) + " "
        
        if pygame.mouse.get_pressed()[0]:
            msg = msg + "1 "
        else:
            msg = msg + "0 "
            
        if pygame.mouse.get_pressed()[2]:
            msg = msg + "1 "
        else:
            msg = msg + "0 "
        
        socket.send(msg)

        d = client.data.split(" ")
        
        try:
            print("test")
            if client.data != "":
                print("test")
                numberPlayers = int(d[0])
                
                positionOfViewX = float(d[1])
                positionOfViewY = float(d[2])
                print("test")
                player.x = float(d[3])
                player.y = float(d[4])
                print("test")
                
                while numberPlayers > len(players):
                    players.append(visuals.SandboxPlayer("hand_of_blood", 100, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, height * 3, height, width, 0,(200, height-300)))
                
                print("test4")
                
                for index in range(len(players)):
                    print(str(index))

                    players[index].x = float(d[4+2*(index+1)-1])
                    players[index].y = float(d[4+2*(index+1)])
        except:
            print("error")
        
        print("test")
        
        #fill background
        screen.fill((0,0,0))
        
        #update time
        deltaTime = (time.clock() - lastFrameTime)
        lastFrameTime = time.clock()

        #update backgound
        for obj in background:
            obj.update(deltaTime, positionOfViewX, positionOfViewY)
            obj.draw(screen, positionOfViewX, positionOfViewY)
        
        print("test1")
        
        #update and draw objects in range of player
        for i in range(round(positionOfViewX/50) - 1, round(positionOfViewX/50) + 37 if round(positionOfViewX/50) + 37 <= len(environment) else len(environment)):
            if i < 0:
                continue
            for i_y in range(len(environment[i])):
                #draw environment
                environment[i][i_y].update(deltaTime, positionOfViewX, positionOfViewY)
                environment[i][i_y].draw(screen, positionOfViewX, positionOfViewY)
        
        #draw player
        for p in players:
            p.draw(screen ,positionOfViewX, positionOfViewY)

        player.draw(screen, positionOfViewX, positionOfViewY)

        #display FPS
        '''
        if key[pygame.K_F3]:
            visuals.displayText(screen, font, ("0" if deltaTime == 0 else str(int(1/deltaTime))) + " FPS")
            visuals.displayText(screen, font, str(positionOfViewX/50), 100)
            visuals.displayText(screen, font, str(round(player.x)), 400)
        '''
    
        pygame.display.flip()
        pygame.display.update()