import copy
from multiprocessing import pool
import random
from tokenize import group
import auxiliary as aux

pool_size = 100
rcl_size = 10

def sort_func(c):
    return c[0]

# Função de construção gulosa
def get_random_greedy_solution(df):
    indexes = df.index.values.tolist()
    team_amount = len(df.index)//11
    groups = [[] for i in range(team_amount)]

    while(len(indexes) > 0):

        candidates = []

        for i in range(pool_size):
            idx = copy.copy(indexes)
            candidate = copy.deepcopy(groups)

            # Atribui um jogador (dos que restam) randômicamente a cada time
            for j in range(team_amount):
                rnd = random.randrange(0,len(idx))
                candidate[j].append(idx[rnd])
                idx.pop(rnd)

            candidates.append([aux.fitness(candidate, df), candidate])

        candidates.sort(key=sort_func)

        # restricted candidate list (RCL)
        best_candidates = candidates[0:rcl_size]
        rnd = random.randrange(0,rcl_size)
        groups = best_candidates[rnd][1]
        
        for v in best_candidates[rnd][1]:
            indexes.pop(v)

        print(aux.fitness(groups))

# Função de construção gulosa
def get_random_greedy_solution_fast(df):
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
        print(aux.fitness(teams, df))

            
def grasp():
    # Importa base de dados
    df = aux.import_data_fifa(110)

    sol = get_random_greedy_solution_fast(df)

    print(aux.fitness(sol, df))

grasp()