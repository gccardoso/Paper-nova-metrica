# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 23:02:40 2020

@author: André Vitor
"""

import glob
import cv2
import numpy as np
import pandas as pd
import pickle
import time
import matplotlib.pyplot as plt

from funcoes import *


#%%
arquivos_na_pasta =  glob.glob('Imagens\*.jpg') # modificar caso necessário
arquivos_na_pasta.sort()
listaImagens = []
for file in arquivos_na_pasta:
    print(file)
    listaImagens.append(file)
#%%
with open('objs.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
    listaImagens,testImg, df, df2, df3 = pickle.load(f)
with open('df_copia.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
    df_copia = pickle.load(f)

#%% Rodar preto e branco
tamanho = 1000
iteracoes = 10000
N = iteracoes
temp = []

for metrica in [weber]:
    valor_lista = []
    std_lista=[]
    
    for file in arquivos_na_pasta:
        tic = time.time()
        imagem = cv2.imread(file,0) 
        valor, std  = quadrados_media_std(imagem,N,tamanho,metrica)
        toc = time.time()
        print("\nTempo de execução: ",toc-tic)
        print("metrica: ", metrica.__name__)
        print("imagem: ", file)
        print("Valor: ", valor)
        valor_lista.append(valor)
        std_lista.append(std)
        


    # 2. Salvar dados no dataframe.
    df[metrica.__name__ + '_valor'] = valor_lista
    df[metrica.__name__ + '_std']   = std_lista

    # 3. Calcular os erros padrão, coloque também no dataframe.
    df[metrica.__name__ + '_erro']  = df[metrica.__name__ + '_std']/100 #std / sqrt(10.000)
#%%

# def aaaa(tamanho, iteracoes,caminho,deletar=True)
"""
Esta função faz análise nas imagens coloridas separando em RGB. 
Retorna um dataframe e  um plot.
deletar o último valor = True
"""
nomesR = []
mediasR = []
desviosR = []

nomesG = []
mediasG = []
desviosG = []

nomesB = []
mediasB = []
desviosB = []

funcao = weber
iteracoes = 10000
tamanho = 1000
for _, nome in enumerate(arquivos_na_pasta):
    imagem = cv2.imread(nome)
    r = imagem[:,:,2]
    g = imagem[:,:,1]
    b = imagem[:,:,0]
    print(nome)
    x, std = quadrados_media_std(r, iteracoes, tamanho,funcao)
    print('media  = %.2f' % x)
    nomesR.append(nome[:-4] + '_' + 'r') # ignoro o .jpg
    # fica do jeito recorte_leite_00_r
    mediasR.append(x)
    desviosR.append(std)
    print('')
    
    x, std = quadrados_media_std(g, iteracoes, tamanho,funcao)
    print('media  = %.2f' % x)
    nomesG.append(nome[:-4] + '_' + 'g') # ignoro o .jpg
    mediasG.append(x)
    desviosG.append(std)
    print('')
    
    x, std = quadrados_media_std(b, iteracoes, tamanho,funcao)
    print('media  = %.2f' % x)
    nomesB.append(nome[:-4] + '_' + 'b') # ignoro o .jpg
    # fica do jeito recorte_leite_00_r
    mediasB.append(x)
    desviosB.append(std)
    print('')
    
concentracao = [0,5,10,15,20,25,30,35,99]
# for i in nomesR:
#     x = i.split(sep='_')[2]
#     print(int(x))
#     concentracao.append(int(x))

#%%
dfR = pd.DataFrame({
    "Nomes": nomesR,
    "Media_R": mediasR,
    "STD_R": desviosR,
    "Concentracao": concentracao
})
dfG = pd.DataFrame({
    "Nomes": nomesG,
    "Media_G": mediasG,
    "STD_G": desviosG,
    "Concentracao": concentracao
})
dfB = pd.DataFrame({
    "Nomes": nomesB,
    "Media_B": mediasB,
    "STD_B": desviosB,
    "Concentracao": concentracao
})
#%%
df = pd.DataFrame({
    "Nomes": nomesR,
    "Media_R": mediasR,
    "STD_R": desviosR,
    "Media_G": mediasG,
    "STD_G": desviosG,
    "Media_B": mediasB,
    "STD_B": desviosB,
    "Concentracao": concentracao 
    })

#%% Sem normalizar

plt.figure(figsize=(8,6),dpi=80)
# plt.plot(concentracao,medias,'ko')
plt.errorbar(df['Concentracao'] * 0.1, df['Media_R'],
             yerr=df['STD_R'] / np.sqrt(iteracoes), fmt='ro',label='R')
plt.errorbar(df['Concentracao'] * 0.1, df['Media_G'],
             yerr=df['STD_G'] / np.sqrt(iteracoes), fmt='go',label='G')
plt.errorbar(df['Concentracao'] * 0.1, df['Media_B'],
             yerr=df['STD_B'] / np.sqrt(iteracoes), fmt='bo',label='B')
plt.title('Grafico colorido')
plt.xlabel("Concentracao [ml]")
plt.ylabel("Media")

#%% Normalizando

def normalizador(df):
    x = df.values
    return  (x-x.min())/(x.max() - x.min())
df['Media_R_norm'] = normalizador(df['Media_R'])
df['Media_G_norm'] = normalizador(df['Media_G'])
df['Media_B_norm'] = normalizador(df['Media_B'])
################ mudar linha ################
df['Media_norm'] = normalizador(df['michelson_valor'])
plt.figure(figsize=(8,6),dpi=80)
# plt.plot(concentracao,medias,'ko')
plt.errorbar(df['Concentracao'], df['Media_R_norm'],
             yerr=df['STD_R'] / np.sqrt(iteracoes), fmt='ro',label='R')
plt.errorbar(df['Concentracao'], df['Media_G_norm'],
             yerr=df['STD_G'] / np.sqrt(iteracoes), fmt='go',label='G')
plt.errorbar(df['Concentracao'], df['Media_B_norm'],
             yerr=df['STD_B'] / np.sqrt(iteracoes), fmt='bo',label='B')
################ mudar linha ################
plt.errorbar(df['Concentracao'], df['Media_norm'],
             yerr=df['RMS_erro'] / np.sqrt(iteracoes), fmt='ko',label='K')
################ mudar linha ################
plt.title('Grafico colorido RMS')
plt.xlabel("Concentracao [ml]")
plt.ylabel("Métrica normalizada")
