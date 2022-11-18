from GenAlgorithm import GenAlgorithm as Algorithm

answer = 'run'

while answer != 'stop':
    pop_size = int(input("Tamanho da População: \n"))
    epochs = int(input("Gerações: \n"))
    alpha = input("Alpha (enter for default):\n")

    if alpha == '':
        alpha = 0.05
    else:
        alpha = float(alpha)


    alg = Algorithm(pop_size, epochs, alpha)
    alg.steadyRun() # main function
    alg.showStatus()

    # alg.showIndividuals()
    print("Melhor indivíduo:", alg.best_individual.x, alg.best_individual.y)

    while answer != 'c' and answer != 'p':

        answer = input("Continuar? (p:parar, c:continuar, v:visualizar, a:animação, m:melhor)\n")

        if answer == 'v':
            chosenGen = int(input("Escolha uma geração:\n"))
            try:
                alg.visualize(chosenGen-1)
            except IndexError:
                print("Geração '"+str(chosenGen)+"' não existe (fora de alcançe).")
        elif answer == 'a':
            vel = int(input("Velocidade (ms):\n"))
            alg.animate(vel)
        elif answer == 'm':
            print("Melhor indivíduo:", alg.best_individual.x, alg.best_individual.y)
            
    if answer == 'c':
        answer = None

