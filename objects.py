from person import Base
from config import * 
from random import randint
import numpy as np

class MandoBullet(Base):
    """
    Mando Bullet Class
    """
    def __init__(self, playerLocation):
        super().__init__()
        self.id = 3
        self.size = MANDO_BULLET_SIZE
        self.location = [playerLocation[0] - MANDO_SIZE[0] + 2, playerLocation[1] + 2]
        self.inMotion = False

    def put(self, map, id):
        map[self.location[0], self.location[1] : self.location[1] + MANDO_BULLET_SIZE[1]] = id

class BossBullet(Base):
    """
    Boss Bullet Class
    """
    def __init__(self, bossLocation):
        super().__init__()
        self.id = 4
        self.size = BOSS_BULLET_SIZE
        self.location = [bossLocation[0], bossLocation[1] - 1]
        self.inMotion = False

    def put(self, map, id):
        #print(map[self.location[0] : self.location[0] + self.size[0], self.location[1] - 1])
        map[self.location[0] - self.size[0] + 1 : self.location[0] + 1, self.location[1] - 1] = id


class Coin(Base):
    """
    Coins Class
    """
    def __init__(self, location):
        super().__init__()
        self.id = 3
        self.size = COIN_SIZE
        self.location = location
       
class horizontalLazer(Base):
    """
    Horizontal Lazer Class
    """
    def __init__(self, location):
        super().__init__()
        self.id = 2
        self.size = HLAZER_SIZE
        self.location = location

class verticalLazer(Base):
    """
    Vertical Lazer Class
    """
    def __init__(self, location):
        super().__init__()
        self.id = 2
        self.size = VLAZER_SIZE
        self.location = location

class diagonalLazer(Base):
    """
    Diagonal Lazer Class
    """
    def __init__(self, location):
        super().__init__()
        self.id = 2
        self.size = DLAZER_SIZE
        self.location = location

    def put(self, map, id):

        for i in range(self.location[0], self.location[0] + DLAZER_SIZE[0]):
            for j in range(self.location[1], self.location[1] + DLAZER_SIZE[1]):
                if i == j:
                    map[i, j] = id

class Magnet(Base):
    """
    Magnet Class
    """
    def __init__(self, location):
        super().__init__()
        self.id = 5
        self.size = MAGNET_SIZE
        self.location = location