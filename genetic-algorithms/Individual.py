from math import *
import numpy as np
import random

class Individual:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.individual_percentage = None
        self.fitness = (self.x * sin(4 * pi * self.x) - self.y * sin(4 * pi * self.y + pi) + 1)


    def setFitness(self):
        self.fitness = (self.x * sin(4 * pi * self.x) - self.y * sin(4 * pi * self.y + pi) + 1)
    def setPercentage(self, percentage) -> None:
        self.individual_percentage = percentage

    def getFitness(self) -> float:
        return self.fitness

    def getPercentage(self) -> None:
        return self.individual_percentage

    def definer(self, value, M, m):
        if value > M:
            return M
        elif value < m:
            return M
        else:
            return value

    def cross(self, parentA, parentB, beta):
        print("Crossing")
        self.x = beta * parentA.x + (1 - beta) * parentB.x
        self.x = self.definer(self.x, 0.5, 0)
        self.y = beta * parentA.y + (1 - beta) * parentB.y
        self.y = self.definer(self.x, 0.5, 0)
        self.setFitness()

    def mutate(self, alpha):
        p = random.uniform(0, 1)
        if p < 0.05:
            print("Mutating")
            normX = np.random.normal(0, alpha)
            self.x += normX
            self.x = self.definer(self.x, 0.5, 0)
            self.y += normX
            self.y = self.definer(self.y, 0.5, 0)
        else:
            print("Not mutating")
        self.setFitness()

