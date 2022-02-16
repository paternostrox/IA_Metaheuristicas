import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import time
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score, balanced_accuracy_score, precision_score, recall_score, f1_score

# Importa base de dados APPLE
def import_apple_sentiment():
    data_frame = pd.read_csv('data/apple_twitter_sentiment_dfe.csv', encoding='latin-1', skiprows=1)
    data_X = data_frame.iloc[:,11]
    data_y = data_frame.iloc[:,5]
    #print_data(data_X, data_y, label_apple, 5) # Imprime dados
    print('distribuicao de classes = ', class_distribution(data_y)) # Imprime distribuição de classe

    # Cria grade adequada para a base
    grades = [{'alpha': [0.5, 1.0, 4.0, 8.0]}, 
    {'min_samples_split': [2 ,5], 'min_samples_leaf' : [1 ,2], 'n_estimators': [50, 100, 200]},
    {'C': [1, 10, 100, 1000]}, 
    {'C': [0.1, 1, 10, 100]}]

    return [data_X, data_y, grades]

# Importa base de dados SENTIMENT 140
def import_sentiment140(elem_amount):
    data_frame = pd.read_csv('data/1_6mi_tweets_training.csv', encoding='latin-1', nrows=elem_amount, skiprows=799999 - elem_amount//2)
    data_X = data_frame.iloc[:,5]
    data_y = data_frame.iloc[:,0]
    #print_data(data_X, data_y, label_140, 5) # Imprime dados
    print('distribuicao de classes = ', class_distribution(data_y)) # Imprime distribuição de classe

    # Cria grade adequada para a base
    grades = [{'alpha': [0.5, 1.0, 4.0, 8.0]}, 
    {'min_samples_split': [2 ,5], 'min_samples_leaf' : [1 ,2], 'n_estimators': [50, 100, 200]}, 
    {'C': [1, 10, 100, 1000]}, 
    {'C': [1, 10, 100, 1000]}]

    return [data_X, data_y, grades]

polarity_140 = {0 : 'negative', 2 : 'neutral', 4 : 'positive'}
polarity_apple = {'1' : 'negative', '3' : 'neutral', '5' : 'positive', 'not_relevant' : 'not_relevant'}

def label_140(index):
    return polarity_140[index]

def label_apple(index):
    return polarity_apple[index]

# Imprime elementos da base (para verificacao)
def print_data(x, y, label, count):
    for i in range(count):
        print(x.iloc[i], ' => ', label(y.iloc[i]))

# Retorna distribuição de classes
def class_distribution (class_data):

    tam = len(class_data)
    labels = np.unique(class_data)
    
    classDistr = []
    for class_value in labels:   
        cvc = len([1 for i in class_data if i == class_value])
        classDistr += [(class_value, cvc/tam)]

    return classDistr

###############################################################################

# T1 - MACHINE LEARNING

# Prepara base de dados
data_X, data_y, grades = import_apple_sentiment()
#data_X, data_y, grades = import_sentiment140(4000)

# Definicoes (modelagem)
count_vect = CountVectorizer()
X_data_counts = count_vect.fit_transform(data_X)
tfidf_transformer = TfidfTransformer()
X_data_tfidf = tfidf_transformer.fit_transform(X_data_counts)

classifiers = [
    MultinomialNB(),
    RandomForestClassifier(n_jobs=-1),
    LinearSVC(dual=False, max_iter=10000),
    LogisticRegression(max_iter=1000)
]

gs_cv = 2
score_data = []

for i in range(len(classifiers)):
    start = time.time()
    clf_name = classifiers[i].__class__.__name__

    # Treina classificador
    gs = GridSearchCV(estimator=classifiers[i],  param_grid = grades[i], 
                  scoring='accuracy', cv = gs_cv)
    gs.fit(X_data_tfidf, data_y)

    rkf = RepeatedStratifiedKFold(n_splits=5, n_repeats=6)
    scores = cross_val_score(gs, X_data_tfidf, data_y, scoring='accuracy', cv = rkf)

    # Imprime metricas
    mean = scores.mean()
    std = scores.std()
    inf, sup = stats.norm.interval(0.95, loc=mean, scale=std/np.sqrt(len(scores)))
    print('\n', clf_name)
    print("acuracia media: %0.4f, desvio padrao: %0.4f" % (mean, std))
    print ("intervalo de confianca da acuracia (95%%): (%0.4f, %0.4f)" % (inf, sup))
    stop = time.time()
    print("tempo de execucao: %0.4f" % (stop-start), "s")

    # Adiciona a lista
    for fold_id,score in enumerate(scores):
        score_data.append((clf_name,fold_id, score))

# Plota grafico de velas da acuracia
data_frame = pd.DataFrame(score_data, columns=['modelo', 'fold_id', 'acurácia'])
sns.boxplot(x='modelo', y='acurácia', data=data_frame)
plt.show()