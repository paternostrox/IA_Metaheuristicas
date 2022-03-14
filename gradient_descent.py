from asyncio.windows_events import NULL
import auxiliary as aux

def gradient_descent(start_sol, df):

    curr_sol = start_sol

    # Busca Local
    # Caso existam vizinhos melhores que a solução corrente, substui-se a corrente
    # Isso ocorre até que nenhum vizinho seja melhor que a solução corrente
    while(True):
        best_sol = curr_sol

        neighborhood = aux.get_neighborhood(curr_sol)
        for neighbor_sol in neighborhood:
            if aux.fitness(neighbor_sol, df) < aux.fitness(best_sol, df):
                best_sol = neighbor_sol

        if best_sol == curr_sol:
            break

        curr_sol = best_sol

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
    final_sol = gradient_descent(start_sol, scaled_df)
    aux.print_DPs(final_sol, df, scaled_df)