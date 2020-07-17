# -*- coding: utf-8 -*-

def weber(imagem, tamanho=None):
    
    # Se eu não especificar nenhum tamanho
    # pegar o menor eixo (x,y) e rodar na maior parte da imagem
    if tamanho is None:
        tamanho = int(np.min(np.shape(imagem)) * 0.9)
        
    if type(imagem) == str:
        imagem = cv2.imread(imagem,0) 
    Back = recortar_quadrado(imagem, tamanho)
    Fore = recortar_quadrado(imagem, tamanho)
    denominador = np.min(Back)
    if denominador == 0:
        denominador = 1
    # print((np.max(Fore) - np.min(Back))/denominador)
    print(np.max(Fore) , np.min(Back))
    return (np.max(Fore) - np.min(Back))/denominador