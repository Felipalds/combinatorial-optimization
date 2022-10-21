from math import *
import random
from Individual import Individual
import numpy as np


class Algorithm:

    def __init__(self, init_population=None, auto_gen=True) -> None:

        self.pop_size = int(input("Population size: "))
        self.generation_times = int(input("Generaion times: "))

        self.population = init_population
        self.nxt_population = []
        self.fitsum = 0
        self.best_individual = Individual(0.0001, 0.0001)
        self.elite = Individual(0.0001, 0.0001)
        if not init_population:
            self.population = []
        #
        if auto_gen and len(self.population) == 0:
            self.generatePopulation()

    def getFitSum(self):
        self.fitsum = sum([ind.getFitness() for ind in self.population])
        return self.fitsum

    def setPopulation(self, array_like):
        self.pop_size = len(array_like)
        self.population = array_like

    def generatePopulation(self, space=[0, 0.5].copy()):
        for i in range(self.pop_size):
            genX = random.uniform(*space)
            genY = random.uniform(*space)
            ind = Individual(genX, genY)
            self.population.append(ind)
        self.setPercentages()

    def setPercentages(self):

        for i in range(self.pop_size):
            self.population[i].setPercentage(self.population[i].getFitness() * 100 / self.getFitSum())

    def crossPopulation(self) -> list[Individual]:

        childs = []

        parentA = self.rouletteSelection()
        parentB = self.rouletteSelection()

        while parentA == parentB or not parentA or not parentB:
            parentA = self.rouletteSelection()
            parentB = self.rouletteSelection()
        
        beta = random.uniform(0, 1)
        cross_change_A = random.uniform(0, 1) #used is 75
        cross_change_B = random.uniform(0, 1) #used is 75

        print("BETA :",beta)
        print("CROSS CHANGE :", cross_change_A)

        if(cross_change_A < 0.75):
            print("Parent A x: ", parentA.x)
            print("Parent B x: ", parentB.x)

            print("Parent A y: ", parentA.y)
            print("Parent B y: ", parentB.y)
            childA_x = beta * parentA.x + (1 - beta) * parentB.x
            childA_y = beta * parentA.y + (1 - beta) * parentB.y
            print("CHILD A X before", childA_x)
            print("CHILD A Y before", childA_y)

            normX = np.random.normal(0, 0.00005)
            print("NORMAL DISTRIBUITION", normX)

            childA_x += normX
            childA_y += normX

            print("NEW X AFTER D DIST: ", childA_x)
            print("NEW y AFTER D DIST: ", childA_y)

            childA = Individual(childA_x, childA_y)
            childs.append(childA)

        if(cross_change_B < 0.75):
            childB_x = beta * parentB.x + (1 - beta) * parentA.x
            childB_y = beta * parentB.y + (1 - beta) * parentA.y
            childB_x += np.random.normal(0, 0.2)
            childB_y += np.random.normal(0, 0.2)
            childB = Individual(childB_x, childB_y)
            childs.append(childB)

        return childs



    def generateNextGeneration(self):

        self.nxt_population.append(self.elite)

        while(len(self.nxt_population) <= self.pop_size):
            childs = self.crossPopulation()
            while(len(childs) == 0):
                childs = self.crossPopulation()

            for child in childs:
                if(child.fitness > self.best_individual.getFitness()): self.best_individual = child
                if(child.fitness > self.elite.getFitness()): self.elite = child
                self.nxt_population.append(child)

            #print(f"Got child.{i}")

    def rouletteSelection(self):
        sumChance = 0
        for ind in (self.population):
            selectedChance = random.uniform(0, 100)
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

    def steadyRun(self, status_show : bool = True):
        for i in range(self.generation_times):
            if status_show: print(f"Generation {i}")
            #self.showIndividuals(100)
            self.generateNextGeneration()
            self.population = list(self.nxt_population)
            self.nxt_population = []
            self.setPercentages()



algorithm = Algorithm()
#algorithm.showIndividuals()

algorithm.steadyRun()

algorithm.showIndividuals(50)
algorithm.showStatus()
print("X ", algorithm.best_individual.x)
print("Y ",algorithm.best_individual.y)
print("FITNESS", algorithm.best_individual.fitness)
