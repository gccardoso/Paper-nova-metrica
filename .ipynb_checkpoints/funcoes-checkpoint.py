# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 19:40:53 2020

@author: Usuario
"""
import cv2
import numpy as np

def HS(imagem):
    """
    
    Parametros
    ----------
    imagem: str
        path da imagem
    
    Retorna
    -------
    hs: float
        Valor da métrica HS para a imagem escolhida
    
    """
    
    if type(imagem) == str:
        imagem_GS = cv2.imread(imagem,0)  # 'array (x,y)'
    elif type(imagem) == np.ndarray:
        imagem_GS = imagem # NÃO NECESSARIAMENTE PRETO E BRANCO

          
    count, _ = np.histogram(imagem_GS, bins=256, range=[0, 256])

    histo = count / sum(count)

    cumulative  = np.cumsum(count)
    normcum = (cumulative - min(cumulative))/(max(cumulative)-min(cumulative))
    
    valor1 = np.where(normcum == min(normcum, key=lambda x:abs(x-0.25)))[0][0]
    valor2 = np.where(normcum == min(normcum, key=lambda x:abs(x-0.75)))[0][0]
    
    hs = (valor2 - valor1)/(np.max(imagem_GS)-np.min(imagem_GS))
    return hs

def michelson(imagem):
    if type(imagem) == str:
        imagem = cv2.imread(imagem,0) 
    elif type(imagem) == np.ndarray:
        imagem = imagem # NÃO NECESSARIAMENTE PRETO E BRANCO
#     imagem = cv2.imread(imagem,0)
    numerador = np.max(imagem) - np.min(imagem)
    denominador = np.max(imagem) + np.min(imagem)
    return numerador/denominador
    
def RMS(imagem):
    if type(imagem) == str:
        imagem = cv2.imread(imagem,0) 
    elif type(imagem) == np.ndarray:
        imagem = imagem # NÃO NECESSARIAMENTE PRETO E BRANCO
#     imagem = cv2.imread(imagem,0)
    imagem = imagem/255
    x,y = imagem.shape
    LM = x * y
    Imed = np.sum(imagem)/LM
    soma1 = (imagem - Imed)**2
    soma2 = np.sum(soma1)
    return np.sqrt(soma2/LM)


def quadrados_media_std(imagem, N, tamanho,metrica):
    """
    Aplica uma certa funcao N quadrados de certo tamanho na imagem selecionada. 
    Retorna:
    lista com médias, lista com desvios padrão
    """
    
    lista = []
    for _ in range(N):
        img_recortada = recortar_quadrado(imagem, tamanho)
        valor = metrica(img_recortada)
        lista.append(valor)
    return np.mean(lista), np.std(lista)

def weber(imagem,tamanho):
    if type(imagem) == str:
        imagem = cv2.imread(imagem,0) 
        
    Back = recortar_quadrado(imagem, tamanho)
    Fore = recortar_quadrado(imagem, tamanho)
    
    return (np.max(Fore) - np.min(Back)/np.min(Back))
        
    
    
    
    
    
    
    
    