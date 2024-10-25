import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from io import open
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer

# Configurações do pandas
pd.options.display.max_columns = 150 # Setando a quantidade maxima de colunas
pd.options.display.float_format = "{:.2f}".format # Ajustando a exibição do float no pandas

# Carregando os dados 
data = pd.read_csv('data-final.csv', sep='\t') # separador tab

# Retirando dados que não serão usados
data.drop(data.columns[50:110], axis=1, inplace=True)

# A partir de um data.describe() conseguimos descobrir que existem valores de pontuação 0, o que é irreal numa escala de respostas de 1 a 5
# Com o método data["EXT1"].value_counts() Conseguimos a partir de uma das perguntas identificar a quantidade de respostas 0 presentes nela
# Exclusão dos dados com valores iguais a 0 do data frame 
data = data[(data > 0.00).all(axis=1)]

# Definindo grupo de pessoas similares
# Primeiramente testando numero ideal de clusters através do KMeans método elbor?
kmeans = KMeans()
visualizer = KElbowVisualizer(kmeans, k=(2,10)) # Definindo uma quantidade de clusters entre 2 e 10 

data_sample = data.sample(n=5000, random_state=1) # Pegando uma amostra randomica de dados correspondente a 5000 resultados

visualizer.fit(data_sample)
#visualizer.poof()

kmeans = KMeans(n_clusters=5) #número ideal calculado anteriormente
k_fit = kmeans.fit(data)

# Rótulando dataframe
predictions = k_fit.labels_
data['Clusters'] = predictions

#print(data.head())
#print(data['Clusters'].value_counts)

#print(data.groupby('Clusters').mean())

# Separação por grupos de perguntas
col_list = list(data)

""" lista de perguntas
['EXT1', 'EXT2', 'EXT3', 'EXT4', 'EXT5', 'EXT6', 'EXT7', 'EXT8', 'EXT9', 'EXT10', 
 'EST1', 'EST2', 'EST3', 'EST4', 'EST5', 'EST6', 'EST7', 'EST8', 'EST9', 'EST10', 
 'AGR1', 'AGR2', 'AGR3', 'AGR4', 'AGR5', 'AGR6', 'AGR7', 'AGR8', 'AGR9', 'AGR10', 
 'CSN1', 'CSN2', 'CSN3', 'CSN4', 'CSN5', 'CSN6', 'CSN7', 'CSN8', 'CSN9', 'CSN10', 
 'OPN1', 'OPN2', 'OPN3', 'OPN4', 'OPN5', 'OPN6', 'OPN7', 'OPN8', 'OPN9', 'OPN10', 
 'Clusters']"""

ext = col_list[0:10]
est = col_list[10:20]
agr = col_list[20:30]
csn = col_list[30:40]
opn = col_list[40:50]

# Calcular média de cada grupo de questões em busca de padrões

# soma por grupo
data_soma = pd.DataFrame()
data_soma['extroversion'] = data[ext].sum(axis=1)/10
data_soma['neurotic'] = data[est].sum(axis=1)/10
data_soma['agreeable'] = data[agr].sum(axis=1)/10
data_soma['conscientious'] = data[csn].sum(axis=1)/10
data_soma['open'] = data[opn].sum(axis=1)/10
data_soma['clusters'] = predictions

# Armazenando em variavel a média agrupada por tipo de personalidade
data_clusters = data_soma.groupby('clusters').mean() 

# Plotando figura para analise dos resultados
plt.figure(figsize=(22,3))

for i in range(0, 5):
    plt.subplot(1, 5, i+1)
    plt.bar(data_clusters.columns, data_clusters.iloc[:, i], color='green', alpha=0.2)
    plt.plot(data_clusters.columns, data_clusters.iloc[:, i], color='red')
    plt.title('Grupo ' + str(i))
    plt.xticks(rotation=45)
    plt.ylim(0,4)
    plt.show()

