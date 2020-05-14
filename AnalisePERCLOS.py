from scipy.spatial import distance
import math

class AnalisePERCLOS(object):
    
    #Calculando a Razão de Aspecto
    def razaoDeAspecto(self, shape):
        
        #RAD = RAZÃO DE ASPECTO DIREITA
        distVerticalDir = distance.euclidean((shape[24] + shape[25]) // 2, (shape[27] + shape[28]) // 2)
        distHorizontalDir = distance.euclidean(shape[23], shape[26])
        rad = distVerticalDir / distHorizontalDir
        
        #RAE = RAZÃO DE ASPECTO ESQUERDA
        distVerticalEsq = distance.euclidean((shape[18] + shape[19]) // 2, (shape[21] + shape[22]) // 2)
        distHorizontalEsq = distance.euclidean(shape[17], shape[20])
        rae = distVerticalEsq / distHorizontalEsq
        
        ra = (rad + rae) / 2
        return ra
    
    #Calcular desvio padrão
    def desvioPadrao(self, indiceFrameCalibragem, matrizRA):
        variancia, media = 0, 0
        count = 0
        
        #Calculo da média
        for i in range(indiceFrameCalibragem + 1):
            media += matrizRA[0][i]
            count += 1
        media = media / count
    
        #Calculo da variância
        for j in range(indiceFrameCalibragem + 1):
            variancia = variancia + math.pow((matrizRA[0][j] - media), 2)
        variancia = variancia / count
    
        #Raiz quadrada da variância
        devPadrao = math.sqrt(variancia)
        return devPadrao
    
    #Calcular erro padrão
    def erroPadrao(self, x, matrizRA):
        if x > 0:
            erroPad = matrizRA[1][x] / math.sqrt(x)
        else:
            erroPad = 0
        return erroPad
    
    #Calibragem dos valores adquiridos no processo de coleta de dados
    def calibragemAberturaOlhos(self, matrizRA):
        aberturaMin = matrizRA[0].min()
        aberturaMax = matrizRA[0].max()
        for x in range(len(matrizRA[0])):
            if (((matrizRA[0][x] - aberturaMin) * 100) / (aberturaMax - aberturaMin) >= 95):
                matrizRA[0][x] = matrizRA[0][x] - matrizRA[2][x]
                
            if (((matrizRA[0][x] - aberturaMin) * 100) / (aberturaMax - aberturaMin) <= 5):
                matrizRA[0][x] = matrizRA[0][x] + matrizRA[2][x]

        return matrizRA
        
    #Coversor de todos os valores da matriz RA para porcentagem
    def converterTudoEmPorcentagem(self, matrizRA):
        matrizAnalitica = []
        aberturaMin = matrizRA[0].min()
        aberturaMax = matrizRA[0].max()
        for i in range(len(matrizRA[0])):
            #Calcular a porcentagem
            porcentagem = (matrizRA[0][i] - aberturaMin) / (aberturaMax - aberturaMin) * 100
            matrizAnalitica.append(porcentagem)
        return matrizAnalitica