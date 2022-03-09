import auxiliary as aux

max_size = 30
max_iter = 80

def tabu_search():
    # Importa base de dados
    df = aux.import_data_fifa(110)
    scaled_df = aux.scale_dataframe(df)

    # Toma solução randômica como primeira solução
    curr_sol = aux.get_random_solution(scaled_df)

    # Cria lista Tabu
    tabu_list = [curr_sol]

    best_sol = curr_sol

    print('INICIANDO BUSCA TABU')
    print('Solução Randômica Gerada')
    aux.print_DPs(curr_sol, df, scaled_df)

    print('######### BUSCA LOCAL #########')
    for i in range(max_iter):
        neighborhood = aux.get_neighborhood(curr_sol)

        # Caso ache uma solução melhor, seleciona ela
        # Caso contrário, usa primeiro vizinho
        curr_sol = neighborhood[0]
        for neighbor_sol in neighborhood:
            if (not tabu_list.__contains__(neighbor_sol)) and aux.fitness(neighbor_sol, scaled_df) < aux.fitness(curr_sol, scaled_df):
                curr_sol = neighbor_sol

        # Atualizar melhor solução encontrada até então, se necessário
        if aux.fitness(curr_sol, scaled_df) < aux.fitness(best_sol, scaled_df):
            best_sol = curr_sol

        # Insere solução na lista Tabu
        tabu_list.append(curr_sol)
        if(len(tabu_list) > max_size):
            tabu_list.pop(0)    

    print('FIM')
    print('Solução Final')
    aux.print_DPs(best_sol, df, scaled_df)

tabu_search()