import random
import copy
import matplotlib.pyplot as plt
import time

# Grava o tempo inicial ###############################################################################
inicio = time.time()


# Inicializacao ###############################################################################

n_linhas = 8
n_pop = 6
taxa_mutacao = 0.001
num_ite = 1000
pop = []
tabuleiro = []
mutacao = []
fitness_pop = []
fitness_mut = []
fitness_cross = []
# valor_pop = []
filho1 = []
filho2 = []
filhos = []
pais = []
melhor_geracao = []
melhor_iteracao = 0
melhor_fitness = []
# melhor_valor = []
count_patamar = 0
num_patamar = 10
ite = 0
graf = {"Valor": [], "Fitness": []}


# Funções ###############################################################################

def selecao_roleta(pop, fitness):
    soma_fitness = sum(fitness)
    probabilidade = []
    cumulativa = 0
    list_cumulativa = []
    list_cumulativa.clear()
    for i in fitness:
        probabilidade.append(i/soma_fitness)
        cumulativa = cumulativa + i/soma_fitness
        list_cumulativa.append(cumulativa)
    # print(probabilidade)
    # print(list_cumulativa)

    r = random.random()
    for i, p in enumerate(list_cumulativa):
        if r < p:
            # print(i, p)
            return pop[i]
        
        
def selecao_duelo(pop, fitness):
    k = 0.8
    tab_cand = random.sample(range(len(pop)), 2)
    r = random.random()
    if(r<k):
        if(fitness[tab_cand[0]]>fitness[tab_cand[1]]):
            return pop[tab_cand[0]]
        else:
            return pop[tab_cand[1]]
    else:
        if(fitness[tab_cand[0]]>fitness[tab_cand[1]]):
            return pop[tab_cand[1]]
        else:
            return pop[tab_cand[0]]
        

def fitness_function(fit):
    pontos = 100
    for i in range(len(fit)):
        for j in range(i+1,len(fit)):
            # Testando linhas
            if fit[i] == fit[j]:
                pontos -= 1
            # Testando diagonais
            if abs(i-j) == abs(fit[i]-fit[j]):
                pontos -= 1
    return pontos


# Populacao inicial ###############################################################################

for i in range(n_pop):
    tabuleiro.clear()
    tabuleiro = []
    for i in range(n_linhas):
        pos_linha = random.randint(1, 8)
        tabuleiro.append(pos_linha)
    pop.append(tabuleiro.copy())
    
    # print(tabuleiro)


while True:

    # Fitness População ###############################################################################

    fitness_pop.clear()  # Limpa a lista de fitness antes de calcular novamente

    for tab in pop:
        fitness_pop.append(fitness_function(tab))
    # print(fitness_pop)
    # print("Fitness População: ", sum(fitness_pop))


    # Seleção natural ###############################################################################

    num_pais = round(len(pop)/2)
    pais.clear()
    for i in range(num_pais):
        # pai = selecao_roleta(pop, fitness_pop)
        pai = selecao_duelo(pop, fitness_pop)
        pais.append(pai)
        # print(pai)


    # Cross Over ###############################################################################

    filhos.clear()
    for i in range(num_pais):
        # for j in range(i+1,num_pais,2): ############################################################################### retirar exponencial de filhos
        # secao = random.randint(1,n_linhas-1)
        filho1.clear()
        filho2.clear()
        for k in range(n_linhas):
            if(k<2 or k>5):                # cross em dois pontos
                filho1.append(pais[num_pais-(num_pais-i)][k])
                filho2.append(pais[num_pais-(num_pais-i+1)][k])
            else:
                filho1.append(pais[num_pais-(num_pais-i+1)][k])
                filho2.append(pais[num_pais-(num_pais-i)][k])
        filhos.append(filho1)  
        filhos.append(filho2)
    # print("len filhos",len(filhos))


    # Fitness Cross Over ###############################################################################

    fitness_cross.clear()
    for tab in filhos:
        fitness_cross.append(fitness_function(tab))
    # print(fitness_cross)
    # print("Fitness Cross Over: ", sum(fitness_cross))


    # Mutacao ###############################################################################

    mutacao.clear()

    for i in filhos:
        r = random.random()
        filho = copy.deepcopy(i)
        if r <= taxa_mutacao:
            indice = random.randint(0, n_linhas-1)
            filho[indice] = random.randint(1, n_linhas)
        mutacao.append(filho)

        
    # Fitness Mutacao ###############################################################################

    fitness_mut.clear()

    for tab in mutacao:
        fitness_mut.append(fitness_function(tab))
    # print(fitness_mut)
    # print("Fitness Mutacao: ", sum(fitness_mut))


    # Nova Populacao ###############################################################################

    pop.clear()
    pop.extend(mutacao)  # Adiciona todos os elementos de mutacao a pop
    # print("nova pop")
    # for i in pop:
    #     print(i)
        

    graf["Fitness"].append(sum(fitness_mut))


    # Melhor Geração ###############################################################################

    if sum(fitness_mut) > sum(melhor_fitness):
        melhor_iteracao = ite
        melhor_geracao.clear()
        melhor_geracao.extend(pop)
        melhor_fitness.clear()
        melhor_fitness.extend(fitness_mut)


    # Criterio de Parada ###############################################################################

    # if ((sum(valor_pop) <= (mem_valor)*1.01) and (sum(valor_pop) >= (mem_valor)*0.99)):
    #     count_patamar += 1
    # else:
    #     mem_valor = sum(valor_pop)

    if ((ite >= num_ite)):
    #if ((count_patamar>num_patamar) or (ite >= num_ite)):
        #print(count_patamar)
        count_patamar = 0
        #print(ite)
        ite = 0
        break
    ite += 1


# Melhor geracao ###############################################################################
print("Melhor Geração:", melhor_iteracao)
print("Valor Fitness:", sum(melhor_fitness))


for i in range(len(melhor_geracao)):
    print("Tabuleiro:", i+1, "/ Fitness", melhor_fitness[i], "/ Querer")
    # print([melhor_geracao[i][j] for j in range(n_linhas)])

# Grava o tempo final
fim = time.time()

# Calcula o tempo total decorrido
tempo_total = fim - inicio

print(f"Tempo de execução: {round(tempo_total,3)} segundos")


# Plotando o gráfico ###############################################################################
plt.plot(graf["Fitness"])  # 'o' para marcar os pontos
plt.title("Gráfico de Fitness")  # Título do gráfico
plt.xlabel("Geracao")  # Rótulo do eixo X
plt.ylabel("Fitness")  # Rótulo do eixo Y
plt.grid(True)  # Exibir grade
plt.show()  # Exibir o gráfico