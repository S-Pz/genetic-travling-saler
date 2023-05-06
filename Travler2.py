from random import randint, shuffle

# numero de cidades e populações
n_cid = 300
n_pop = n_cid * 20

# grafo de ligações entre cidades
def criar_grafo(n): 
    grafo = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                grafo[i][j] = 0
            else:
                dist = randint(0, 100)
                grafo[i][j] = dist 
                grafo[j][i] = dist
    return grafo

# aleatorização de caminhos
def criar_populacao(n_cid, n_pop):
    matriz_pop = [[j for j in range(n_cid)] for _ in range(n_pop)]
    for i in range(n_pop):
        shuffle(matriz_pop[i])
    return matriz_pop

# cálculo de melhor cidade
def avaliacao(n_cid, n_pop, populacao, grafo):
    notas = []
    for i in range(n_pop):
        distancia = 0
        for j in range(n_cid-1):
            cid_a = populacao[i][j]
            cid_b = populacao[i][j+1]
            distancia += grafo[cid_a][cid_b] 
        #tupla indice, nota
        notas.append(distancia)
    return notas

# funções de torneio
def torneio(populacao, notas, n_pop):
    n_pais = 4
    pais = []
    for _ in range(n_pop):
        selecionados = []
        for _ in range(n_pais):
            aleatorio = randint(0, len(notas) - 1)
            selecionados.append(notas[aleatorio])
        selecionados.sort()
        #pai com nota igual a selecionados[0]
        pais.append(populacao[notas.index(selecionados[0])])
    return pais 

# função de cruzamento
def order_crossover(n_pop, pais, n_cid):
    # selecionando pais
    filhos = []
    p_tercil = int(n_cid/3)
    t_tercil = int((2 * n_cid)/3) - 1
    
    taxa_crossover = int(0.8 * n_pop)

    for i in range(int(taxa_crossover / 2)):
        # seleção de pais
        pai1 = pais[2 * i]
        pai2 = pais[2 * i + 1]

        # fatiamento entre pais
        fatiap1 = pai1[p_tercil:t_tercil+1]
        fatiap2 = pai2[p_tercil:t_tercil+1]
        
        filho1 = [cidade for cidade in pai1 if cidade not in fatiap2]
        filhos.append(fatiap2 + filho1)
        filho2 = [cidade for cidade in pai2 if cidade not in fatiap1]
        filhos.append(fatiap1 + filho2)
    
    for j in range(taxa_crossover, n_pop):
        filhos.append(pais[j])
    return filhos

if __name__ == "__main__":
    grafo     = criar_grafo(n_cid)
    populacao = criar_populacao(n_cid, n_pop)
    for gen in range(2000):
        fitness_pop = avaliacao(n_cid, n_pop, populacao, grafo)
        copia = fitness_pop.copy()
        copia.sort()
        print(f"Geração {gen}:\t{copia[0]}")
        ganhadores  = torneio(populacao, fitness_pop, n_pop)
        cruzados    = order_crossover(n_pop, ganhadores, n_cid)
        populacao   = cruzados

        #https://jaketae.github.io/study/genetic-algorithm/
        #https://www.inf.tu-dresden.de/content/institutes/ki/cl/study/summer14/pssai/slides/GA_for_TSP.pdf
        #https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35