# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:21:09 2020

@author: andre_000
"""

import glob
import cv2
import numpy as np
import pandas as pd
import pickle
import time
import matplotlib.pyplot as plt

from funcoes import *

#%% Leitura dos dados

df_HS = pd.read_excel('HS.xlsx')
df_RMS = pd.read_excel('RMS.xlsx')
df_michelson = pd.read_excel('michelson.xlsx')

#%% Gráficos




def sem_normalizar_erro():
    plt.figure(figsize=(8,6),dpi=80)
    # plt.plot(concentracao,medias,'ko')
    plt.errorbar(df['Concentracao'], df['Media_R'],
                 yerr=df['STD_R']/100 , fmt='ro',label='R')
    plt.errorbar(df['Concentracao'], df['Media_G'],
                 yerr=df['STD_G']/100 , fmt='go',label='G')
    plt.errorbar(df['Concentracao'], df['Media_B'],
                 yerr=df['STD_B']/100 , fmt='bo',label='B')
    plt.errorbar(df['Concentracao'], df[metrica.__name__ + '_valor'],
                 yerr=df[metrica.__name__ +'_std' ]/100,fmt='ko')
    plt.title('Grafico colorido ' + metrica.__name__)
    plt.xlabel("Concentracao [ml]")
    plt.ylabel("Media")


def sem_normalizar_std():
    plt.figure(figsize=(8,6),dpi=80)
    # plt.plot(concentracao,medias,'ko')
    plt.errorbar(df['Concentracao'], df['Media_R'],
                 yerr=df['STD_R'] , fmt='ro',label='R')
    plt.errorbar(df['Concentracao'], df['Media_G'],
                 yerr=df['STD_G'] , fmt='go',label='G')
    plt.errorbar(df['Concentracao'], df['Media_B'],
                 yerr=df['STD_B'] , fmt='bo',label='B')
    plt.errorbar(df['Concentracao'], df[metrica.__name__ + '_valor'],
                 yerr=df[metrica.__name__ +'_std' ],fmt='ko')
    plt.title('Grafico colorido ' + metrica.__name__)
    plt.xlabel("Concentracao [ml]")
    plt.ylabel("Media")

def normalizar():

    def normalizador(df):
        x = df.values
        return  (x-x.min())/(x.max() - x.min())
    df['Media_R_norm'] = normalizador(df['Media_R'])
    df['Media_G_norm'] = normalizador(df['Media_G'])
    df['Media_B_norm'] = normalizador(df['Media_B'])
    ################ mudar linha ################
    df['Media_norm'] = normalizador(df[metrica.__name__ + '_valor'])
    plt.figure(figsize=(8,6),dpi=80)
    # plt.plot(concentracao,medias,'ko')
    plt.errorbar(df['Concentracao'], df['Media_R_norm'],
                  fmt='ro--',label='R')
    plt.errorbar(df['Concentracao'], df['Media_G_norm'],
                  fmt='go--',label='G')
    plt.errorbar(df['Concentracao'], df['Media_B_norm'],
                  fmt='bo--',label='B')
    # ################ mudar linha ################
    # plt.errorbar(df['Concentracao'], df['Media_norm'],
    #              yerr=df[metrica.__name__ +'_erro'] , fmt='ko',label='K')
    ################ mudar linha ################
    plt.title('Grafico normalizado ' + metrica.__name__)
    plt.xlabel("Concentracao [ml]")
    plt.ylabel("Métrica normalizada")
#%%
metrica = michelson
df = df_michelson.copy()
# sem_normalizar_erro = True
# sem_normalizar_std = True
normalizar()
