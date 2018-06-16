# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 20:51:21 2018

@author: Fabian
"""

#import python libaries
import pygame
import time
import os

def leaveSystem():
    os._exit(0)

#create option window
def optionWindow(screen):
    
    #main loop
    while True:
        key = pygame.key.get_pressed()
        
        pygame.draw.rect(screen, (59, 60, 61), (50 ,50 ,width-100 ,height-100))
        pygame.draw.rect(screen, (10, 10, 10), (50 ,50 ,width-100 , 70))
        
        visuals.displayText(screen,fontOptionMenue50, "Options", 100, 70)
        visuals.displayText(screen,fontOptionMenue40, "Music", 200, 170)
        visuals.displayText(screen,fontOptionMenue40, "Volume", 200, 270)
        
        #check for quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                leaveSystem()
                
        if key[pygame.K_ESCAPE]:
            break;
        
        #update display
        pygame.display.flip()
        pygame.display.update()

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
    
    # init font
    pygame.font.init()
    
    #create screen
    screen = pygame.display.set_mode((width,height))
    
    #import own module
    import visuals
    import generators

    #load music
    pygame.mixer.music.load("music/music.wav")
    
    #setup menue elments
    startButton = visuals.MenueElement(visuals.graphic.start,(350,70)).loadSound("click")
    sandboxButton = visuals.MenueElement(visuals.graphic.sandbox,(350,220)).loadSound("click")
    aiLifeButton = visuals.MenueElement(visuals.graphic.AILife,(350,370)).loadSound("click")
    flappyButton = visuals.MenueElement(visuals.graphic.flappy,(350,530)).loadSound("click")
    vs1Button = visuals.MenueElement(visuals.graphic.vs1,(350,680)).loadSound("click")
    
    resumeButton = visuals.MenueElement(visuals.graphic.resume,(width/2,300)).loadSound("resume")
    quitButton = visuals.MenueElement(visuals.graphic.quit,(width/2,400)).loadSound("quit")
    optionButton = visuals.MenueElement(visuals.graphic.options,(width/2,500)).loadSound("click")
    
    background_game_menue = visuals.Visual(visuals.graphic.background_game_menue, (width/2-125,650), True,1)
    background_menue = visuals.Visual(visuals.graphic.background_menue ,(0,height),True,100)
        
    bar = visuals.MenueBar(3000,height,100,1000)
    
    #setup game elements
    environment = []
    
    #init mixer
    mixer = pygame.mixer.init()
    
    #load font
    font = pygame.font.SysFont('Papyrus', 20)
    font3 = pygame.font.SysFont('Papyrus', 30)
    font5 = pygame.font.SysFont('Papyrus', 50)
    
    fontOptionMenue50 = pygame.font.SysFont('Original Surfer', 50)
    fontOptionMenue40 = pygame.font.SysFont('Original Surfer', 40)
    
    #set window properties
    pygame.display.set_caption('Spandauer Handwerk: Ahu Edition')
    pygame.display.set_icon(pygame.image.load("graphics/hand_of_blood/0.png"))
    
    #set last frame time
    lastFrameTime = time.clock()
    deltaTime = 0
    
    #set ground
    ground = height
    
    #set system_running variable
    system_running = True
    
    pygame.mixer.music.play(-1)
            
    pygame.mixer.music.set_volume(0.05)
    
    #start system loop
    while system_running:
        #vreate subsystem loop variable
        running = True  
        
        #save selected item
        selectedItem = -1
        
        #run start menue loop
        while True:
            #get key
            key = pygame.key.get_pressed()
            
            #update deltaTime
            deltaTime = (time.clock() - lastFrameTime)
            lastFrameTime = time.clock()

            #update menue bar
            menueOpen = bar.update(deltaTime)
            
            #check if menue is opend
            if menueOpen:
                
                #check if item is selected and set selectedItem to selected item
                if startButton.update():
                    selectedItem = 0
                    break
                
                if sandboxButton.update():
                    selectedItem = 1
                    break
                
                if aiLifeButton.update():
                    selectedItem = 2
                    break
                
                if flappyButton.update():
                    selectedItem = 3
                    break
                
                if vs1Button.update():
                    selectedItem = 4
                    break
            
            #get key for specialmode is pressed
            if key[pygame.K_F10] or key[pygame.K_F11]:
                #break out of loop
                break
            
            #screen.fill((83,0,7))
            
            #update background
            background_menue.update(deltaTime)
            
            #draw elements
            background_menue.draw(screen)
            bar.draw(screen)
            
            #if menue is open draw menue items
            if menueOpen:
                startButton.draw(screen)
                sandboxButton.draw(screen)
                aiLifeButton.draw(screen)
                flappyButton.draw(screen)
                vs1Button.draw(screen)
                
            #update screen
            pygame.display.flip()
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    leaveSystem()
                    break
        #gameloops 
        key = pygame.key.get_pressed()


        serverStart = False

        #check which item is selected
        if selectedItem == 0:
            #save bullets
            bullets = []
            bulletShooters = []
            
            #create player
            border = visuals.Visual(visuals.graphic.border, (-400,height))
            player = visuals.Player(visuals.graphic.hand_of_blood_walking, 100, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, height+300, height,  width, -width/2,(100, height-500))
           
            #generate generator
            generator = generators.JumpGenerator(player)
            
            #position of background
            positionOfViewX = player.x
            positionOfViewY = player.y
            
            #create environment
            background,environment,bulletShooters = generator.createEnvironment()
            
            #update time
            deltaTime = (time.clock() - lastFrameTime)
            lastFrameTime = time.clock()
            
            #for trolling purpose
            overrideRight = 0
            index = 0
            
            #subsystem running loop
            while running:
                #get key
                key = pygame.key.get_pressed()
                        
                if key[pygame.K_F4]:
                    background = [visuals.Background(visuals.graphic.background0, background[0].screenWidth, background[0].screenHeight, (0,background[0].screenHeight),0),visuals.Background("background1", background[1].screenWidth, background[1].screenHeight, (0,background[1].screenHeight),0.2),visuals.Background("background2", background[2].screenWidth, background[2].screenHeight, (0,background[2].screenHeight),0.5)]

                if key[pygame.K_TAB]:
                    import server
                    server.start()
                    severStart = True
                
                if serverStart and len(server.data) != 0:
                    t = server.data[0].split(" ")
                    
                    print(t)
    
                    if t[0] == "set":
                        player.x = int(t[1])
                        player.y = int(t[2])
                        
                        server.data[0] = ""
                        
                    elif t[0] == "game_speed":
                        player.game_speed = int(t[1])
                        
                        server.data[0] = ""
                        
                    elif t[0] == "speed":
                        player.speed = float(t[1])
                        
                        server.data[0] = ""
                        
                    elif t[0] == "gravity":
                        player.gravity = float(t[1])
                        
                        server.data[0] = ""
                    
                    elif t[0] == "right":
                        overrideRight = 1
                
                    elif t[0] == "clear":
                        overrideRight = 0
                        
                        server.data[0] = ""
                    
                    elif t[0] == "superman":
                        player.gravity = 0
                        player.game_speed = 50
                        player.speed = 100
                        
                        server.data[0] = ""

                #check if escape key is pressed
                if key[pygame.K_ESCAPE]:
                    
                    image = pygame.surfarray.array3d(screen)

                    background_game_menue.draw(screen)
                    
                    #game meune loop
                    while True:                
                        
                        #check for quit
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                leaveSystem()
                        
                        #check if item is selected
                        if resumeButton.update():
                            #update time and return to game
                            deltaTime = (time.clock() - lastFrameTime)
                            lastFrameTime = time.clock()
                            break

                        if quitButton.update():   
                            #leave game
                            running = False
                            break
                        
                        if optionButton.update():
                            
                            #display optionmenue
                            pygame.surfarray.blit_array(screen, image)
                            
                            optionWindow(screen)
                                
                            pygame.surfarray.blit_array(screen, image)
                                
                        #draw menue
                        resumeButton.draw(screen)
                        quitButton.draw(screen)
                        optionButton.draw(screen)
                
                        #update display
                        pygame.display.flip()
                        pygame.display.update()

                if key[pygame.K_e]:
                    #respawn player
                    player.respawn()
                    
                #update time
                deltaTime = (time.clock() - lastFrameTime)
                lastFrameTime = time.clock()
                
                #update player
                respawn = player.update(deltaTime, player.game_speed, key, environment, bullets, overrideRight)
                
                #adjust position of view                           
                offset_view_player = (player.x - positionOfViewX - width/2)
                
                #linear adjustment
                positionOfViewX += 0.1 * (offset_view_player/(width*2)) * deltaTime * player.speed * width/player.obj_width * player.game_speed

                #parabola adjustment
                calculated_view_adjustment = 0.0000002*(offset_view_player)*(offset_view_player) * deltaTime * player.speed * width/player.obj_width * player.game_speed
                
                #check where the parabola is positiv or negativ
                if offset_view_player < 0:
                    positionOfViewX -= calculated_view_adjustment
                else:
                    positionOfViewX += calculated_view_adjustment

                #adjust border
                generator.genrateEnvironment(environment, positionOfViewX, bulletShooters)
                player.border += 0.5* deltaTime * player.speed * player.game_speed
                
                #update and draw elements
                for obj in background:
                    obj.update(deltaTime, player.game_speed, positionOfViewX)
                    obj.draw(screen, positionOfViewX)

                for obj in environment:
                    obj.update(deltaTime, player.game_speed, positionOfViewX)
                    obj.draw(screen, positionOfViewX)
                    
                    #destroy environment objects when border is past or reduce of memory
                    if obj.x <= player.border-500:
                        environment.remove(obj)

                for bulletShooter in bulletShooters:
                    bulletShooter.update(deltaTime, player.game_speed, bullets, positionOfViewX, player)
                    bulletShooter.draw(screen, positionOfViewX)
                    
                    #destroy bulletshooter when border is past for reduce of memory
                    if bulletShooter.x <= player.border:
                        bulletShooters.remove(bulletShooter)

                for bullet in bullets:
                    bullet.update(deltaTime, player)
                    bullet.draw(screen, positionOfViewX)
                    
                #draw player
                player.draw(screen, positionOfViewX)
                
                #draw border
                border.x = player.border - border.obj_width
                border.draw(screen, positionOfViewX)
                # pygame.draw.line(screen,(255,0,0),(player.border-positionOfViewX,0),(player.border-positionOfViewX,height),5)
                
                #visual text
                visuals.displayText(screen, font5, "Coins: " + str(player.counterCoins), 1400, 10)
                
                #dsiplay FPS
                if key[pygame.K_F3]:
                    visuals.displayText(screen, font, ("0" if deltaTime == 0 else str(int(1/deltaTime))) + " FPS")
                    visuals.displayText(screen, font, str(positionOfViewX/50), 100)
                    visuals.displayText(screen, font, str(round(player.x)), 400)
                    
                #check for exit event
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        leaveSystem()
                
                #update display
                pygame.display.flip()
                pygame.display.update()
                
                if respawn:
                    #respawn player
                    
                    #clear bullets
                    bullets = []
                    
                    #reset border
                    player.border = -width/2
                    
                    #respawn player
                    player.respawn()
                    
                    #create environmet
                    background,environment,bulletShooters = generator.createEnvironment()
                    image = pygame.surfarray.array3d(screen)

                    font2Size = 20
                    spacePressed = False
                    
                    blinkingText = visuals.blinkingText(font3, "press space to continue", width/2-100, height-200, 1.5)
                    
                    while spacePressed == False:

                        #check for quit
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                leaveSystem()
                                
                        key = pygame.key.get_pressed()
                        
                        if key[pygame.K_SPACE]:
                            spacePressed = True
                        
                        #check if escape key is pressed
                        if key[pygame.K_ESCAPE]:
                            
                            background_game_menue.draw(screen)
                            
                            #game meune loop
                            while True:                
                                
                                #check for quit
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        leaveSystem()
                                
                                #check if item is selected
                                if resumeButton.update():
                                    #update time and return to game
                                    deltaTime = (time.clock() - lastFrameTime)
                                    lastFrameTime = time.clock()
                                    break
        
                                if quitButton.update():   
                                    #leave game
                                    spacePressed = True
                                    running = False
                                    break
                                
                                if optionButton.update():
                                    
                                    #display optionmenue
                                    pygame.surfarray.blit_array(screen, image)
                                    
                                    optionWindow(screen)
                                        
                                    pygame.surfarray.blit_array(screen, image)
                                        
                                #draw menue
                                resumeButton.draw(screen)
                                quitButton.draw(screen)
                                optionButton.draw(screen)
                        
                                #update display
                                pygame.display.flip()
                                pygame.display.update()

                        #respawn animation
                        font2 = pygame.font.SysFont('Papyrus', int(font2Size))
                        
                        pygame.surfarray.blit_array(screen, image)
                        visuals.displayText(screen,font2, "YOU ARE DEAD", width/2-int(font2Size*13/3), height/2-int(font2Size/2))

                        blinkingText.update(deltaTime)
                        blinkingText.draw(screen)
                        
                        if font2Size <= 70:
                            font2Size += deltaTime *18
                        
                        deltaTime = (time.clock() - lastFrameTime)
                        lastFrameTime = time.clock()
                        
                        pygame.display.update()
                    
                    #update time
                    lastFrameTime = time.clock()

        elif selectedItem == 1 :#and key[pygame.K_F10]:
            
            severStart = False
            
            players = []
            
            positionOfViewsX = []
            positionOfViewsY = []
            
            #create player
            player = visuals.SandboxPlayer(visuals.graphic.hand_of_blood, 100, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, height * 3, height, width, 0,(200, height-300))
            generator = generators.SandboxGenerator(player,1000)
            
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
                
                if severStart and len(server.data) != 0:
                    while server.index > len(players):
                        players.append(visuals.SandboxPlayer(visuals.graphic.hand_of_blood, 100, -1, -1, -1, height * 3, height, width, 0,(200, height-300)))
                        
                        positionOfViewsX.append(player.x - width/2)
                        positionOfViewsY.append(player.y - height/2)

                #get key
                key = pygame.key.get_pressed();
                
                if key[pygame.K_TAB]:
                    import server
                    server.start()
                    severStart = True

                #check if escape key is pressed
                if key[pygame.K_ESCAPE]:
                    image = pygame.surfarray.array3d(screen)

                    background_game_menue.draw(screen)
                    
                    #game meune loop
                    while True:                
                        
                        #check for quit
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                leaveSystem()
                        
                        #check if item is selected
                        if resumeButton.update():
                            #update time and return to game
                            deltaTime = (time.clock() - lastFrameTime)
                            lastFrameTime = time.clock()
                            break

                        if quitButton.update():   
                            #leave game
                            running = False
                            break
                        
                        if optionButton.update():
                            
                            #display optionmenue
                            pygame.surfarray.blit_array(screen, image)
                            
                            optionWindow(screen)
                                
                            pygame.surfarray.blit_array(screen, image)
                                
                        #draw menue
                        resumeButton.draw(screen)
                        quitButton.draw(screen)
                        optionButton.draw(screen)
                
                        #update display
                        pygame.display.flip()
                        pygame.display.update()

                #for debunging purpose
                if key[pygame.K_e]:
                    #respawn player
                    player.respawn()
                
                #fill background
                screen.fill((0,0,0))
                
                #update time
                deltaTime = (time.clock() - lastFrameTime)
                lastFrameTime = time.clock()
                
                index = 0
                #update player
                for p in players:
                    print(server.data[index])
                    t = server.data[index].split(" ")
                    
                    overrideSideways = 0
                    overrideUp = 0
                    mouse = (0,0)
                    mouse_pressed_left = 0
                    mouse_pressed_right = 0
                    
                    print(t)
                    
                    if t[0] != '':
                        overrideSideways = int(t[0])
                        overrideUp = int(t[1])
                        mouse = (int(t[2]),int(t[3]))
                        mouse_pressed_left = int(t[4])
                        mouse_pressed_right = int(t[5])
                    
                    p.update(deltaTime, player.game_speed, key, environment, positionOfViewsX[index], positionOfViewsY[index], overrideSideways, overrideUp, mouse, mouse_pressed_left, mouse_pressed_right)
                    
                    positionOfViewsX[index] += ((p.x - positionOfViewsX[index] - width/2)/(width*2)) * deltaTime * player.speed * width/player.obj_width * player.game_speed/2
                    positionOfViewsY[index] += ((p.y - positionOfViewsY[index] - height/2)/(height*2)) * deltaTime * player.speed * height/player.obj_height * player.game_speed /2
                    
                    index += 1
                
                player.update(deltaTime, player.game_speed, key, environment, positionOfViewX, positionOfViewY)

                #adjust position of view
                positionOfViewX += ((player.x - positionOfViewX - width/2)/(width*2)) * deltaTime * player.speed * width/player.obj_width * player.game_speed/2
                positionOfViewY += ((player.y - positionOfViewY - height/2)/(height*2)) * deltaTime * player.speed * height/player.obj_height * player.game_speed /2

                for i in range(len(players)):
                    changelog = str(len(players)) + " " + str(positionOfViewsX[i]) + " " + str(positionOfViewsY[i]) + " " + str(player.x) + " " + str(player.y)
                    
                    for p in players:
                        changelog += " " + str(p.x) + " " + str(p.y)
                    
                    print(changelog)
                    server.send(changelog, server.connections[i])

                #update backgound
                for obj in background:
                    obj.update(deltaTime, player.game_speed, positionOfViewX, positionOfViewY)
                    obj.draw(screen, positionOfViewX, positionOfViewY)
                                
                
                #update and draw objects in range of player
                for i in range(round(positionOfViewX/50) - 1, round(positionOfViewX/50) + 37 if round(positionOfViewX/50) + 37 <= len(environment) else len(environment)):
                    if i < 0:
                        continue
                    for i_y in range(len(environment[i])):
                        #draw environment
                        environment[i][i_y].update(deltaTime, player.game_speed, positionOfViewX, positionOfViewY)
                        environment[i][i_y].draw(screen, positionOfViewX, positionOfViewY)
                
                #draw player
                for p in players:
                    p.draw(screen ,positionOfViewX, positionOfViewY)
                    
                player.draw(screen, positionOfViewX, positionOfViewY)

                #display FPS
                if key[pygame.K_F3]:
                    visuals.displayText(screen, font, ("0" if deltaTime == 0 else str(int(1/deltaTime))) + " FPS")
                    visuals.displayText(screen, font, str(positionOfViewX/50), 100)
                    visuals.displayText(screen, font, str(round(player.x)), 400)
                
                #check for exit event
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        if serverStart:
                            server.socket_close()
                        leaveSystem()
                
                #update display
                pygame.display.flip()
                pygame.display.update()
                
        #test ai
        if selectedItem == 2:
            #import aiLife
            import aiLife
            
            displayAI = False
            gamespeed = 900
            
            if input("Type y to display best ai: ") == "y":
                displayAI = True
                gamespeed = 100
                
            #waiting screen
            screen.fill((0,0,0))
            pygame.display.update()
            
            aiLife = aiLife
            
            if displayAI:                
                aiLife = aiLife.AI("ai/bestLast.tfl")
                
            else:
                #create aiLife
                aiLife = aiLife.aiLife()
                #create first population
                aiLife.generateFirstPopulation()

            #create player
            player = visuals.Player(visuals.graphic.hand_of_blood_running, gamespeed, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, height+300, height,  width, 0,(100, height-300))
            #generate environment
            generator = generators.JumpGenerator(player, 1000)
            
            #position of background
            positionOfViewX = player.x
            positionOfViewY = 0
            
            #create Environment
            background,environment,bulletShooters = generator.createEnvironment()

            #update time
            deltaTime = (time.clock() - lastFrameTime)
            lastFrameTime = time.clock()
            
            #subsurface for screen
            #screen2 = screen.subsurface((width/2-100,0,width/2+100,height))
                        
            while running:
                #get key pressed
                key = pygame.key.get_pressed()

                #update time
                deltaTime = (time.clock() - lastFrameTime)
                lastFrameTime = time.clock()
                
                #fill background
                screen.fill((0,0,0))

                #set input of ai
                inputAI = (1,1,1,1)

                #generate input of ai
                for i in range(len(environment)):
                    if environment[i].x > player.x and environment[i].model == 1:
                        inputAI = (environment[i].x + environment[i].obj_width - player.x, environment[i].y - player.y)
                        #inputAI = (environment[i].x,environment[i].y,player.x,player.y)
                        break

                output = None
                #get next move
                if displayAI:
                    output = aiLife.getOutput([inputAI])
                else:
                    output = aiLife.population[aiLife.currentLivingAI].getOutput([inputAI])

                #convert output to movement 
                if output[0][0] >= 0.5:
                    overrideUp = True
                else:
                    overrideUp = False
                if output[0][1] >= 0.5:
                    overrideRight = True
                else:
                    overrideRight = False
                
                #update player and set override for keys
                if player.update(deltaTime, player.game_speed, key, environment, overrideRight = overrideRight, overrideUp = overrideUp):
                    #player died respawn
                    
                    #get next ai
                    if displayAI == False:
                        aiLife.getNextAI(player.fitness)
                    
                    #get border
                    player.border = 0
                    player.respawn()
                    
                    #greate new enviroment
                    background,environment,bulletShooters = generator.createEnvironment()
                    
                    #update view
                    player.x = environment[0].x + player.obj_width
                    player.y = environment[0].y - player.obj_height -10
                    
                    #update time
                    lastFrameTime = time.clock()
                            
                #adjust position of view
                positionOfViewX = player.x - width/2

                #adjust border
                generator.genrateEnvironment(environment, positionOfViewX, [])
                player.border += 0.2* deltaTime * player.speed * player.game_speed
                
                #update and draw elements
                for obj in background:
                    obj.update(deltaTime, player.game_speed, positionOfViewX)
                    if displayAI:
                        obj.draw(screen, positionOfViewX)
                
                #update environmental objects
                for obj in environment:
                    obj.update(deltaTime, player.game_speed, positionOfViewX,positionOfViewY)
                    if displayAI:
                        obj.draw(screen, positionOfViewX,positionOfViewY)
                    if obj.x <= player.border:
                        environment.remove(obj)
                        
                if displayAI:
                    player.draw(screen, positionOfViewX, positionOfViewY)
                
                    #draw border
                    pygame.draw.line(screen,(255,0,0),(player.border-positionOfViewX,0),(player.border-positionOfViewX,height),5)
                            
                #get FPS
                if key[pygame.K_F3]:
                    visuals.displayText(screen, font, ("0" if deltaTime == 0 else str(int(1/deltaTime))) + " FPS")
                    visuals.displayText(screen, font, str(positionOfViewX/50), 100)
                    visuals.displayText(screen, font, str(round(player.x)), 400)
                
                #wait for exit
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        leaveSystem()
                
                #update display
                pygame.display.flip()
                pygame.display.update()
                
        #check which item is selected
        if selectedItem == 4:
            pygame.mixer.music.play()
            #save bullets
            bullets = []
            
            #create player
            player = visuals.Player(visuals.graphic.hand_of_blood_running, 100, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, height+300, height,  width, -width/2,(100, height-500), True)
            player2 = visuals.Player(visuals.graphic.hand_of_blood_running, 100, pygame.K_a, pygame.K_d, pygame.K_w, height+300, height,  width, -width/2,(800, height-500), True)
           
            #generate generator
            generator = generators.PvPGenerator(player)
            
            #position of background
            positionOfViewX = player.x - player2.x
            positionOfViewY = player.y - player.y
            
            #create environment
            background,environment = generator.createPvPEnvironment()
            
            #update time
            deltaTime = (time.clock() - lastFrameTime)
            lastFrameTime = time.clock()
            
            #for trolling purpose
            overrideRight = 0
            index = 0
            
            #subsystem running loop
            while running:
                #get key
                key = pygame.key.get_pressed()

                #check if escape key is pressed
                if key[pygame.K_ESCAPE]:
                    
                    image = pygame.surfarray.array3d(screen)

                    background_game_menue.draw(screen)
                    
                    #game meune loop
                    while True:                
                        
                        #check for quit
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                leaveSystem()
                        
                        #check if item is selected
                        if resumeButton.update():
                            #update time and return to game
                            deltaTime = (time.clock() - lastFrameTime)
                            lastFrameTime = time.clock()
                            break

                        if quitButton.update():   
                            #leave game
                            running = False
                            break
                        
                        if optionButton.update():
                            
                            #display optionmenue
                            pygame.surfarray.blit_array(screen, image)
                            
                            optionWindow(screen)
                                
                            pygame.surfarray.blit_array(screen, image)
                                
                        #draw menue
                        resumeButton.draw(screen)
                        quitButton.draw(screen)
                        optionButton.draw(screen)
                
                        #update display
                        pygame.display.flip()
                        pygame.display.update()

                if key[pygame.K_e]:
                    #respawn player
                    player.respawn()
                    
                #update time
                deltaTime = (time.clock() - lastFrameTime)
                lastFrameTime = time.clock()
                
                #update player
                if key[pygame.K_4]:
                    player2.shootBullet(bullets)
                    
                if key[pygame.K_RSHIFT]:
                    player.shootBullet(bullets)
                
                respawn1 = player.update(deltaTime, player.game_speed, key, environment, bullets, overrideRight)
                respawn2 = player2.update(deltaTime, player.game_speed, key, environment, bullets, overrideRight)
                
                middlePlayerX = (player.x + player2.x)/2 if player.x >= player2.x else (player2.x + player.x)/2
                
                #adjust position of view                           
                offset_view_player = (middlePlayerX - positionOfViewX - width/2)
                
                #linear adjustment
                positionOfViewX += 0.1 * (offset_view_player/(width*2)) * deltaTime * player.speed * width/player.obj_width * player.game_speed

                #parabola adjustment
                calculated_view_adjustment = 0.0000002*(offset_view_player)*(offset_view_player) * deltaTime * player.speed * width/player.obj_width * player.game_speed
                
                #check where the parabola is positiv or negativ
                if offset_view_player < 0:
                    positionOfViewX -= calculated_view_adjustment
                else:
                    positionOfViewX += calculated_view_adjustment
                
                #update and draw elements
                for obj in background:
                    obj.update(deltaTime, player.game_speed, positionOfViewX)
                    obj.draw(screen, positionOfViewX)

                for obj in environment:
                    obj.update(deltaTime, player.game_speed, positionOfViewX)
                    obj.draw(screen, positionOfViewX)

                for bullet in bullets:
                    bullet.update(deltaTime, player)
                    bullet.draw(screen, positionOfViewX)
                    
                #draw player
                player.draw(screen, positionOfViewX)
                player2.draw(screen, positionOfViewX)
                
                #dsiplay FPS
                if key[pygame.K_F3]:
                    visuals.displayText(screen, font, ("0" if deltaTime == 0 else str(int(1/deltaTime))) + " FPS")
                    visuals.displayText(screen, font, str(positionOfViewX/50), 100)
                    visuals.displayText(screen, font, str(round(player.x)), 400)
                    
                #check for exit event
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        leaveSystem()
                
                #update display
                pygame.display.flip()
                pygame.display.update()
                
                if respawn1 or respawn2:
                    #respawn player
                    
                    #clear bullets
                    bullets = []
                    
                    #respawn player
                    player2.respawn()
                    player.respawn()
                    
                    image = pygame.surfarray.array3d(screen)

                    font2Size = 20
                    spacePressed = False
                    blinkingText = visuals.blinkingText(font3, "press space to continue", width/2-100, height-200, 1.5)
                    
                    while spacePressed == False:
 
                        #check for quit
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                leaveSystem()
                                
                        key = pygame.key.get_pressed()
                        
                        if key[pygame.K_SPACE]:
                            spacePressed = True
                        
                        #check if escape key is pressed
                        if key[pygame.K_ESCAPE]:
                            
                            background_game_menue.draw(screen)
                            
                            #game meune loop
                            while True:                
                                
                                #check for quit
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        leaveSystem()
                                
                                #check if item is selected
                                if resumeButton.update():
                                    #update time and return to game
                                    deltaTime = (time.clock() - lastFrameTime)
                                    lastFrameTime = time.clock()
                                    break
        
                                if quitButton.update():   
                                    #leave game
                                    spacePressed = True
                                    running = False
                                    break
                                
                                if optionButton.update():
                                    
                                    #display optionmenue
                                    pygame.surfarray.blit_array(screen, image)
                                    
                                    optionWindow(screen)
                                        
                                    pygame.surfarray.blit_array(screen, image)
                                        
                                #draw menue
                                resumeButton.draw(screen)
                                quitButton.draw(screen)
                                optionButton.draw(screen)
                        
                                #update display
                                pygame.display.flip()
                                pygame.display.update()

                        #respawn animation
                        font2 = pygame.font.SysFont('Papyrus', int(font2Size))
                        
                        pygame.surfarray.blit_array(screen, image)
                        if respawn1:
                            visuals.displayText(screen,font2, "PLAYER 2 WINS", width/2-int(font2Size*13/3), height/2-int(font2Size/2))
                        else:
                            visuals.displayText(screen,font2, "PLAYER 1 WINS", width/2-int(font2Size*13/3), height/2-int(font2Size/2))

                        blinkingText.update(deltaTime)
                        blinkingText.draw(screen)
                        
                        if font2Size <= 70:
                            font2Size += deltaTime *18
                        
                        deltaTime = (time.clock() - lastFrameTime)
                        lastFrameTime = time.clock()
                        
                        pygame.display.update()
                    
                    #update time
                    lastFrameTime = time.clock()
                    
        #check which item is selected
        if selectedItem == 3:
            
            #Flappy Bird
            
            #create bird
            bird = visuals.Bird(visuals.graphic.hanno, 100, pygame.K_SPACE, height,  width, (100, height-500))
            
            #generate generator
            generator = generators.FlappyGenerator(bird)
            #position of background
            positionOfViewX = bird.x
            
            #create environment
            background,environment = generator.createEnvironment()
            
            #update time
            deltaTime = (time.clock() - lastFrameTime)
            lastFrameTime = time.clock()
            
            #subsystem running loop
            while running:
                #get key
                key = pygame.key.get_pressed()

                #check if escape key is pressed
                if key[pygame.K_ESCAPE]:
                    
                    image = pygame.surfarray.array3d(screen)

                    background_game_menue.draw(screen)
                    
                    #game meune loop
                    while True:                
                        
                        #check for quit
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                leaveSystem()
                        
                        #check if item is selected
                        if resumeButton.update():
                            #update time and return to game
                            deltaTime = (time.clock() - lastFrameTime)
                            lastFrameTime = time.clock()
                            break

                        if quitButton.update():   
                            #leave game
                            running = False
                            break
                        
                        if optionButton.update():
                            
                            #display optionmenue
                            pygame.surfarray.blit_array(screen, image)
                            
                            optionWindow(screen)
                                
                            pygame.surfarray.blit_array(screen, image)
                                
                        #draw menue
                        resumeButton.draw(screen)
                        quitButton.draw(screen)
                        optionButton.draw(screen)
                
                        #update display
                        pygame.display.flip()
                        pygame.display.update()

                if key[pygame.K_e]:
                    #respawn player
                    bird.respawn()
                    
                #update time
                deltaTime = (time.clock() - lastFrameTime)
                lastFrameTime = time.clock()
                
                respawn = bird.update(deltaTime, key, environment)
                                
                #linear adjustment
                positionOfViewX = bird.x -200
                
                generator.genrateEnvironment(environment, positionOfViewX)
                
                #increase speed
                bird.game_speed += deltaTime * 1000 / bird.game_speed * 0.001
                
                #update and draw elements
                for obj in background:
                    obj.update(deltaTime, bird.game_speed, positionOfViewX)
                    obj.draw(screen, positionOfViewX)

                for obj in environment:
                    obj.update(deltaTime, bird.game_speed, positionOfViewX)
                    obj.draw(screen, positionOfViewX)
                    
                #draw player
                bird.draw(screen, positionOfViewX)
                
                #dsiplay FPS
                if key[pygame.K_F3]:
                    visuals.displayText(screen, font, ("0" if deltaTime == 0 else str(int(1/deltaTime))) + " FPS")
                    visuals.displayText(screen, font, str(positionOfViewX/50), 100)
                    visuals.displayText(screen, font, str(round(player.x)), 400)
                    
                #check for exit event
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        leaveSystem()
                
                #update display
                pygame.display.flip()
                pygame.display.update()
                
                if respawn:
                    #respawn player
                    
                    #respawn
                    bird.respawn()
                    bird.game_speed = 100
                    bird.forceUp = 0
                    
                    #create environment
                    background,environment = generator.createEnvironment()
                    
                    image = pygame.surfarray.array3d(screen)

                    font2Size = 20
                    spacePressed = False
                    blinkingText = visuals.blinkingText(font3, "press space to continue", width/2-100, height-200, 1.5)
                    
                    while spacePressed == False:

                        #check for quit
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                leaveSystem()
                                
                        key = pygame.key.get_pressed()
                        
                        if key[pygame.K_SPACE]:
                            spacePressed = True
                        
                        #check if escape key is pressed
                        if key[pygame.K_ESCAPE]:
                            
                            background_game_menue.draw(screen)
                            
                            #game meune loop
                            while True:                
                                
                                #check for quit
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        leaveSystem()
                                
                                #check if item is selected
                                if resumeButton.update():
                                    #update time and return to game
                                    deltaTime = (time.clock() - lastFrameTime)
                                    lastFrameTime = time.clock()
                                    break
        
                                if quitButton.update():   
                                    #leave game
                                    spacePressed = True
                                    running = False
                                    break
                                
                                if optionButton.update():
                                    
                                    #display optionmenue
                                    pygame.surfarray.blit_array(screen, image)
                                    
                                    optionWindow(screen)
                                        
                                    pygame.surfarray.blit_array(screen, image)
                                        
                                #draw menue
                                resumeButton.draw(screen)
                                quitButton.draw(screen)
                                optionButton.draw(screen)
                        
                                #update display
                                pygame.display.flip()
                                pygame.display.update()

                        #respawn animation
                        font2 = pygame.font.SysFont('Papyrus', int(font2Size))
                        
                        pygame.surfarray.blit_array(screen, image)
                        visuals.displayText(screen,font2, "YOU ARE DEAD", width/2-int(font2Size*13/3), height/2-int(font2Size/2))

                        blinkingText.update(deltaTime)
                        blinkingText.draw(screen)
                        
                        if font2Size <= 70:
                            font2Size += deltaTime *18
                        
                        deltaTime = (time.clock() - lastFrameTime)
                        lastFrameTime = time.clock()
                        
                        pygame.display.update()
                    
                    #update time
                    lastFrameTime = time.clock()