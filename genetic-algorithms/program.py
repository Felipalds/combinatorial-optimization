from genalg import Algorithm
from matplotlib import pyplot as plt
answer = None

while answer != 'p':
    alg = Algorithm(pop_size=int(input("Tamanho da população: ")), epochs=int(input("Gerações: ")))
    alg.steadyRun(False)
    alg.showStatus()
    # alg.showIndividuals()
    print("Melhor indivíduo:", alg.best_individual.x, alg.best_individual.y)

    while answer == 'c' or answer != 'p':

        answer = input("Continuar? (p:parar, c:continuar, v:visualizar, m:melhor)\n")

        if answer == 'v':
            chosenGen = int(input("Escolha uma geração:\n"))
            x = [ind.x for ind in  alg.generations[chosenGen-1]]
            y = [ind.y for ind in alg.generations[chosenGen-1]]
            plt.xlim([0, 0.5])
            plt.ylim([0, 0.5])
            plt.scatter(x, y)
            plt.show()
        elif answer == 'm':
            print("Melhor indivíduo:", alg.best_individual.x, alg.best_individual.y)

