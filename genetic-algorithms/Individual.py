from math import *

class Individual:

    def __init__(self, x, y, rounder : int = 4) -> None:
        self.x = x
        self.y = y
        self.individual_percentage = None
        self.fitness = round((self.x * sin(4 * pi * self.x) - self.y * sin(4 * pi * self.y + pi) + 1), rounder)
        self.rounder = rounder

    def setPercentage(self, percentage) -> None:
        self.individual_percentage = round(percentage, self.rounder)

    def getFitness(self) -> float:
        return self.fitness

    def getPercentage(self) -> None:
        return self.individual_percentage
