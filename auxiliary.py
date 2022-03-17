import copy
from operator import index
import random
import pandas as pd
import numpy as np
import statistics as stats
from sklearn import preprocessing

#####################
# Funções Auxiliares
#####################

team_size = 11
scaler = preprocessing.StandardScaler()

# Importa base de dados
def import_data_fifa(elem_amount, rnd_state = None):    
    df = pd.read_csv('data/data.csv').sample(n=110,random_state=rnd_state)
    df = df[['Age', 'Overall', 'Value']]

    # Trata string de valor (e.g. €110.5M), transformando para int
    df['Value'] = df['Value'].replace({"€": "", "M": "*1E6", "K": "*1E3"}, regex=True).map(pd.eval).astype(int)
    #print(df.head())
    return df

# Retorna solução randômica
def get_random_solution(df):
    teams = []
    indexes = df.index.values.tolist()

    while(len(indexes) > 0):
        team = []
        for i in range(team_size):
            rnd = random.randrange(0, len(indexes))
            team.append(indexes[rnd])
            indexes.pop(rnd)
        teams.append(team)
    return teams

# Função de construção gulosa
def get_random_greedy_solution(df, pool_size):
    indexes = df.index.values.tolist()
    team_amount = len(df.index)//team_size
    teams = [[] for i in range(team_amount)]

    for n in range(team_size):

        best = []

        for i in range(pool_size):
            idx = copy.copy(indexes)
            random.shuffle(idx)
            candidate = copy.deepcopy(teams)

            # Atribui um jogador (dos que restam) randômicamente a cada time
            for j in range(team_amount-1,-1,-1):
                candidate[j].append(idx[j])
                idx.pop(j)

            if(fitness(candidate, df) < fitness(best, df)):
                best = candidate

        teams = best
        for team in teams:
            indexes.remove(team[n])

    return teams

# Escala data frame com StandardScaler
def scale_dataframe(df):
    scaled_df = pd.DataFrame(scaler.fit_transform(df), index=df.index, columns=df.columns)
    return scaled_df

# Retorna médias de cada time para Age, Overall e Value
def get_means(solution, df):
    means = []
    for i in range(len(solution)):
        total_age = 0.0
        total_overall = 0.0
        total_value = 0.0
        curr_team_size = len(solution[i])
        for j in range(curr_team_size):
            index = solution[i][j]
            player = df.loc[index]
            total_age += player[0]
            total_overall += player[1]
            total_value += player[2]
        aov = [total_age/curr_team_size, total_overall/curr_team_size, total_value/curr_team_size]
        means.append(aov)
    return means

# Função de debug, imprime Desvios Padrões e fitness para comparação
def print_DPs(sol, df, scaled_df):
    print('DP Normal:', get_std(sol, df))
    print('DP Escalado:', get_std(sol, scaled_df), 'FITNESS:', fitness(sol, scaled_df))

# Dado as médias de uma solução
# Retorna Desvio Padrão dos três atributos (Age, Overall e Value)
def get_std_means(means):
    a = [aov[0] for aov in means]
    o = [aov[1] for aov in means]
    v = [aov[2] for aov in means]

    return [stats.stdev(a), stats.stdev(o), stats.stdev(v)]

# Dado uma solução, retorna desvio padrão
def get_std(solution, df):
    means = get_means(solution, df)
    std = get_std_means(means)
    return std

# Função de vizinhança
# Para cada grupo g1, escolher outro grupo g2 aleatóriamente, formando pares
# Escolher um jogador de g1 e de g2 aleatóriamente e trocar os dois
# Desse modo, cada vizinho será a solução com dois jogadores trocados
def get_neighborhood(solution):
    neighborhood = []

    indexes = [i for i in range(len(solution))]
    random.shuffle(indexes)

    for i in range(0,len(indexes),2):
        neighbor = copy.deepcopy(solution)
        g1_index = indexes[i]
        g2_index = indexes[i+1]

        rnd_player1 = random.randrange(0,team_size)
        rnd_player2 = random.randrange(0,team_size)
        p1 = neighbor[g1_index].pop(rnd_player1)
        p2 = neighbor[g2_index].pop(rnd_player2)
        neighbor[g1_index].append(p2)
        neighbor[g2_index].append(p1)
        neighborhood.append(neighbor)
    return neighborhood

# Returna solution fitness
# Quanto menor melhor
def fitness(solution, df):
    if(len(solution) == 0 or len(solution[0]) == 0):
        return np.Inf

    means = get_means(solution, df)
    std = get_std_means(means)
    fitness = (std[0] + std[1] + std [2]) / 3

    return fitness
