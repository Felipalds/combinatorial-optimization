from math import *

class Individual:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.individual_percentage = None
        self.fitness = (self.x * sin(4 * pi * self.x) - self.y * sin(4 * pi * self.y + pi) + 1)


    def setPercentage(self, percentage) -> None:
        self.individual_percentage = percentage

    def getFitness(self) -> float:
        return self.fitness

    def getPercentage(self) -> None:
        return self.individual_percentage
