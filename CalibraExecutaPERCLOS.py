# -*- coding: utf-8 -*-
'''
Created on 16 de jun de 2018

@author: almer
'''
from PyQt5.Qt import QTime, QThread, pyqtSignal, QPixmap, Qt
import pyqtgraph as pg
import dlib, time, cv2
import numpy as np
from imutils import face_utils
from scipy.spatial import distance

from PyQt5 import QtCore
from PyQt5.QtGui import QImage
from MensagemFalada import MensagemFalada
from AnalisePERCLOS import AnalisePERCLOS
from GerarArquivoDeDados import GerarArquivoDeDados
from ArquivoCalibracao import ArquivoCalibracao
import imutils


class CalibraExecutaPERCLOS(QThread):
    # Captura de Imagem
    changePixmap = pyqtSignal(QPixmap)
    # Contador para calcular o FPS
    contadorLoop = pyqtSignal(str)

    # Resumo da Calibragem PERCLOS
    valorMaxPERCLOS = pyqtSignal(str)
    valorMinPERCLOS = pyqtSignal(str)
    PThreshold = pyqtSignal(str)

    # Alimenta��o de dados dos Gr�ficos
    plotarCalibragem = pyqtSignal(pg.PlotItem)

    # Alimentação de dados dos Gr�ficos
    variaveisGrafico = pyqtSignal(list)

    # Dados para a tela de log
    msgLog = pyqtSignal(str)

    def __init__(self, parent=None, nome="", framesCalibragem=100, threshold=70):
        QThread.__init__(self, parent=parent)
        self.hora = QTime()
        self.framesCalibragem = framesCalibragem
        self.threshold = threshold
        self.usuario = nome

        self.arq_predicao = "IAs\\shape_predictor_ID12_37fl_cfbo_pyis.dat"
        self.detector = dlib.get_frontal_face_detector()
        self.predicao = dlib.shape_predictor(self.arq_predicao)
        self.judite = MensagemFalada()
        self.analisePERCLOS = AnalisePERCLOS()
        arquivoCalibracao = ArquivoCalibracao()
        self.valorMaximo, self.valorMinimo, self.nome = arquivoCalibracao.abrirArquivoCalibracao()

    def __del__(self):
        self.wait()

    def run(self):
        self.judite.scriptInicial()
        self.judite.scriptContagem()

        self.calibracaoPERCLOS()

        self.judite.scriptIniciarExecucao()

        self.execucaoPERCLOS()

    def calibracaoPERCLOS(self):

        # Habilitando a captura de video
        cap = cv2.VideoCapture(0)
        start_time = time.time()
        contFPS, fps, contImgCalibracao = 0, 0, 0
        # Matriz da Razao de Aspecto
        self.matrizRA = np.zeros((5, self.framesCalibragem))

        b = True
        while b:
            _, frame = cap.read()
            frameRedimencionado = imutils.resize(frame, width=357, height=273)
            # rgbImage = cv2.cvtColor(frameRedimencionado, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frameRedimencionado, cv2.COLOR_BGR2GRAY)

            retangulos = self.detector(gray, 0)

            # Verificar se há reconhecimento de pelo menos um rosto
            if len(retangulos) > 0:
                self.shape = self.verificarMaiorRetangulo(gray, retangulos)

                # Printa os landmark points do rosto
                # for (x, y) in self.shape:
                #     cv2.circle(rgbImage, (x, y), 2, (0, 0, 255), -1)

                # Aquisição de dados para calibrar
                if (contImgCalibracao < self.framesCalibragem):
                    if (contImgCalibracao == 0):
                        self.msgLog.emit(self.hora.currentTime().toString() + " - Aquisição  de dados para calibração")
                    if (contImgCalibracao == (self.framesCalibragem // 2) - 1):
                        self.judite.scriptRegulagemOlhosAbertos()
                        # contar
                        self.judite.scriptContagem()

                    self.matrizRA[0][contImgCalibracao] = self.analisePERCLOS.razaoDeAspecto(self.shape)
                    self.matrizRA[1][contImgCalibracao] = self.analisePERCLOS.desvioPadrao(contImgCalibracao,
                                                                                           self.matrizRA)
                    self.matrizRA[2][contImgCalibracao] = self.analisePERCLOS.erroPadrao(contImgCalibracao,
                                                                                         self.matrizRA)

                    self.matrizRA = self.preencherDadosDeTeste(contImgCalibracao, self.matrizRA)

                # Calibragem e plotagem dos dados de calibragem no gr�fico
                elif (contImgCalibracao == self.framesCalibragem):
                    self.judite.scriptFimCalibragem()
                    eixoX_graficoDeCalibragem = np.arange(self.framesCalibragem)
                    eixoX_graficoDeCalibragem = eixoX_graficoDeCalibragem.tolist()
                    self.matrizRA = self.analisePERCLOS.calibragemAberturaOlhos(self.matrizRA)
                    eixoY_graficoDeCalibragem = self.descreverDadosObtidosNoLog(self.matrizRA)

                    # Gerar gráfico de análise
                    grafico = pg.PlotWidget(title="GRÁFICO AQUISIÇÃO DE DADOS INICIAL PARA CALIBRAGEM")
                    grafico.setLabels(left="PERCLOS", bottom="Frames")
                    grafico.setXRange(0, len(eixoX_graficoDeCalibragem) - 1, padding=0)
                    grafico.getPlotItem().showGrid(True, True, 0.2)

                    grafico.plot(eixoX_graficoDeCalibragem, eixoY_graficoDeCalibragem, pen=pg.mkPen('b'))

                    self.plotarCalibragem.emit(grafico.getPlotItem())

                    self.preencherCampoDeTextoDeCalibragem()
                    arquivoCalibracao = ArquivoCalibracao()
                    arquivoCalibracao.gerarArquivoCalibracao(self.matrizRA[0], self.usuario)
                    b = False

                contImgCalibracao += 1

            # height, width, channel = rgbImage.shape
            # bytesPerLine = 3 * width
            # convertToQtFormat = QImage(rgbImage.data, width, height, bytesPerLine, QImage.Format_RGB888)
            # imagemDeExecucao = QPixmap.fromImage(convertToQtFormat)

            contFPS = contFPS + 1
            tempoDoLoop = int(time.time() - start_time)
            if tempoDoLoop > 1 and tempoDoLoop < 3:
                fps = tempoDoLoop / contFPS
                contFPS = 0
                start_time = time.time()

            # self.changePixmap.emit(imagemDeExecucao)
            self.contadorLoop.emit(str(fps))
        cap.release()
        cv2.destroyAllWindows()
        return

    def execucaoPERCLOS(self):
        # Habilitando a captura de video
        cap = cv2.VideoCapture(0)
        start_time = time.time()
        displayFPS = 1  # Atualiza o FPS a cada displayFPS segundo(s), A SER UTILIZADO COM FRAME_SKIP

        # contadores para frameSkip e janela de Baixo PERCLOS
        cont, janelaBaixoPERCLOS, contFPS = 0, 0, 0

        eixoX_graficoDeExecucao = 0

        while True:
            _, frame = cap.read()
            frameRedimencionado = imutils.resize(frame, width=357, height=273)
            # rgbImage = cv2.cvtColor(frameRedimencionado, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frameRedimencionado, cv2.COLOR_BGR2GRAY)

            # detectar o rosto
            retangulos = self.detector(gray, 0)

            # Verificar se há reconhecimento de pelo menos um rosto
            if len(retangulos) > 0:
                self.shape = self.verificarMaiorRetangulo(gray, retangulos)

                # Printa os landmark points do rosto
                # for (x, y) in self.shape:
                #     cv2.circle(rgbImage, (x, y), 2, (0, 0, 255), -1)

                threshold_porcento = self.threshold

                eixoY_graficoDeExecucao = ((self.analisePERCLOS.razaoDeAspecto(self.shape) - self.valorMinimo) / (
                        self.valorMaximo - self.valorMinimo) * 100)
                eixoX_graficoDeExecucao = eixoX_graficoDeExecucao + 1

                self.variaveisGrafico.emit([eixoX_graficoDeExecucao, eixoY_graficoDeExecucao,
                                            threshold_porcento])

                # Verificar e Alertar
                if (eixoY_graficoDeExecucao < self.threshold):
                    print("PERCLOS: " + str(eixoY_graficoDeExecucao))
                    janelaBaixoPERCLOS += 1
                    if (janelaBaixoPERCLOS > 15):

                        self.judite.scriptBeep()

                        if (janelaBaixoPERCLOS > 15 and janelaBaixoPERCLOS % 25 == 0):
                            self.judite.scriptAlerta()

                else:
                    janelaBaixoPERCLOS = 0

            # MOSTRA IMAGEM NO FRAME DO PROGRAMA
            # height, width, channel = rgbImage.shape
            # bytesPerLine = 3 * width
            # convertToQtFormat = QImage(rgbImage.data, width, height, bytesPerLine, QImage.Format_RGB888)
            # imagemDeExecucao = QPixmap.fromImage(convertToQtFormat)
            # self.changePixmap.emit(imagemDeExecucao)

            cont = cont + 1
            # função para contar FPS
            contFPS = contFPS + 1
            if (time.time() - start_time) > displayFPS:
                self.contadorLoop.emit(str(int(contFPS / (time.time() - start_time))))
                contFPS = 0
                start_time = time.time()
        cap.release()
        cv2.destroyAllWindows()

    def verificarMaiorRetangulo(self, imagemGray, retangulos):
        maiorRetangulo = 0

        for retangulo in retangulos:
            shape = self.predicao(imagemGray, retangulo)
            shape = face_utils.shape_to_np(shape)

            # Calcular a distancia do rosto pertinente ao retangulo em an�lise
            distHorizontalRosto = distance.euclidean((shape[0] + shape[1]) // 2, (shape[15] + shape[16]) // 2)
            distVerticalRosto = distance.euclidean((shape[0] + shape[16]) // 2, (shape[7] + shape[8] + shape[9]) // 3)

            if ((distHorizontalRosto * distVerticalRosto) > maiorRetangulo):
                maiorRetangulo = distHorizontalRosto * distVerticalRosto
                shapeMaior = shape
        return shapeMaior

    def preencherDadosDeTeste(self, indiceFrameCalibragem, matrizRA):
        matrizRA[4][indiceFrameCalibragem] = 70

        if (indiceFrameCalibragem < len(matrizRA[0])):
            matrizRA[3][indiceFrameCalibragem] = 0
        else:
            matrizRA[3][indiceFrameCalibragem] = 1

        return matrizRA

    def descreverDadosObtidosNoLog(self, matrizRA):
        dadosNoEixoY = []
        for i in range(len(matrizRA[0])):
            if (i == 0):
                self.msgLog.emit("Razão de Aspecto; Desvio Padrão; Erro Padrão")
            dadosNoEixoY.append(matrizRA[0][i])
            msg = (str(round(matrizRA[0][i], 5)) + "; " +
                   str(round(matrizRA[1][i], 5)) + "; " +
                   str(round(matrizRA[2][i], 5)) + "; ")
            self.msgLog.emit(msg)
        self.msgLog.emit(self.hora.currentTime().toString() + " - Calibração Finalizada")
        return dadosNoEixoY

    def gerarArquivoDeDados(self, matrizRA):
        print(str(matrizRA))
        arrayDados = self.matrizRA.tolist()
        print(str(arrayDados))
        arquivo = GerarArquivoDeDados()
        arquivo.gerarCSV(arrayDados)

    def preencherCampoDeTextoDeCalibragem(self):
        self.valorMaxPERCLOS.emit(str(round(self.matrizRA[0].max(), 3)))
        self.valorMinPERCLOS.emit(str(round(self.matrizRA[0].min(), 3)))
        valorRAdoThreshold = ((self.matrizRA[0].max() - self.matrizRA[0].min()) * (self.threshold / 100)) + \
                             self.matrizRA[0].min()
        self.PThreshold.emit(str(round(valorRAdoThreshold, 3)))