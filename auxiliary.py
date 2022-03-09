from cmath import inf
import copy
from operator import index
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import time
import statistics as stats

from sklearn import preprocessing

team_size = 11
scaler = preprocessing.StandardScaler()

def import_data_fifa(elem_amount):    
    df = pd.read_csv('data/data.csv').sample(n=110,random_state=42)
    df = df[['Age', 'Overall', 'Value']]

    # Trata string de valor, transformando para INT
    df['Value'] = df['Value'].replace({"€": "", "M": "*1E6", "K": "*1E3"}, regex=True).map(pd.eval).astype(int)
    #print(df.head())
    return df

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

def get_means_scaled(solution, df):
    means = get_means(solution, df)
    scaled_means = scaler.fit_transform(means)
    return scaled_means

def print_formatted_means(means):
    print(*['[%.3f, %.3f, %.3f]' % (vals[0], vals[1], vals[2]) for vals in means])

def print_DPs(sol, df, scaled_df):
    print('DP Normal:', get_std(sol, df))
    print('DP Escalado:', get_std(sol, scaled_df), 'FITNESS:', fitness(sol, scaled_df))

def get_std(solution, df):
    means = get_means(solution, df)
    return get_std_means(means)

def get_std_scaled(solution, df):
    means = get_means(solution, df)
    scaled_means = scaler.fit_transform(means)
    return get_std_means(scaled_means)

# Dado as médias de uma solução
# Retorna Desvio Padrão dos três atributos (Age, Overall e Value)
def get_std_means(means):
    a = [aov[0] for aov in means]
    o = [aov[1] for aov in means]
    v = [aov[2] for aov in means]

    return [stats.stdev(a), stats.stdev(o), stats.stdev(v)]

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

# NÃO UTILIZADA
# Função de vizinhança com alterações fortes
def get_neighborhood_wild(solution):
    neighborhood = []

    # O número de vizinhos é o tamanho do time
    for n in range(team_size):

        # Embaralha grupos
        group_idxs = [i for i in range(len(solution))]
        random.shuffle(group_idxs)

        # Copia solução
        neighbor = copy.deepcopy(solution)

        # Escolher pares de grupos aleatóriamente e trocar dois jogadores
        # Desse modo, o vizinho será a solução com um jogador trocado em cada grupo
        for i in range(0,len(group_idxs),2):
            g1_index = group_idxs[i]
            g2_index = group_idxs[i+1]

            for j in range(2):
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
    fitness = std[0] + std[1] + std [2]

    return fitness


# df = import_data_fifa(team_size*10)
# scaled_df = scale_dataframe(df)
# while(True):
#     input ()
#     solution = get_random_solution(scaled_df)
#     print(fitness(solution, scaled_df))
