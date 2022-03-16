import time
import auxiliary as aux
import gradient_descent as gd
import tabu_search as ts
import grasp as gsp
import scipy.stats as st
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as stats

# Importa base de dados
df = aux.import_data_fifa(110, 42)
# Escala base de dados
scaled_df = aux.scale_dataframe(df)

test_amount = 30

# Gera soluções randômicas
rnd_sols = []
rnd_time = []
for i in range(test_amount):
    start_time = time.process_time()
    sol = aux.get_random_solution(scaled_df)
    rnd_time.append(time.process_time() - start_time)
    rnd_sols.append(sol)

# Gera soluções gulosas
gdy_sols = []
gdy_time = []
for i in range(test_amount):
    start_time = time.process_time()
    sol = aux.get_random_greedy_solution(scaled_df, 16)
    gdy_time.append(time.process_time() - start_time)
    gdy_sols.append(sol)

# Roda gradient descent
gd_sols = []
gd_time = []
for i in range(test_amount):
    start_time = time.process_time()
    # Toma solução randômica como primeira solução
    start_sol = aux.get_random_solution(scaled_df)
    # Roda algoritmo
    final_sol = gd.gradient_descent(start_sol, scaled_df)
    gd_time.append(time.process_time() - start_time)
    gd_sols.append(final_sol)

# Roda tabu search
ts_sols = []
ts_time = []
for i in range(test_amount):
    start_time = time.process_time()
    # Toma solução randômica como primeira solução
    start_sol = aux.get_random_solution(scaled_df)
    # Roda algoritmo
    final_sol = ts.tabu_search(start_sol, scaled_df, 580, 30, 30)
    ts_time.append(time.process_time() - start_time)
    ts_sols.append(final_sol)

# Roda grasp
gsp_sols = []
gsp_time = []
for i in range(test_amount):
    start_time = time.process_time()
    # Roda algoritmo (soluções são construídas pelo grasp)
    final_sol = gsp.grasp(scaled_df, 30, 16, 30)
    gsp_time.append(time.process_time() - start_time)
    gsp_sols.append(final_sol)

# DP de atributos separados
rnd_results_sep = []
gdy_results_sep = []
gd_results_sep = []
ts_results_sep = []
gsp_results_sep = []

# DP FITNESS (média dos atributos)
rnd_results = []
gdy_results = []
gd_results = []
ts_results = []
gsp_results = []

# Calcula Desvios Padrões
for i  in range(test_amount):
    rnd_results_sep.append(aux.fitness_sep(rnd_sols[i], scaled_df))
    gdy_results_sep.append(aux.fitness_sep(gdy_sols[i], scaled_df))
    gd_results_sep.append(aux.fitness_sep(gd_sols[i], scaled_df))
    ts_results_sep.append(aux.fitness_sep(ts_sols[i], scaled_df))
    gsp_results_sep.append(aux.fitness_sep(gsp_sols[i], scaled_df))

    rnd_results.append(aux.fitness(rnd_sols[i], scaled_df))
    gdy_results.append(aux.fitness(gdy_sols[i], scaled_df))
    gd_results.append(aux.fitness(gd_sols[i], scaled_df))
    ts_results.append(aux.fitness(ts_sols[i], scaled_df))
    gsp_results.append(aux.fitness(gsp_sols[i], scaled_df))

# Imprime resultados
print('Medias Sol. Randômica |', 'Age:', stats.mean([aov[0] for aov in rnd_results_sep]), 'Overall:', stats.mean([aov[1] for aov in rnd_results_sep]), 
'Value:', stats.mean([aov[2] for aov in rnd_results_sep]), 'Fitness', stats.mean(rnd_results), 'Time', stats.mean(rnd_time))

print('Medias Sol. Gulosa |', 'Age:', stats.mean([aov[0] for aov in gdy_results_sep]), 'Overall:', stats.mean([aov[1] for aov in gdy_results_sep]), 
'Value:', stats.mean([aov[2] for aov in gdy_results_sep]), 'Fitness', stats.mean(gdy_results), 'Time', stats.mean(gdy_time))

print('Medias Gradiente de Descida |', 'Age:', stats.mean([aov[0] for aov in gd_results_sep]), 'Overall:', stats.mean([aov[1] for aov in gd_results_sep]), 
'Value:', stats.mean([aov[2] for aov in gd_results_sep]), 'Fitness', stats.mean(gd_results), 'Time', stats.mean(gd_time))

print('Medias Busca Tabu |', 'Age:', stats.mean([aov[0] for aov in ts_results_sep]), 'Overall:', stats.mean([aov[1] for aov in ts_results_sep]), 
'Value:', stats.mean([aov[2] for aov in ts_results_sep]), 'Fitness', stats.mean(ts_results), 'Time', stats.mean(ts_time))

print('Medias GRASP |', 'Age:', stats.mean([aov[0] for aov in gsp_results_sep]), 'Overall:', stats.mean([aov[1] for aov in gsp_results_sep]), 
'Value:', stats.mean([aov[2] for aov in gsp_results_sep]), 'Fitness', stats.mean(gsp_results), 'Time', stats.mean(gsp_time))

# Plota grafico de velas
plt.boxplot([rnd_results, gdy_results, gd_results, ts_results, gsp_results])
plt.xticks([1, 2, 3, 4, 5], ['Sol. Randômica', 'Sol. Gulosa', 'Descida de Gradiente', 'Busca Tabu', 'GRASP'])
plt.show()

# Teste de Student, dado um algoritmo A e B 
# Testa-se a hipótese nula que o desempenho de A é igual ao de B (M_a = M_b)
print('Teste para a hipótese nula M_gd = M_ts')
t,p = st.ttest_ind(gd_results, ts_results)
print('T value:', t, 'P value:', p)

print('Teste para a hipótese nula M_gd = M_gsp')
t,p = st.ttest_ind(gd_results, gsp_results)
print('T value:', t, 'P value:', p)

print('Teste para a hipótese nula M_ts = M_gsp')
t,p = st.ttest_ind(ts_results, gsp_results)
print('T value:', t, 'P value:', p)