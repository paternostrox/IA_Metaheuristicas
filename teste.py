import time
import auxiliary as aux
import gradient_descent as gd
import tabu_search as ts
import grasp as gsp
import scipy.stats as st

# Importa base de dados
df = aux.import_data_fifa(110, 42)
# Escala base de dados
scaled_df = aux.scale_dataframe(df)

test_amount = 30

# Roda gradient descent
gd_sols = []
for i in range(test_amount):
    # Toma solução randômica como primeira solução
    start_sol = aux.get_random_solution(scaled_df)
    # Roda algoritmo
    final_sol = gd.gradient_descent(start_sol, scaled_df)
    gd_sols.append(final_sol)

# Roda tabu search
ts_sols = []
for i in range(test_amount):
    # Toma solução randômica como primeira solução
    start_sol = aux.get_random_solution(scaled_df)
    # Roda algoritmo
    final_sol = ts.tabu_search(start_sol, scaled_df)
    ts_sols.append(final_sol)

# Roda grasp
gsp_sols = []
for i in range(test_amount):
    # Roda algoritmo (soluções são construídas pelo grasp)
    final_sol =gsp.grasp(scaled_df)
    gsp_sols.append(final_sol)

gd_results = []
ts_results = []
gsp_results = []

for i  in range(test_amount):
    gd_results.append(aux.fitness(gd_sols[i], scaled_df))
    ts_results.append(aux.fitness(ts_sols[i], scaled_df))
    gsp_results.append(aux.fitness(gsp_sols[i], scaled_df))

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

# Plota grafico de velas da acuracia
# data_frame = pd.DataFrame(score_data, columns=['modelo', 'fold_id', 'acurácia'])
# sns.boxplot(x='modelo', y='acurácia', data=data_frame)
# plt.show()