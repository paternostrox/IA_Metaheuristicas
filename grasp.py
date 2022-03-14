import copy
import random
import time
import auxiliary as aux
import gradient_descent as gd

def sort_func(c):
    return c[0]

# Função de construção gulosa
def get_random_greedy_solution(df, pool_size):
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

            
def grasp(df, max_iter, pool_size, max_time):

    start_time = time.process_time()

    # Manter melhor solução
    best_sol = []

    # Roda iterações de GRASP
    iter = 0
    while iter < max_iter and (time.process_time() - start_time) < max_time:
        
        # FASE CONSTRUTIVA
        # Constrói solução de forma gulosa
        curr_sol = get_random_greedy_solution(df, pool_size)

        # INTENSIFICAÇÃO (BUSCA LOCAL)
        curr_sol = gd.gradient_descent(curr_sol, df)
        
        # Caso seja melhor que a melhor encontrada até então, a substitui
        if(aux.fitness(curr_sol, df) < aux.fitness(best_sol, df)):
            best_sol = curr_sol

    return best_sol

# MAIN
if __name__ == "__main__":

    # Importa base de dados
    df = aux.import_data_fifa(110, 42)
    # Escala base de dados
    scaled_df = aux.scale_dataframe(df)

    # Roda algoritmo
    final_sol = grasp(scaled_df, 20, 8)
    aux.print_DPs(final_sol, df, scaled_df)