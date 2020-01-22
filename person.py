from config import *
import numpy as np 


class Base():
    """
    Base Class For All Objects
    """

    def __init__(self):
        self.id = None
        self.location = []
        self.size = []

    def put(self, map, id):
        
        # for i in range(0, HEIGHT):
        #     for j in range(0, WIDTH):
        #         if i in range(self.location[0] - self.size[0] + 1, self.location[0] + 1) and j in range(self.location[1], self.location[1] + self.size[1]):
        #             map[i, j] = self.id

        #         else:
        #             map[i, j] = 0
        #print(self.size)
     
        # map[self.location[0]-self.size[0] + 1:self.location[0]+1,self.location[1]:self.location[1] + self.size[1]] = np.full([self.size[0], self.size[1]], id)
        map[self.location[0]-self.size[0] + 1:self.location[0]+1,self.location[1]:self.location[1] + self.size[1]] = id


class Person(Base):
    """
    Base Class For All People
    """

    def __init__(self):
        super().__init__()
        self.lives = None
    
    def interact(self, map, obj1, obj2):
        if obj1 == "M" and obj2 == "L":
            pass

    def move(self, map, key, val):
        
        returnFlag = -1


        if key == 0 and self.location[0] - MANDO_SIZE[0] - 1 > SKY_HEIGHT:

            try:
                newLocations = map[self.location[0] - MANDO_SIZE[0] - 1, self.location[1] : self.location[1] + 2]
                
                
                if len(newLocations) != 0:
                    
                    try:
                        for i in newLocations:
                            if i == 1:
                                returnFlag = 1
                            elif i == 2:
                                returnFlag = 2

                    except:
                        pass
                
                self.put(map, 0)
                self.location[0] -= val
                self.put(map, self.id)

            except IndexError:
                self.put(map, self.id)

        elif key == 1:

            try:
                newLocations = map[self.location[0] - MANDO_SIZE[0] + 1 : self.location[0] + 1, self.location[1] - 1]
                

                if len(newLocations) != 0:
                    try:
                        for i in newLocations:
                            if i == 1:
                                returnFlag = 1
                            elif i == 2:
                                returnFlag = 2

                    except:
                        pass

                self.put(map, 0)
                self.location[1] -= val
                self.put(map, self.id)

            except:
                self.location[1] += val
                self.put(map, self.id)

        elif key == 2:

            try:
                newLocations = map[self.location[0] - MANDO_SIZE[0] + 1 : self.location[0] + 1, self.location[1] + 2]
                
                if len(newLocations) != 0:
                    try:
                        for i in newLocations:
                            if i == 1:
                                returnFlag = 1
                            elif i == 2:
                                returnFlag = 2

                    except:
                        pass

                self.put(map, 0)
                self.location[1] += val
                self.put(map, self.id)

            except:
                self.put(map, self.id)

        elif key == 3:
            returnFlag = 3

        elif key == 4:
            returnFlag = 4

        # Gravity
        elif key == 5:

            newLocations = map[self.location[0] + 1, self.location[1] : self.location[1] + 2]

            if len(newLocations) != 0:
                    
                try:
                    for i in newLocations:
                        if i == 1:
                            returnFlag = 1
                        elif i == 2:
                            returnFlag = 2

                except:
                    pass
                
            self.put(map, 0)
            self.location[0] += val
            self.put(map, self.id)

            

        return returnFlag
    

class Mando(Person):
    """
    Mandalorian Charecter
    """

    def __init__(self, map):
        super().__init__()
        self.id = 8
        self.size = MANDO_SIZE
        self.location = MANDO_INIT_LOCATION
        self.lives = MANDO_LIVES

        self.put(map, self.id)

class Boss(Person):
    """
    Boss Charecter
    """

    def __init__(self, map):
        super().__init__()
        self.id = 9
        self.size = BOSS_SIZE
        self.location = BOSS_INIT_LOCATION
        self.lives = BOSS_LIVES

        self.put(map, self.id)

    def move(self, map, key, val):

        returnFlag = -1

        if key == 0 and self.location[0] - BOSS_SIZE[0] - 1 > SKY_HEIGHT:

            newLocations = map[self.location[0] - MANDO_SIZE[0] - 1, self.location[1] : self.location[1] + BOSS_SIZE[1]]
            
            
            if len(newLocations) != 0:
                
                try:
                    for i in newLocations:
                        if i == 1:
                            returnFlag = 1
                        elif i == 2:
                            returnFlag = 2

                except:
                    pass
            
            self.put(map, 0)
            self.location[0] -= val
            self.put(map, self.id)

        elif key == 1:

            newLocations = map[self.location[0] + 1, self.location[1] : self.location[1] + BOSS_SIZE[1]]

            if len(newLocations) != 0:
                    
                try:
                    for i in newLocations:
                        if i == 1:
                            returnFlag = 1
                        elif i == 2:
                            returnFlag = 2

                except:
                    pass
                
            self.put(map, 0)
            self.location[0] += val
            self.put(map, self.id)

        return returnFlag