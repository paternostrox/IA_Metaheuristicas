import auxiliary as aux

max_size = 30
max_iter = 80

def tabu_search():
    # Importa base de dados
    df = aux.import_data_fifa(110)

    # Toma solução randômica como primeira solução
    curr_sol = aux.get_random_solution(df)

    # Cria lista Tabu
    tabu_list = [curr_sol]

    best_sol = curr_sol

    print('Starting')
    print(best_sol)
    print(aux.get_std(best_sol, df))

    for i in range(max_iter):
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

    print('DONE')
    print(best_sol)
    print(aux.get_std(best_sol, df))

tabu_search()