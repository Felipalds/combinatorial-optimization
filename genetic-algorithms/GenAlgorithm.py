from math import *
import random
from Individual import Individual
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class GenAlgorithm:

    def __init__(self, init_population = None, pop_size : int = 50, epochs : int = 300, auto_gen : bool = True, alpha : float = 0.0005) -> None:
        # Parameters:
        # init_population -> Is the first population dealt by the algorithm, defaults to None.
        # auto_gen -> If passed as True, and no init_population value is passed, then a random population will be generated for the initial population.
        # pop_size -> Integer value that defines the size of the populations to be handled.
        # epochs -> Integer value that defines the amounts of epochs (or generations) to be calculated.
        # alpha -> Float value that defines the alpha for the mutation.
        self.alpha = alpha
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

    def definer(self, value, M, m):
        if value > M:
            return M
        elif value < m:
            return M
        else:
            return value

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

        if(cross_change_A < 0.75):
            childA_x = beta * parentA.x + (1 - beta) * parentB.x
            childA_x = self.definer(childA_x, 0.5, 0)
            childA_y = beta * parentA.y + (1 - beta) * parentB.y
            childA_y = self.definer(childA_y, 0.5, 0)
            normX = np.random.normal(0, self.alpha)

            childA_x += normX
            childA_x = self.definer(childA_x, 0.5, 0)
            childA_y += normX
            childA_y = self.definer(childA_y, 0.5, 0)

            childA = Individual(childA_x, childA_y)
            childs.append(childA)

        if(cross_change_B < 0.75):
            childB_x = beta * parentB.x + (1 - beta) * parentA.x
            childB_x = self.definer(childB_x, 0.5, 0)
            childB_y = beta * parentB.y + (1 - beta) * parentA.y
            childB_y = self.definer(childB_y, 0.5, 0)
            normX = np.random.normal(0, self.alpha)

            childB_x += normX
            childB_x = self.definer(childB_x, 0.5, 0)
            childB_y += normX
            childB_y = self.definer(childB_y, 0.5, 0)

            childB = Individual(childB_x, childB_y)
            childs.append(childB)

        return childs



    def generateNextGeneration(self):

        self.nxt_population.append(self.elite)

        while(len(self.nxt_population) != self.pop_size):
            childs = self.crossPopulation()
            for child in childs:
                if(child.getFitness() > self.best_individual.getFitness()): self.best_individual = child
                if(child.getFitness() > self.elite.getFitness()): self.elite = child
                if len(self.nxt_population) < self.pop_size:
                    self.nxt_population.append(child)

    def rouletteSelection(self):
        self.setPercentages()
        sumChance = 0
        for ind in self.population:
            selectedChance = random.uniform(0, 100)
            sumChance += ind.getPercentage()
            if ind and selectedChance < sumChance:
                return ind
        print("Got None")
        return None

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

    def steadyRun(self, status_show : bool = True):
        for i in range(self.generation_times):
            print(f"Generation {i}")
            if status_show: self.showIndividuals(self.pop_size)
            self.generateNextGeneration()
            self.population = list(self.nxt_population)
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

