from main import Game
from utility import NonBlockingInput, keyPressed, clearScreen as c
from config import *
from time import sleep, monotonic
from objects import MandoBullet, BossBullet
import sys

g = Game(100)

keys = NonBlockingInput()
keys.NBISetupTerminal()

counter = 0
bulletFlag = False

coinLocations = []
lazerLocations = []

for location in g.screen.locationsUsed:

    if counter < COINB_COUNT:

        coinLocations.append(g.screen.map[location[0] - COIN_SIZE[0] : location[0], location[1] : location[1] + COIN_SIZE[1]])

    elif counter < COINB_COUNT + HLAZER_COUNT:
            
        lazerLocations.append(g.screen.map[location[0], location[1] : location[1] + HLAZER_SIZE[1]])

    elif counter < COINB_COUNT + HLAZER_COUNT + VLAZER_COUNT:
            
        lazerLocations.append(g.screen.map[location[0] - VLAZER_SIZE[0] : location[0], location[1]])

    
    counter += 1
                
i = 0

while g.player.lives > 0 and g.timeRemaining > 0:

    if i == 20:
        g.timer()
        i = 0

    c()
    g.redraw()

    input = ''

    if keys.isKeyPressed() == True:
        
        input = keys.getCharecter()
    
    val = g.nextState(keyPressed(input))

    if val == 1:
        bulletFlag = True

    if bulletFlag == True:
        for j in g.mandoBullets:
            if j.location[1] < g.rightBorder - 2 and j.inMotion == True:
                output = g.mandoBulletMovement(j)

                if output == 1:
                    g.screen.map[j.location[0], j.location[1] : j.location[1] + 2] = 1
                elif output == 2:
                    g.screen.map[j.location[0], j.location[1] + 1] = 0
                    j.put(g.screen.map, 0)
            else:
                j.put(g.screen.map, 0)
                j.inMotion = False

    if g.boss.lives <= 0:
        g.boss.put(g.screen.map, 0)

    if g.bossActive == True:
        if len(g.bossBullets) > 1:
            for j in g.bossBullets:
                if j.location[1] >= 0 and j.inMotion == True:
                    g.bossBulletMovement(j)

                else:
                    j.put(g.screen.map, 0)
        
        elif len(g.bossBullets) == 1:
            #print(g.bossBullets)
            if g.bossBullets[0].location[1] >= 0 and g.bossBullets[0].inMotion == True:
                #print("imin")
                g.bossBulletMovement(g.bossBullets[0])


    playerLocation = g.screen.map[g.player.location[0] - MANDO_SIZE[0] : g.player.location[0], g.player.location[1] : g.player.location[1] + 1]


    # collisionCheck = g.screen.collision(playerLocation, coinLocations, lazerLocations)

    # if collisionCheck == 0
    #     g.points += 1
    # elif collisionCheck == 1:
    #     g.player.lives -= 1
    #     g.player.location = MANDO_INIT_LOCATION
    #     g.player.put(g.screen.map, g.player.id)
    

    # for playerLocation in playerLocations:

    #     if playerLocation in locationSpace:

    #         # Interacting With Coin
    #         if counter < COINB_COUNT:
    #             g.points += 1
            
    #         # Interacting With Lazer
    #         elif counter < COINB_COUNT + VLAZER_COUNT + HLAZER_COUNT:
    #             g.player.lives -= 1
    #             g.player.location = MANDO_INIT_LOCATION
    #             g.player.put(g.screen.map, g.player.id)

        

    # 
    # if locationNumber < COINB_COUNT:
    #     g.points += 1

    # #
    # elif locationNumber < COINB_COUNT + HLAZER_COUNT + VLAZER_COUNT:
    #     pass

    # Gravity Logic
    if g.player.location[0] < GROUND_HEIGHT - 1:
        g.gravity()

    # Activate Boss
    if g.rightBorder == WIDTH:
        g.activateBoss()
        g.clearObjects()

    # Move Background
    if g.rightBorder < WIDTH:
        g.rightBorder += 1

    if g.leftBorder < WIDTH - 164:
        g.leftBorder += 1   

    if g.leftBorder < WIDTH - 164:
        g.nextState(keyPressed('d'))
    
    # Magnet Gravity
    #g.magnetGravity()

    keys.flush()

    # while currentFrame - g.getRemainingTime() < 0.07:
    #     continue
    sleep(0.05)
    i += 1