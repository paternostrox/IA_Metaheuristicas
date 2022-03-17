import time
import auxiliary as aux
import gradient_descent as gd
import tabu_search as ts
import grasp as gsp
import scipy.stats as stats
import statistics as st

###########################################################
# Treino para o ajuste de parâmetros de Tabu Search e GRASP
###########################################################

# Critério de parada para os algoritmos, tempo max (s)
max_time = 30

# Número de testes com cada configuração de parâmetros
test_amount = 10

# Importa base de dados
df = aux.import_data_fifa(110, 21)
# Escala base de dados
scaled_df = aux.scale_dataframe(df)

# Grade de parâmetros para Tabu Search
ts_max_iter = [30, 120, 240, 580]
ts_max_size = [20, 40, 75, 130]

ts_results = []
for i in range(len(ts_max_iter)):
    for j in range(len(ts_max_size)):
        config_stds = []
        config_times = []
        for n in range(test_amount):
            start_time = time.process_time()
            # Toma solução randômica como primeira solução
            start_sol = aux.get_random_solution(scaled_df)
            # Roda algoritmo
            final_sol = ts.tabu_search(start_sol, scaled_df, ts_max_iter[i], ts_max_size[j], max_time)

            # Adiciona valores do teste da configuração
            end_time = time.process_time()
            config_stds.append(aux.fitness(final_sol, scaled_df))
            config_times.append(end_time - start_time)

        # Adiciona médias da configuração
        std_mean = st.mean(config_stds)
        time_mean = st.mean(config_times)
        ts_results.append([std_mean, time_mean])

print('Busca Tabu:', ts_results)        

# Grade de parâmetros para GRASP
gsp_max_iter = [10, 15, 30, 50]
gsp_pool_size = [8, 16, 32, 64]

gsp_results = []
for i in range(len(gsp_max_iter)):
    for j in range(len(gsp_pool_size)):
        config_stds = []
        config_times = []
        for n in range(test_amount):
            start_time = time.process_time()

            # Roda algoritmo (soluções são construídas pelo grasp)
            final_sol = gsp.grasp(scaled_df, gsp_max_iter[i], gsp_pool_size[j], max_time)

            # Adiciona valores do teste da configuração
            end_time = time.process_time()
            config_stds.append(aux.fitness(final_sol, scaled_df))
            config_times.append(end_time - start_time)

        # Adiciona médias da configuração
        std_mean = st.mean(config_stds)
        time_mean = st.mean(config_times)
        gsp_results.append([std_mean, time_mean])

print('GRASP:', gsp_results)