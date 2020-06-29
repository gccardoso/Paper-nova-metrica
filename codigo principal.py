# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 23:02:40 2020

@author: André Vitor
"""

import glob
import cv2
import numpy as np
import pickle
import time

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

for _, nome in enumerate(arquivos_na_pasta):
    imagem = cv2.imread(nome)
    r = imagem[:,:,2]
    g = imagem[:,:,1]
    b = imagem[:,:,0]
    print(nome)
    x, std = media_quadrados(r, iteracoes, tamanho,funcao)
    print('media  = %.2f' % x)
    nomesR.append(nome[:-4] + '_' + 'r') # ignoro o .jpg
    # fica do jeito recorte_leite_00_r
    mediasR.append(x)
    desviosR.append(std)
    print('')
    
    x, std = media_quadrados(g, iteracoes, tamanho)
    print('media  = %.2f' % x)
    nomesG.append(nome[:-4] + '_' + 'g') # ignoro o .jpg
    mediasG.append(x)
    desviosG.append(std)
    print('')
    
    x, std = media_quadrados(b, iteracoes, tamanho)
    print('media  = %.2f' % x)
    nomesB.append(nome[:-4] + '_' + 'b') # ignoro o .jpg
    # fica do jeito recorte_leite_00_r
    mediasB.append(x)
    desviosB.append(std)
    print('')
    
concentracao = []
for i in nomesR:
    x = i.split(sep='_')[2]
    print(int(x))
    concentracao.append(int(x))

dfR = pd.DataFrame({
    "Nomes": nomesR,
    "Potencial dos quadrados": mediasR,
    "Desvio padrao": desviosR,
    "Concentracao": concentracao
})
dfG = pd.DataFrame({
    "Nomes": nomesG,
    "Potencial dos quadrados": mediasG,
    "Desvio padrao": desviosG,
    "Concentracao": concentracao
})
dfB = pd.DataFrame({
    "Nomes": nomesB,
    "Potencial dos quadrados": mediasB,
    "Desvio padrao": desviosB,
    "Concentracao": concentracao
})