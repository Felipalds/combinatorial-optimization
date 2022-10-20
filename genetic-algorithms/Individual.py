from math import *
DECIMAL = 4

class Individual:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.fitness = round((self.x * sin(4 * pi * self.x) - self.y * sin(4 * pi * self.y + pi) + 1), DECIMAL)

    def setPercentage(self, percentage):
        self.individual_percentage = round(percentage, DECIMAL)

    def getFitness(self):
        return self.fitness

    def getPercentage(self):
        return self.individual_percentage
