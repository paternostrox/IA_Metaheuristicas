import random
from tokenize import group
import auxiliary as aux

def grasp():
    # Importa base de dados
    df = aux.import_data_fifa(110)

# Função de construção gulosa
def get_random_greedy_solution_rcl(df):
    indexes = df.index.values.tolist()
    team_amount = len(df.index)
    groups = []

    # Inicia adicionando um jogador randômico em cada time
    # Caso contrário algoritmo ficará enviesado a adicionar os menores primeiro
    for i in range(team_amount):
        rnd = random.randrange(0,len(indexes))
        groups.append([indexes[rnd]])
        indexes.pop(rnd)

    while(len(indexes) > 0):
        for i in range(team_amount):
            # restricted candidate list (RCL)
            best_candidates = []
            

def get_random_greedy_solution_quick(df):
    groups = []

grasp()