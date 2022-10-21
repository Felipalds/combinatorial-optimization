from math import *
import random
from Individual import Individual
DECIMAL = 4

class Algorithm:

    def __init__(self, init_population=None, pop_size=100, auto_gen=True, rounder=4) -> None:
        self.rounder = rounder
        self.population = init_population
        self.nxt_population = []
        self.fitsum = 0
        self.pop_size = pop_size
        if not init_population:
            self.population = []
        #
        if auto_gen and len(self.population) == 0:
            self.generatePopulation()
        self.setPercentages()

    def getFitSum(self):
        self.fitsum = sum([ind.getFitness() for ind in self.population])
        return self.fitsum

    def setPopulation(self, array_like):
        self.pop_size = len(array_like)
        self.population = array_like

    def generatePopulation(self, space=[0, 0.5].copy()):
        for i in range(self.pop_size):
            genX = round(random.uniform(*space), self.rounder)
            genY = round(random.uniform(*space), self.rounder)
            ind = Individual(genX, genY)
            self.population.append(ind)
        self.setPercentages()

    def setPercentages(self):
        for i in range(self.pop_size):
            self.population[i].setPercentage(self.population[i].getFitness() * 100 / self.getFitSum())

    def crossPopulation(self, beta : float = None) -> Individual:
        parentA = self.rouletteSelection()
        parentB = self.rouletteSelection()

        if parentA == parentB or not parentA or not parentB:
            return None
        
        if not beta:
            beta = round(random.uniform(0, 1), self.rounder)
        fx = round(beta*parentA.x + (1-beta)*parentB.x, self.rounder)
        fy = round(beta*parentA.y + (1-beta)*parentB.y, self.rounder)

        child = Individual(fx, fy)
        return child

    def generateNextGeneration(self):
        # elitism

        for i in range(self.pop_size):
            child = self.crossPopulation()
            while(child == None):
                child = self.crossPopulation()

            self.nxt_population.append(child)
            #print(f"Got child.{i}")

    def rouletteSelection(self):
        sumChance = 0
        for ind in (self.population):
            selectedChance = round(random.uniform(0, 100), self.rounder)
            sumChance += ind.getPercentage()
            if ind and selectedChance < sumChance:
                return ind
        return None

    def showIndividuals(self, amount):
        if not amount:
            amount = self.pop_size
        for i in range(amount):
            print("Elemento", i)
            print("Elemento X", self.population[i].x)
            print("Elemento Y", self.population[i].y)
            print("Fitness: ", self.population[i].fitness)
            print("Percentage: ", self.population[i].getPercentage())

    def showStatus(self):
        print("Population size: ", self.pop_size)
        print("Total fitness: ", self.getFitSum())

    def steadyRun(self, i_times : int = 100, status_show : bool = True):
        for i in range(i_times):
            if status_show: print(f"Generation {i}", [f"{self.population.index(i)}X:{i.x}Y:{i.y}" for i in self.population])
            self.generateNextGeneration()
            self.population = list(self.nxt_population)
            self.nxt_population = []
            self.setPercentages()

algorithm = Algorithm()
#algorithm.showIndividuals()

algorithm.steadyRun(100, status_show=True)
"""
algorithm.showIndividuals(100)
algorithm.showStatus()"""
