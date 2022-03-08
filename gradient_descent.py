from asyncio.windows_events import NULL
import auxiliary as aux

def gradient_descent():
    # Importa base de dados
    df = aux.import_data_fifa(110)

    # Toma solução randômica como primeira solução
    curr_sol = aux.get_random_solution(df)

    print('STARTING')
    print(curr_sol)
    print(aux.get_means(curr_sol, df))
    print(aux.get_means_scaled(curr_sol, df))
    print(aux.get_std(curr_sol, df))
    print(aux.get_std_scaled(curr_sol, df))

    while(True):
        curr_std = aux.get_std(curr_sol, df)

        best_sol = curr_sol

        neighborhood = aux.get_neighborhood(curr_sol)
        for neighbor_sol in neighborhood:
            #print(aux.fitness(neighbor_sol, df), " || ", aux.fitness(best_sol, df))
            if aux.fitness(neighbor_sol, df) < aux.fitness(best_sol, df):
                best_sol = neighbor_sol

        if best_sol == curr_sol:
            break

        curr_sol = best_sol    

    print('DONE')
    print(curr_sol)
    print(aux.get_means(curr_sol, df))
    print(aux.get_means_scaled(curr_sol, df))
    print(aux.get_std(curr_sol, df))
    print(aux.get_std_scaled(curr_sol, df))

gradient_descent()