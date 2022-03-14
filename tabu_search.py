import time
import auxiliary as aux

def tabu_search(start_sol, df, max_iter, max_size, max_time):

    start_time = time.process_time()

    curr_sol = start_sol

    # Cria lista Tabu
    tabu_list = [curr_sol]

    # Guarda melhor solução
    best_sol = curr_sol
    iter = 0
    while iter < max_iter and (time.process_time() - start_time) < max_time:
        iter += 1
        neighborhood = aux.get_neighborhood(curr_sol)

        # Caso ache uma solução melhor, seleciona ela
        # Caso contrário, usa primeiro vizinho
        curr_sol = neighborhood[0]
        for neighbor_sol in neighborhood:
            if (not tabu_list.__contains__(neighbor_sol)) and aux.fitness(neighbor_sol, df) < aux.fitness(curr_sol, df):
                curr_sol = neighbor_sol

        # Atualizar melhor solução encontrada até então, se necessário
        if aux.fitness(curr_sol, df) < aux.fitness(best_sol, df):
            best_sol = curr_sol

        # Insere solução na lista Tabu
        tabu_list.append(curr_sol)
        if(len(tabu_list) > max_size):
            tabu_list.pop(0)

    return best_sol 

# MAIN
if __name__ == "__main__":

    # Importa base de dados
    df = aux.import_data_fifa(110, 42)
    # Escala base de dados
    scaled_df = aux.scale_dataframe(df)

    # Toma solução randômica como primeira solução
    start_sol = aux.get_random_solution(scaled_df)

    # Roda algoritmo
    final_sol = tabu_search(start_sol, scaled_df, 30, 80, 60)
    aux.print_DPs(final_sol, df, scaled_df)