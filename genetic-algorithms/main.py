from math import *
import random
import Individual

DECIMAL = 4

class Algorithm:
    current_population = []
    next_population = []
    current_population_fitness = 0

    def __init__(self, pop_size) -> None:
        self.pop_size = pop_size

    def generateFirstPopulation(self):
        for i in range(self.pop_size):
            current_x = round(float(random.uniform(0, 0.5)), DECIMAL)
            current_y = round(float(random.uniform(0, 0.5)), DECIMAL)
            current_individual = Individual(current_x, current_y)
            self.current_population.append(current_individual)
            self.current_population_fitness += current_individual.fitness

    def generateIndividualPercentage(self):
        for i in range(self.pop_size):
            individual = self.current_population[i]
            individual.setPercentage(individual.getFitness() * 100 / self.current_population_fitness)

    def crossingPopulation(self):
        parent1 = self.rouletteSelection()
        parent2 = self.rouletteSelection()

    def rouletteSelection(self):
        selected = None
        while not selected:
            for i in self.current_population:
                selectedChance = random.randrange(0, 101)
                if selectedChance < i.getPercentage():
                    selected = i
                    break

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

    def testPercentage(self):
        x = 0
        for i in range(self.pop_size):
            x += self.current_population[i].getPercentage()
        print("Percentage somado:", x)


algorithm = Algorithm(100)
algorithm.generateFirstPopulation()
algorithm.generateIndividualPercentage()

algorithm.showIndividuals()
algorithm.showStatus()

algorithm.testPercentage()