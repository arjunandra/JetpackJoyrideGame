from screen import Screen
from person import Mando, Boss
from config import *
from utility import NonBlockingInput, keyPressed, clearScreen as c
from time import sleep, monotonic
from objects import MandoBullet, BossBullet
import sys

class Game():
    """
        Entire Game
    """

    def generateObjects(self):

        # Object Generation
        for i in range(COINB_COUNT):
            self.screen.coins[i].put(self.screen.map, 1)

        for i in range(HLAZER_COUNT):
            self.screen.horizontalLazers[i].put(self.screen.map, 2)

        for i in range(VLAZER_COUNT):
            self.screen.verticalLazers[i].put(self.screen.map, 2)

        for i in range(DLAZER_COUNT):
            self.screen.diagonalLazers[i].put(self.screen.map, 2)
        
        for i in range(MAGNET_COUNT):
            self.screen.magnets[i].put(self.screen.map, 5)

    def __init__(self, gameTime):
        self.screen = Screen()
        self.player = Mando(self.screen.map)

        self.generateObjects()

        #self.screen.coin.put(self.screen.map, self.screen.coin.id)
        self.startTime = monotonic()
        self.endTime = self.startTime + gameTime
        self.timeRemaining = gameTime
        self.points = 0
        self.mandoBullets = []
        self.bossBullets = []
        self.shield = False
        self.shieldTime = None
        self.shieldCount = 1
        self.leftBorder = WIDTH - 165
        self.rightBorder = WIDTH - 1
        self.invincibleTill = self.timeRemaining
        self.bossActive = False

        # Initialize Sky & Ground
        self.screen.map[0:SKY_HEIGHT, 0 : WIDTH] = -1
        self.screen.map[GROUND_HEIGHT:HEIGHT + 1, 0 : WIDTH] = -2

    def timer(self):
        self.timeRemaining -= 1

    def activateBoss(self):
        self.bossActive = True
        self.boss = Boss(self.screen.map)
        
    def nextState(self, key):

        if key == 1 and self.player.location[1] == self.leftBorder:
            return -1

        moveMade = self.player.move(self.screen.map, key, 2)

        if key == 2:
            if self.rightBorder < WIDTH:
                self.rightBorder += 1

            if self.leftBorder < WIDTH - 164:
                self.leftBorder += 1   

        elif key == 1:
            if self.rightBorder > 164:
                self.rightBorder -= 1
            
            if self.leftBorder > 0:
                self.leftBorder -= 1

        if self.shield == True and self.shieldTime > self.timeRemaining:
            self.shield = False

        if self.shieldCount == 0 and self.timeRemaining < self.shieldTime - 60:
            self.shieldCount += 1
            self.invincibleTill = self.timeRemaining - 3

        if moveMade == 1:
            self.points += 1
        elif moveMade == 2:

            if self.shield == True:
                self.shield = False
            
            else:
                if self.invincibleTill > self.timeRemaining:
                    self.player.lives -= 1
                    self.invincibleTill = self.timeRemaining - 3
                
            
        elif moveMade == 3:
            bullet = MandoBullet(self.player.location)
            bullet.put(self.screen.map, bullet.id)
            bullet.inMotion = True
            self.mandoBullets.append(bullet)
            return 1

        elif moveMade == 4:
            self.activateShield()

        # Boss Movement
        if self.bossActive == True:
            if self.player.location[0] == self.boss.location[0]:
                pass
            elif self.player.location[0] < self.boss.location[0]:
                self.boss.move(self.screen.map, 0, 2)
            else:
                self.boss.move(self.screen.map, 1, 2)

        # Boss Bullets
        if self.bossActive == True and self.timeRemaining % 3 == 0:
            bullet = BossBullet(self.boss.location)
            bullet.put(self.screen.map, bullet.id)
            bullet.inMotion = True

            self.bossBullets.append(bullet)

        return 0

            # self.player.location = MANDO_INIT_LOCATION
            # self.player.put(self.screen.map, self.player.id)

    def activateShield(self):

        if self.shieldCount > 0:
            self.shield = True
            self.shieldTime = self.timeRemaining - 5
            self.shieldCount -= 1

    def clearObjects(self):
        # Object Clearing
        for i in range(COINB_COUNT):
            self.screen.coins[i].put(self.screen.map, 0)

        for i in range(HLAZER_COUNT):
            self.screen.horizontalLazers[i].put(self.screen.map, 0)

        for i in range(VLAZER_COUNT):
            self.screen.verticalLazers[i].put(self.screen.map, 0)

        for i in range(DLAZER_COUNT):
            self.screen.diagonalLazers[i].put(self.screen.map, 0)

        for i in range(MAGNET_COUNT):
            self.screen.magnets[i].put(self.screen.map, 0)

    def mandoBulletMovement(self, bullet):

        bullet.inMotion = True
        bullet.put(self.screen.map, 0)
        newLocations = self.screen.map[bullet.location[0], bullet.location[1] : bullet.location[1] + 3]
        
        bullet.location[1] += 3

        count = 0

        for i in newLocations:
                
            if i == 1:
                self.screen.map[bullet.location[0], bullet.location[1] - 3 + count] = 1
                bullet.put(self.screen.map, 1)
                return 1

            elif i == 2:
                self.screen.map[bullet.location[0], bullet.location[1] - 3 + count] = 0
                bullet.inMotion = False
                return 2

            elif i == 9:
                self.boss.lives -= 1
            
            else:
                bullet.put(self.screen.map, bullet.id)

            count += 1

    def bossBulletMovement(self, bullet):

        bullet.inMotion = True
        bullet.put(self.screen.map, 0)
        newLocations = self.screen.map[bullet.location[0] - bullet.size[0] + 1 : bullet.location[0] + 1, bullet.location[1] - 1]
        #print(newLocations)
        for i in newLocations:
            if i == 8:
                self.player.lives -= 1

        bullet.location[1] -= 3
        bullet.put(self.screen.map, bullet.id)

    def magnetGravity(self):
        
        for i in self.screen.magnets:
            if self.player.location[1] + 10 >= i.location[1] and i.location[1] + 10 <= self.player.location[1]:

                if self.player.location[0] < i.location[0] and self.player.location[0] < GROUND_HEIGHT:
                    moveMade = self.player.move(self.screen.map, 5, 1)

                    if moveMade == 1:
                        self.points += 1
                    elif moveMade == 2:

                        if self.shield == True:
                            self.shield = False
                        
                        else:
                            if self.invincibleTill == None or self.invincibleTill > self.timeRemaining:
                                self.player.lives -= 1
                                self.invincibleTill = self.timeRemaining - 3

                elif self.player.location[0] >= i.location[0] and self.player.location[0] - MANDO_SIZE[0] > SKY_HEIGHT:

                    moveMade = self.player.move(self.screen.map, 0, 1)

                    if moveMade == 1:
                        self.points += 1
                    elif moveMade == 2:

                        if self.shield == True:
                            self.shield = False
                        
                        else:
                            if self.invincibleTill == None or self.invincibleTill > self.timeRemaining:
                                self.player.lives -= 1
                                self.invincibleTill = self.timeRemaining - 3

                if self.player.location[1] < i.location[1] and self.player.location[1] <= self.rightBorder - 2:

                    moveMade = self.player.move(self.screen.map, 2, 1)

                    if moveMade == 1:
                        self.points += 1
                    elif moveMade == 2:

                        if self.shield == True:
                            self.shield = False
                        
                        else:
                            if self.invincibleTill == None or self.invincibleTill > self.timeRemaining:
                                self.player.lives -= 1
                                self.invincibleTill = self.timeRemaining - 3

                elif self.player.location[1] >= i.location[1] and self.player.location[0] - 1 >= self.leftBorder:

                    moveMade = self.player.move(self.screen.map, 1, 1)

                    if moveMade == 1:
                        self.points += 1
                    elif moveMade == 2:

                        if self.shield == True:
                            self.shield = False
                        
                        else:
                            if self.invincibleTill == None or self.invincibleTill > self.timeRemaining:
                                self.player.lives -= 1
                                self.invincibleTill = self.timeRemaining - 3

    def clearScreen(self):
         print("\033c")

    def redraw(self):
        # sys.stdout.flush()
        # sys.stdout.write("\x1bc")
        sys.stdout.write("\033[0;0H]")
        self.screen.render(self.leftBorder - 1, self.rightBorder)
        
        if self.shield == True:
            sys.stdout.write(f"SHEILD ACTIVE\nScore: {self.points}\n")
        else:
            sys.stdout.write(f"Score: {self.points}\n")
        
        if self.bossActive == False:
            sys.stdout.write(f"Lives: {self.player.lives}\nTime Remaining: {self.timeRemaining}\n")
        else:
            sys.stdout.write(f"Lives: {self.player.lives}\nTime Remaining: {self.timeRemaining}\nBoss Lives: {self.boss.lives}")
            
    def getRemainingTime(self):
        return self.endTime - monotonic()

    def getSpentTime(self):
        return monotonic() - self.startTime

    def play(self):
        pass
    
    def gravity(self):
        moveMade = self.player.move(self.screen.map, 5, 1)

        if moveMade == 1:
            self.points += 1
        elif moveMade == 2:

            if self.shield == True:
                self.shield = False
            
            else:
                if self.invincibleTill == None or self.invincibleTill > self.timeRemaining:
                    self.player.lives -= 1
                    self.invincibleTill = self.timeRemaining - 3
            
            


        
