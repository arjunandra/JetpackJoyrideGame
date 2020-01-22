import numpy as np
import sys
from config import *
from objects import Coin, horizontalLazer, verticalLazer, diagonalLazer, Magnet
from random import randint

class Screen():
    def __init__(self):
        self.map = np.zeros([HEIGHT, WIDTH])
        self.currentFrame = []
        self.coins = []
        self.horizontalLazers = []
        self.verticalLazers = []
        self.diagonalLazers = []
        self.magnets = []
        self.locationsUsed = []

        for i in range(RANDOM_OBJECT_COUNT):

            if i < COINB_COUNT:

                randLocation = [randint(SKY_HEIGHT + COIN_SIZE[0] + 1, GROUND_HEIGHT - COIN_SIZE[0] - 1), randint(MANDO_SIZE[1], WIDTH - COIN_SIZE[1] - 1)]

                while randLocation in self.locationsUsed == True:
                    randLocation = [randint(SKY_HEIGHT + COIN_SIZE[0] + 1, GROUND_HEIGHT - COIN_SIZE[0] - 1), randint(MANDO_SIZE[1], WIDTH - COIN_SIZE[1] - 1)]

                coin = Coin(randLocation)
                self.coins.append(coin)

            elif i < HLAZER_COUNT + COINB_COUNT:

                randLocation = [randint(SKY_HEIGHT + 1, GROUND_HEIGHT - 1), randint(MANDO_SIZE[1], WIDTH - HLAZER_SIZE[1] - 165)]

                while randLocation in self.locationsUsed == True:
                    randLocation = [randint(SKY_HEIGHT + 1, GROUND_HEIGHT - 1), randint(MANDO_SIZE[1], WIDTH - HLAZER_SIZE[1] - 165)]

                lazer = horizontalLazer(randLocation)
                self.horizontalLazers.append(lazer)

            elif i < HLAZER_COUNT + COINB_COUNT + VLAZER_COUNT:

                randLocation = [randint(SKY_HEIGHT + VLAZER_SIZE[0] + 1, GROUND_HEIGHT - VLAZER_SIZE[0] - 3), randint(MANDO_SIZE[1], WIDTH - 165)]

                while randLocation in self.locationsUsed == True:
                    randLocation = [randint(SKY_HEIGHT + VLAZER_SIZE[0] + 1, GROUND_HEIGHT - 1), randint(MANDO_SIZE[1], WIDTH - 165)]

                lazer = verticalLazer(randLocation)
                self.verticalLazers.append(lazer)

            elif i < HLAZER_COUNT + COINB_COUNT + VLAZER_COUNT + DLAZER_COUNT:

                randLocation = [randint(SKY_HEIGHT + 1, GROUND_HEIGHT - DLAZER_SIZE[0]), randint(MANDO_SIZE[1], WIDTH - DLAZER_SIZE[1] - 165)]

                while randLocation in self.locationsUsed == True:
                    randLocation = [randint(SKY_HEIGHT + 1, GROUND_HEIGHT - DLAZER_SIZE[0]), randint(MANDO_SIZE[1], WIDTH - DLAZER_SIZE[1] - 165)]

                lazer = diagonalLazer(randLocation)
                self.diagonalLazers.append(lazer)

            elif i < HLAZER_COUNT + COINB_COUNT + VLAZER_COUNT + DLAZER_COUNT + MAGNET_COUNT:

                randLocation = [randint(SKY_HEIGHT + 2, GROUND_HEIGHT - 1), randint(MANDO_SIZE[1], WIDTH - MAGNET_SIZE[1] - 165)]

                while randLocation in self.locationsUsed == True:
                    randLocation = [randint(SKY_HEIGHT + 2, GROUND_HEIGHT - 1), randint(MANDO_SIZE[1], WIDTH - MAGNET_SIZE[1] - 165)]

                magnet = Magnet(randLocation)
                self.magnets.append(magnet)
            self.locationsUsed.append(randLocation)

        

    # def collision(self, playerLocation, coinLocations, lazerLocations):
        
    #     if any(playerLocation in coinLocations):
    #         return 0
    #     elif any(playerLocation in lazerLocations):
    #         return 1

    #     return -1
            

    def render(self, leftBorder, rightBorder):
        """Print The Game Screen""" 

        objectMap = {
            -1: "S",
            -2: "G",
            0: " ",
            1: "C",
            2: "L",
            3: "B",
            4: "L",
            5: "A",
            8: "M",
            9: "Q"
        }

        self.currentFrame = self.map[0 : HEIGHT, leftBorder : rightBorder]

        # for i in range(0, HEIGHT):
        #     for j in range(0, WIDTH):
        #         sys.stdout.write(objectMap[self.map[i, j]])

        #     sys.stdout.write("\n")

        # buff = "\n".join(
        #     [
        #         f"{''.join([objectMap[pixel] for pixel in row])}"
        #         for row in self.map
        #     ]
        # )
        # sys.stdout.write(buff + "\n")
        for i in self.currentFrame:
            for j in i:
                sys.stdout.write(objectMap[j])

            sys.stdout.write("\n")
    