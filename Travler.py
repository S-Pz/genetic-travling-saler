from random import randint, shuffle

n_cid = 100
n_pop = 500

# ////////////////////////////////////////////////////////////////////////////////

# grafo de ligações entre cidades
def criar_grafo(n): 
    grafo = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                grafo[i][j] = 0
            else:
                dist = randint(0, 200)
                grafo[i][j] = dist 
                grafo[j][i] = dist
    return grafo

def printGrafo(grafo):
    for j in range (n_cid):
        print("     ",j, end='\t')
    print()
    print()
    
    for i in range(n_cid):
        print(i, end='\t')
        for j in range(n_cid):
            print(grafo[i][j], end='\t')
        print()
    print()

# ////////////////////////////////////////////////////////////////////////////////

def criar_populacao():
    matriz_pop = [[j for j in range(n_cid)] for _ in range(n_pop)]
    for i in range(n_pop):
        shuffle(matriz_pop[i])
    return matriz_pop

def printPopulacao(populacao):
    for i in range(n_pop):
        print(populacao[i])
    print()

# ////////////////////////////////////////////////////////////////////////////////

def avaliacao(populacao, grafo):
    notas = []
    for i in range(n_pop):
        distancia = 0
        for j in range(n_cid-1):
            cid_a = populacao[i][j]
            cid_b = populacao[i][j+1]
            distancia += grafo[cid_a][cid_b] 
        notas.append(distancia)
    return notas

def printAvaliacao(fit):
    for i in range(n_pop):
        print(fit[i])
    print()

# ////////////////////////////////////////////////////////////////////////////////

def printFitPop(populacao, fit):
    for i in range(n_pop):
        print(populacao[i], fit[i])
    print()

# ////////////////////////////////////////////////////////////////////////////////

def torneio(notas):
    n_pais = 5
    pais = []
    for i in range(n_pop):
        selecionados = []
        for j in range(n_pais):
            aleatorio = randint(0, n_pop - 1)
            selecionados.append(notas[aleatorio])
        selecionados.sort()
        pais.append(selecionados[0])
    return pais 

def printPai(pais):
    print(pais)

# ////////////////////////////////////////////////////////////////////////////////

def indice_pais(pais, notas):
    indices = []
    for i in range(n_pop):
        if pais[i] in notas:
            indices.append(notas.index(pais[i]))
    return indices

def printIndices(indices):
    print(indices)

# ////////////////////////////////////////////////////////////////////////////////

def crossover(populacao, indice):
    newpop = []

    j = n_pop
    for i in range(int(n_pop/2)):
        child1 = []
        child2 = []
        childP1 = []
        childP2 = []
        parent1 = []
        parent2 = []
        j -= 1
        parent1 = populacao[indice[i]]
        parent2 = populacao[indice[j]]

        geneA = randint(0, n_cid)
        geneB = randint(0, n_cid)

        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        for x in range(startGene, endGene):
            childP1.append(parent1[x])
            childP2.append(parent2[x])
            

        newchildP1 = [item for item in parent2 if item not in childP1]
        newchildP2 = [item for item in parent1 if item not in childP2]
        child1 = childP1 + newchildP1
        child2 = childP2 + newchildP2
        
        newpop.append(child1)
        newpop.append(child2)

    return newpop

def printFilhos(filhos):
    for i in range(n_pop):
        print(filhos[i])

def printParents(populacao, indice): 
    for i in range(n_pop):
        print(populacao[indice[i]])
    print()

# ////////////////////////////////////////////////////////////////////////////////

def melhorFit(fit, i):
    copia_fit = fit.copy()
    copia_fit.sort()
    print(f"Menor distância da geração {i}: {copia_fit[0]}")

# ////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    grafo = criar_grafo(n_cid)
    populacao = criar_populacao()
    for i in range(50):
        fit = avaliacao(populacao, grafo)
        melhorFit(fit, i)
        pais = torneio(fit)
        indices = indice_pais(pais, fit)
        filhos = crossover(populacao, indices)
        populacao = filhos