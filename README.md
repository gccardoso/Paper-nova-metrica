# Paper-nova-metrica
Repositório para arquivos sobre a nova métrica sendo desenvolvida.

## Algumas características

- As funções recebem uma imagem ou como um array numérico (e roda normalmente) ou o caminho da imagem em string (transforma a imagem em preto e branco e continua). Portanto para ler imagens coloridas, deve-se ter como input um array

## Funções

### Métricas
- HS
- RMS
- Michelson
- Haziness

### Outras
- quadrados_media_std(imagem, N, tamanho,metrica):     Aplica uma certa funcao N vezes, em quadrados de certo *tamanho* na imagem selecionada. 
- recortar_quadrado(imagem, tamanho):     Retorna um recorte da imagem de tamanho *tamanho* Pedaço aleatório da imagem.
