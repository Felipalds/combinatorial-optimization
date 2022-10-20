from math import *
from pickle import POP_MARK
import random
from Individual import Individual
DECIMAL = 4


class Algorithm:
    current_population = []
    next_population = []
    current_population_fitness = 0

    def __init__(self, pop_size) -> None:
        self.pop_size = pop_size
        self.generateFirstPopulation()
        self.generateIndividualPercentage()

    def generateFirstPopulation(self):
        for i in range(self.pop_size):
            current_x = round(float(random.uniform(0, 0.5)), DECIMAL)
            current_y = round(float(random.uniform(0, 0.5)), DECIMAL)
            current_individual = Individual(current_x, current_y)
            self.current_population.append(current_individual)
            self.current_population_fitness += round(current_individual.fitness, DECIMAL)
        print("First generation")


    def generateIndividualPercentage(self):
        for i in range(0, self.pop_size):
            self.current_population[i].setPercentage(self.current_population[i].getFitness() * 100 / self.current_population_fitness)

    def crossingPopulation(self):
        self.generateIndividualPercentage()

        parent1 = self.rouletteSelection()
        parent2 = self.rouletteSelection()

        if(parent1 == parent2):
            return None

        if(parent1 == None or parent2 == None):
            return None

        beta = round(float(random.uniform(0, 1)), DECIMAL)
        fx = beta*parent1.x + (1-beta)*parent2.x
        fy = beta*parent1.y + (1-beta)*parent2.y

        child = Individual(fx, fy)
        return child

    def generateNextGeneration(self):
        # elitism
        for i in range(self.pop_size):
            child = self.crossingPopulation()
            while(child == None):
                child = self.crossingPopulation()

            self.next_population.append(child)
        print("Next generation generated")

    def rouletteSelection(self):
        selected = None
        while not selected:
            for i in (self.current_population):
                selectedChance = random.randrange(0, 100)
                
                if i and selectedChance < i.individual_percentage:
                    selected = i
                    return selected

    def showIndividuals(self):
        for i in range(self.pop_size):
            print(f"Elemento {i}")
            print("Elemento X", self.current_population[i].x)
            print("Elemento Y", self.current_population[i].y)
            print("Fitness: ", self.current_population[i].fitness)
            print("Percentage: ", self.current_population[i].getPercentage())

    def showStatus(self):
        print("Population size: ", self.pop_size)
        print("Total fitness: ", self.current_population_fitness)



algorithm = Algorithm(100)
#algorithm.showIndividuals()


for i in range(0, 100):
    algorithm.crossingPopulation()
    algorithm.generateNextGeneration()
    print(i, "generated")

    algorithm.current_population = []
    for i in range(0, 100):
        algorithm.current_population.append(algorithm.next_population[i])
    algorithm.next_population = []
    

algorithm.generateIndividualPercentage()
algorithm.showIndividuals()
algorithm.showStatus()
