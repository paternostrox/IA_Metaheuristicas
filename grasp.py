import copy
import random
import time
import auxiliary as aux
import gradient_descent as gd

def sort_func(c):
    return c[0]
            
def grasp(df, max_iter, pool_size, max_time):

    start_time = time.process_time()

    # Manter melhor solução
    best_sol = []

    # Roda iterações de GRASP
    iter = 0
    while iter < max_iter and (time.process_time() - start_time) < max_time:
        iter += 1
        # FASE CONSTRUTIVA
        # Constrói solução de forma gulosa
        curr_sol = aux.get_random_greedy_solution(df, pool_size)


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
    start_time = time.process_time()
    final_sol = grasp(scaled_df, 1, 1, 30)
    print('TEMPO:', time.process_time() - start_time)
    aux.print_DPs(final_sol, df, scaled_df)