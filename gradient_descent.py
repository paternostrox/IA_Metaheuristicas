from asyncio.windows_events import NULL

from matplotlib.pyplot import sca
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
            #print(aux.fitness(neighbor_sol, scaled_df), " || ", aux.fitness(best_sol, scaled_df))
            if aux.fitness(neighbor_sol, df) < aux.fitness(best_sol, df):
                best_sol = neighbor_sol

        if best_sol == curr_sol:
            break

        curr_sol = best_sol

    return best_sol 

# MAIN
if __name__ == "__main__":

    # Importa base de dados
    df = aux.import_data_fifa(110)
    # Escala base de dados
    scaled_df = aux.scale_dataframe(df)

    print('INICIANDO DESCIDA DE GRADIENTE')

    # Toma solução randômica como primeira solução
    start_sol = aux.get_random_solution(scaled_df)
    print('Solução Randômica Gerada')
    aux.print_DPs(start_sol, df, scaled_df)

    print('========= BUSCA LOCAL =========')
    final_sol = gradient_descent(start_sol, scaled_df)

    print('FIM')
    print('Solução Final')
    aux.print_DPs(final_sol, df, scaled_df)