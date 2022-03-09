import copy
from multiprocessing import pool
import random
from tokenize import group
import auxiliary as aux
import gradient_descent as gd

pool_size = 30

max_iter = 10

def sort_func(c):
    return c[0]

# Função de construção gulosa
def get_random_greedy_solution(df):
    indexes = df.index.values.tolist()
    team_amount = len(df.index)//aux.team_size
    teams = [[] for i in range(team_amount)]

    for n in range(aux.team_size):

        best = []

        for i in range(pool_size):
            idx = copy.copy(indexes)
            candidate = copy.deepcopy(teams)

            # Atribui um jogador (dos que restam) randômicamente a cada time
            for j in range(team_amount):
                rnd = random.randrange(0,len(idx))
                candidate[j].append(idx[rnd])
                idx.pop(rnd)

            if(aux.fitness(candidate, df) < aux.fitness(best, df)):
                best = candidate

        teams = best
        for team in teams:
            indexes.remove(team[n])

    return teams

            
def grasp():
    # Importa base de dados
    df = aux.import_data_fifa(110)
    scaled_df = aux.scale_dataframe(df)

    best_sol = []

    print('INICIANDO GRASP')

    for i in range(max_iter):
        
        # FASE CONSTRUTIVA
        curr_sol = get_random_greedy_solution(scaled_df)
        print('Solução Construída por Função Gulosa')

        # INTENSIFICAÇÃO (BUSCA LOCAL)
        print('######### BUSCA LOCAL #########')
        curr_sol = gd.gradient_descent(curr_sol, scaled_df)
        
        # Caso seja melhor que a melhor encontrada até então, a substitui
        if(aux.fitness(curr_sol, scaled_df) < aux.fitness(best_sol, scaled_df)):
            best_sol = curr_sol
            print('Nova Melhor Solução Encontrada')
            aux.print_DPs(best_sol, df, scaled_df)
    
    print('FIM')
    print('Solução Final')
    aux.print_DPs(best_sol, df, scaled_df)

grasp()