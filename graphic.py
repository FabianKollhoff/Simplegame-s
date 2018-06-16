# -*- coding: utf-8 -*-
"""
Created on Sun May 27 16:32:22 2018

@author: Fabian
"""

import pygame
import glob
import _thread

#load img
def loadImg(image):

    ani_path = sorted(glob.glob("graphics/" + image + "/*.png"))
    ani_max = len(ani_path)
    ani = []
    
    #convert or don't
    for i in range(0,ani_max):
        if True:
            ani.append(pygame.image.load("graphics/" + image + "/"+str(i)+".png").convert_alpha())
        else:
            ani.append(pygame.image.load(ani_path[i]).convert())
            
    return ani

#define name with corrensponding index
block_tom = 0
start = 1
sandbox = 2
AILife = 3
resume = 4
quit = 5
options = 6
background_game_menue = 7
background_menue = 8
hand_of_blood_running = 9
block_black = 10
Options = 11
Music = 12
Volume = 13
hand_of_blood = 14
background_1 = 15
background_0 = 16
background_2 = 17
coin2 = 18
background0 = 19
background1 = 20
background2 = 21
bullet = 22
newBlock = 23
groundPvp = 24
wall = 25
hanno = 26
flappy = 27
canon = 28
hand_of_blood_walking = 29
vs1 = 30
border = 31

def loadBackgroundMenue():
    global grahics
    try:
        graphics[background_menue] = loadImg("background_menue")
        
    except:
        print("error")

graphics = [loadImg("block_tom"),loadImg("start"),loadImg("sandbox"),loadImg("AILife"),loadImg("resume"),loadImg("quit"),loadImg("options"),loadImg("background_game_menue"),loadImg("background_menue_test"),loadImg("hand_of_blood_running"),loadImg("block_black"),loadImg("Options"),loadImg("Music"),loadImg("Volume"),loadImg("hand_of_blood"),loadImg("background_1"),loadImg("background_0"),loadImg("background_2"),loadImg("coin2"),loadImg("background0"),loadImg("background1"),loadImg("background2"),loadImg("bullet"),loadImg("lastBlock"),loadImg("groundPvP"),loadImg("wall"),loadImg("hanno3"),loadImg("flappy"),loadImg("canon"),loadImg("hand_of_blood_walking"),loadImg("1vs1"),loadImg("border")]