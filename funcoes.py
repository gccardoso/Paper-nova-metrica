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
    
    denominador = np.max(imagem_GS)-np.min(imagem_GS)
    if denominador == 0:
        denominador = 1
    
    
    hs = (valor2 - valor1)/denominador
    
    return hs

def michelson(imagem):
    if type(imagem) == str:
        imagem = cv2.imread(imagem,0) 
    elif type(imagem) == np.ndarray:
        imagem = imagem # NÃO NECESSARIAMENTE PRETO E BRANCO
#     imagem = cv2.imread(imagem,0)
    numerador = np.max(imagem) - np.min(imagem)
    denominador = np.max(imagem) + np.min(imagem)
    if denominador == 0:
        denominador = 1
    
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
    denominador = np.min(Back)
    if denominador == 0:
        denominador = 0
    return (np.max(Fore) - np.min(Back)/)

def recortar_quadrado(imagem, tamanho):
    """
    Retorna um recorte da imagem de tamanho tamanho....
    Pedaço aleatório da imagem.

    Parameters
    ----------
    imagem : imagem em formato array
        imagem em formato array
    tamanho : int, optional
        Tamanho de um quadrado.

    Returns
    -------
    recorte : imagem em formato array
        retorna um pedaço da imagem original.

    """
    # tamanho do quadrado:
    
    x, y = imagem.shape
    # Intervalo no qual eu posso pegar os pontos
    intervalox = x - tamanho
    intervaloy = y - tamanho

    pontox = np.random.randint(0, intervalox)
    pontoy = np.random.randint(0, intervaloy)

    retangulo = [pontox, pontoy, pontox + tamanho, pontoy + tamanho]
    recorte = imagem[retangulo[0]:retangulo[2], retangulo[1]:retangulo[3]]

    return recorte

def histo_norm(imagem):
    """
    Retorna o histograma normalizado da imagem, isto é se somarmos todos os valores deve dar um,
    mas o formato do histograma continua o mesmo.
    Parameters
    ----------
    imagem

    Returns
    -------

    """
    # pega o histograma da imagem, equivalente ao imhist do matlab
    count, _ = np.histogram(imagem, bins=256, range=[0, 256])

    histo = count / sum(count)
    return histo

def potential_contrast(imagem, tamanho):
    """

    Parameters
    ----------
    imagem
    tamanho: tamanho dos quadradinhos

    Returns
    -------
    Retorna um valor entre 0 e 255, que é a minha métrica de contraste, baseada naquele artigo.
    """
    Back = recortar_quadrado(imagem, tamanho)
    Fore = recortar_quadrado(imagem, tamanho)

    histoBack = histo_norm(Back)
    histoFore = histo_norm(Fore)

    z = histoBack - histoFore
    z0 = z > 0
    z = z * z0 * 255
    return sum(z)

def media_quadrados(imagem, N, tamanho):
    """
    Esta função roda N quadrados de certo tamanho na imagem selecionada. 
    Retorna:
    lista com médias, lista com desvios padrão
    """
    lista = []
    for _ in range(N):
        temp = potential_contrast(imagem, tamanho)
        lista.append(temp)
    # print('desvio padrao = ', "%.2f" % (np.std(lista)))
    return np.mean(lista), np.std(lista)

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
    
def recortar_quadrado_inverso(imagem, tamanho):
    """
    Retorna um recorte da imagem de tamanho tamanho....
    Pedaço aleatório da imagem.

    Parameters
    ----------
    imagem : imagem em formato array
        imagem em formato array
    tamanho : int, optional
        Tamanho de um quadrado.

    Returns
    -------
    recorte : imagem em formato array
        retorna um pedaço da imagem original.

    """
    
    # Seja uma imagem de tamanho x,y
    x,y = imagem.shape
    
    # Quero retirar N pixels das bordas
    # Olhando para somente o eixo x, ele deve ter um tamanho x-pixels
    # Então devo escolher o primeiro valor entre 0 e pixels
    # e o último valor (x- pixels) + pixels
    
    # Intervalo no qual eu posso pegar os pontos
    intervalox = tamanho
    intervaloy = tamanho

    pontox = np.random.randint(0, intervalox)
    pontoy = np.random.randint(0, intervaloy)

    retangulo = [pontox, pontoy, pontox + x-tamanho, pontoy + y - tamanho]
    recorte = imagem[retangulo[0]:retangulo[2], retangulo[1]:retangulo[3]]

    return recorte








