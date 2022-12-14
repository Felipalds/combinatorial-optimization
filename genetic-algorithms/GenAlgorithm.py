from math import *
import random
from Individual import Individual
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class GenAlgorithm:

    def __init__(self, init_population = None, pop_size : int = 50, epochs : int = 300, auto_gen : bool = True) -> None:
        # Parameters:
        # init_population -> Is the first population dealt by the algorithm, defaults to None.
        # auto_gen -> If passed as True, and no init_population value is passed, then a random population will be generated for the initial population.
        # pop_size -> Integer value that defines the size of the populations to be handled.
        # epochs -> Integer value that defines the amounts of epochs (or generations) to be calculated.
        # alpha -> Float value that defines the alpha for the mutation.
        self.alpha = 0.0005
        self.generations = []
        self.pop_size = pop_size
        self.generation_times = epochs

        self.population = init_population
        self.nxt_population = []
        self.fitsum = 0
        self.best_individual = Individual(0.0001, 0.0001)
        self.elite = Individual(0.0001, 0.0001)

        # Defines an empty population in case of null value given
        if not init_population:
            self.population = []
        else:
            self.generations.append(init_population)
        # Generates the initial population in case of a given null value, and selected auto_gen.
        if auto_gen and len(self.population) == 0:
            self.generatePopulation()
            self.generations.append(self.population)
        if (len(self.population) > 0):
            self.population = np.array(self.population)

        

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
        self.population = np.array(self.population)
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

        if(cross_change_A <= 0.75):
            childA = Individual(0.2, 0.2)
            childA.cross(parentA, parentB, beta)
            childA.mutate(self.alpha)
            childs.append(childA)

            childB = Individual(0.2, 0.2)
            childB.cross(parentA, parentB, beta)
            childB.mutate(self.alpha)
            childs.append(childB)
        else:
            parentA.mutate(self.alpha)
            parentB.mutate(self.alpha)
            childs.append(parentA)
            childs.append(parentB)

        return childs

    def generateNextGeneration(self):
        self.elite = self.population[0]
        for ind in self.population:
            if ind.getFitness() > self.elite.getFitness():
                self.elite = ind
        self.nxt_population.append(self.elite)
        for i in range(self.pop_size-1):
            for child in self.crossPopulation():
                if (child.getFitness() > self.best_individual.getFitness()): self.best_individual = child
                self.nxt_population.append(child)
        while len(self.nxt_population) > self.pop_size:
            self.nxt_population.pop()

    def rouletteSelection(self):
        self.setPercentages()
        sumChance = 0
        for ind in self.population[:self.pop_size]:
            selectedChance = random.uniform(0, 100)
            sumChance += ind.getPercentage()
            if selectedChance <= sumChance:
                print(len(self.population))
                return ind

    def showIndividuals(self, amount : int = None):
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

    def steadyRun(self):
        for i in range(self.generation_times):
            print(f"Generation {i}")
            self.generateNextGeneration()
            self.population = np.array(self.nxt_population)
            self.generations.append(self.population)
            self.nxt_population = []
            self.setPercentages()
    
    def visualize(self, n_gen : int):
        x = [ind.x for ind in self.generations[n_gen]]
        y = [ind.y for ind in self.generations[n_gen]]
        plt.xlim([0, 0.5])
        plt.ylim([0, 0.5])
        plt.scatter(x, y)
        plt.show()
    
    def animate(self, interval : int = 200):
        gens = self.generations
        fig = plt.figure(1)
        ax = plt.axes(xlim=[0, 0.5], ylim=[0, 0.5])

        x = [ind.x for ind in gens[0]]
        y = [ind.y for ind in gens[0]]
        scatter = ax.scatter(x, y)

        def update(i):
            xy = [[ind.x, ind.y] for ind in gens[i]]

            scatter.set_offsets(xy)
            fig.suptitle("Generation: "+str(i))

            return scatter,
        
        anim = FuncAnimation(fig, update, frames=len(gens)-1, interval=interval)
        plt.show()

