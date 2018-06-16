# -*- coding: utf-8 -*-
"""
Created on Fri May 11 10:44:25 2018

@author: Fabian
"""

import pygame
import os
import client

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
    
    while True:
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
        
        screen.fill((255,255,255))
        
        pygame.display.flip()
        pygame.display.update()

        