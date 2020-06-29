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

