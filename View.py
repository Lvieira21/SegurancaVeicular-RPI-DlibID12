# -*- coding: utf-8 -*-
'''
Created on 16 de jun de 2018
Edited on 12/05/2020

@author: Almerindo
@Edit by: Lucas Vieira
'''
from random import randint

from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import QWidget, QTime, QInputDialog
import pyqtgraph as pg
from DesempenhoProcessador import DesempenhoProcessador
from Horario import Horario
from CalibraExecutaPERCLOS import CalibraExecutaPERCLOS


class Ui_MainWindow(QWidget):

    def setupUi(self, MainWindow):
        self.showFullScreen()
        self.setHidden(True)

        MainWindow.setObjectName("Segurança Veicular")
        MainWindow.setEnabled(True)
        MainWindow.resize(self.size())
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidgetLog = QtWidgets.QGroupBox(self.centralwidget)
        self.verticalLayoutWidgetLog.setTitle("Tela de Log")
        self.verticalLayoutWidgetLog.setGeometry(QtCore.QRect(920, 10, 435, 289))
        self.verticalLayoutWidgetLog.setObjectName("verticalLayoutLog")
        self.verticalLayoutWidgetLog.setWindowTitle("LOG")

        self.verticalLayoutLog = QtWidgets.QVBoxLayout(self.verticalLayoutWidgetLog)
        self.verticalLayoutLog.setContentsMargins(2, 2, 2, 2)
        self.verticalLayoutLog.setObjectName("verticalLayoutLog")

        self.txtLog = QtWidgets.QPlainTextEdit(self.verticalLayoutWidgetLog)
        self.txtLog.setWindowTitle("Log")
        self.txtLog.setReadOnly(True)
        self.verticalLayoutLog.addWidget(self.txtLog)

        self.verticalLayoutWidgetCamera = QtWidgets.QGroupBox(self.centralwidget)
        self.verticalLayoutWidgetCamera.setTitle("Câmera")
        self.verticalLayoutWidgetCamera.setGeometry(QtCore.QRect(550, 10, 361, 289))
        self.verticalLayoutWidgetCamera.setObjectName("verticalLayoutWidgetCamera")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidgetCamera)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self.verticalLayoutWidgetCamera)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.horizontalLayoutWidget = QtWidgets.QGroupBox(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 304, 1345, 241))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.horizontalLayoutWidget.setLayout(self.horizontalLayout)

        pg.setConfigOption("background", "w")
        pg.setConfigOption("foreground", "k")

        self.graficoMicro = pg.PlotWidget(self.horizontalLayoutWidget, title="GRÁFICO EM REAL TIME - PERCLOS ANÁLISE")
        self.graficoMicro.setXRange(0, 1000, padding=0)
        self.graficoMicro.setYRange(0, 100, padding=0)
        self.graficoMicro.getPlotItem().showGrid(True, True, 0.2)
        self.x = [0]
        self.y = [0]
        self.t = [0]
        self.dados = self.graficoMicro.plot(self.x, self.y, pen=pg.mkPen('b'))
        self.threshold = self.graficoMicro.plot(self.x, self.t, pen=pg.mkPen('r', style=QtCore.Qt.DashLine))
        self.horizontalLayout.addWidget(self.graficoMicro)

        self.horizontalLayoutWidget_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 550, 1345, 150))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.graficoMacro = pg.PlotWidget(self.horizontalLayoutWidget,
                                          title="GRÁFICO AQUISIÇÃO DE DADOS INICIAL PARA CALIBRAGEM")
        self.graficoMacro.setLabels(left="PERCLOS", bottom="Frames")
        self.graficoMacro.setXRange(0, 20, padding=0)
        self.graficoMacro.setYRange(0, 1, padding=0)
        self.graficoMacro.getPlotItem().showGrid(True, True, 0.2)
        self.horizontalLayout_2.addWidget(self.graficoMacro)

        self.horizontalLayoutWidget_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 531, 41))
        self.horizontalLayoutWidget_3.setTitle("Estado do Sistema")
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")

        self.layoutParteSuperior = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.layoutParteSuperior.setContentsMargins(2, 2, 2, 2)
        self.layoutParteSuperior.setObjectName("layoutParteSuperior")

        ##----------FPS----------##
        self.lbFPS = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.lbFPS.setText("FPS")

        self.lcdFPS = QtWidgets.QLCDNumber(self.horizontalLayoutWidget_3)
        self.lcdFPS.setObjectName("lcdFPS")

        ##----------Marcador de Tempo----------##
        self.lbTempo = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.lbTempo.setText("Tempo")

        self.timeEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.timeEdit.setObjectName("timeEdit")

        hora = QTime()
        self.timeEdit.setText(hora.currentTime().toString())

        ##----------Marcador da Ultima Parada----------##
        self.lbProcessoCPU = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.lbProcessoCPU.setText("CPU: ")

        self.txtProcessoCPU = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.txtProcessoCPU.setObjectName("txtProcessoCPU")

        # Layout da parte superior
        self.layoutParteSuperior.addWidget(self.lbFPS)
        self.layoutParteSuperior.addWidget(self.lcdFPS)
        self.layoutParteSuperior.addWidget(self.lbTempo)
        self.layoutParteSuperior.addWidget(self.timeEdit)
        self.layoutParteSuperior.addWidget(self.lbProcessoCPU)
        self.layoutParteSuperior.addWidget(self.txtProcessoCPU)

        # ---------- Layout de Análise PERCLOS ----------
        self.layoutPERCLOS = QtWidgets.QGroupBox(self.centralwidget)
        self.layoutPERCLOS.setGeometry(QtCore.QRect(375, 55, 166, 93))
        self.layoutPERCLOS.setObjectName("layoutPERCLOS")
        self.layoutPERCLOS.setTitle("Resumo de Calib. PERCLOS (RA)")

        self.formLayout = QtWidgets.QFormLayout(self.layoutPERCLOS)
        self.formLayout.setContentsMargins(2, 2, 2, 2)
        self.formLayout.setObjectName("formLayout")

        self.lbValorMaxPERCLOS = QtWidgets.QLabel(self.layoutPERCLOS)
        self.lbValorMaxPERCLOS.setObjectName("lbValorMaxPERCLOS")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lbValorMaxPERCLOS)

        self.lbValorMinPERCLOS = QtWidgets.QLabel(self.layoutPERCLOS)
        self.lbValorMinPERCLOS.setObjectName("lbValorMinPERCLOS")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbValorMinPERCLOS)

        self.lbP70 = QtWidgets.QLabel(self.layoutPERCLOS)
        self.lbP70.setObjectName("lbP70")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lbP70)

        self.txtValorMaxPERCLOS = QtWidgets.QLineEdit(self.layoutPERCLOS)
        self.txtValorMaxPERCLOS.setObjectName("txtValorMaxPERCLOS")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtValorMaxPERCLOS)

        self.txtValorMinPERCLOS = QtWidgets.QLineEdit(self.layoutPERCLOS)
        self.txtValorMinPERCLOS.setObjectName("txtValorMinPERCLOS")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtValorMinPERCLOS)

        self.txtP70 = QtWidgets.QLineEdit(self.layoutPERCLOS)
        self.txtP70.setObjectName("txtP70")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txtP70)

        # ---------- Layout de Análise Estatisticas do PERCLOS ----------
        self.layoutEstatisticaPERCLOS = QtWidgets.QGroupBox(self.centralwidget)
        self.layoutEstatisticaPERCLOS.setGeometry(QtCore.QRect(375, 152, 166, 147))
        self.layoutEstatisticaPERCLOS.setObjectName("layoutEstatisticaPERCLOS")
        self.layoutEstatisticaPERCLOS.setTitle("Estatistica PERCLOS")

        self.gridLayoutPiscada_3 = QtWidgets.QGridLayout(self.layoutEstatisticaPERCLOS)
        self.gridLayoutPiscada_3.setContentsMargins(2, 2, 2, 2)
        self.gridLayoutPiscada_3.setObjectName("gridLayoutPiscada_3")

        self.lbBaixoPerclosMedia = QtWidgets.QLabel(self.layoutEstatisticaPERCLOS)
        self.lbBaixoPerclosMedia.setObjectName("lbBaixoPerclosMedia")
        self.gridLayoutPiscada_3.addWidget(self.lbBaixoPerclosMedia, 2, 0, 1, 1)

        self.txtBaixoPerclosMedia = QtWidgets.QLineEdit(self.layoutEstatisticaPERCLOS)
        self.txtBaixoPerclosMedia.setObjectName("txtBaixoPerclosMedia")
        self.gridLayoutPiscada_3.addWidget(self.txtBaixoPerclosMedia, 2, 1, 1, 1)

        self.txtAltoPerclos = QtWidgets.QLineEdit(self.layoutEstatisticaPERCLOS)
        self.txtAltoPerclos.setObjectName("txtAltoPerclos")
        self.gridLayoutPiscada_3.addWidget(self.txtAltoPerclos, 3, 1, 1, 1)

        self.txtBaixoPerclos = QtWidgets.QLineEdit(self.layoutEstatisticaPERCLOS)
        self.txtBaixoPerclos.setObjectName("txtBaixoPerclos")
        self.gridLayoutPiscada_3.addWidget(self.txtBaixoPerclos, 1, 1, 1, 1)

        self.lbAltoPerclos = QtWidgets.QLabel(self.layoutEstatisticaPERCLOS)
        self.lbAltoPerclos.setObjectName("lbAltoPerclos")
        self.gridLayoutPiscada_3.addWidget(self.lbAltoPerclos, 3, 0, 1, 1)

        self.lbPorMinutoResumoPerclos = QtWidgets.QLabel(self.layoutEstatisticaPERCLOS)
        self.lbPorMinutoResumoPerclos.setObjectName("lbPorMinutoResumoPerclos")
        self.gridLayoutPiscada_3.addWidget(self.lbPorMinutoResumoPerclos, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)

        self.lbBaixoPerclos = QtWidgets.QLabel(self.layoutEstatisticaPERCLOS)
        self.lbBaixoPerclos.setObjectName("lbBaixoPerclos")
        self.gridLayoutPiscada_3.addWidget(self.lbBaixoPerclos, 1, 0, 1, 1)

        self.lbAltoPerclosMedia = QtWidgets.QLabel(self.layoutEstatisticaPERCLOS)
        self.lbAltoPerclosMedia.setObjectName("lbAltoPerclosMedia")
        self.gridLayoutPiscada_3.addWidget(self.lbAltoPerclosMedia, 4, 0, 1, 1)

        self.txtAltoPerclosMedia = QtWidgets.QLineEdit(self.layoutEstatisticaPERCLOS)
        self.txtAltoPerclosMedia.setObjectName("txtAltoPerclosMedia")
        self.gridLayoutPiscada_3.addWidget(self.txtAltoPerclosMedia, 4, 1, 1, 1)

        thCPU = DesempenhoProcessador(self)
        thCPU.desempenhoCPU.connect(self.txtProcessoCPU.setText)
        thCPU.start()

        thHora = Horario(self)
        thHora.horarioEmTempoReal.connect(self.timeEdit.setText)
        thHora.startTelaDeLog.connect(self.txtLog.setPlainText)
        thHora.start()

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Timer gráfico em tempo real
        # self.timer = QtCore.QTimer()
        # self.timer.setInterval(50)
        # self.timer.timeout.connect(self.update_plot_data)
        # self.timer.start()

    def executarPERCLOS(self):
        boasVindas = BoasVindas()
        self.usuario = boasVindas.getNome()

        self.perclos = CalibraExecutaPERCLOS(self, self.usuario)
        self.perclos.changePixmap.connect(self.label.setPixmap)
        self.perclos.contadorLoop.connect(self.lcdFPS.display)
        self.perclos.plotarCalibragem.connect(self.graficoMacro.setCentralWidget)
        self.perclos.variaveisGrafico.connect(self.update_plot_data)
        self.perclos.valorMaxPERCLOS.connect(self.txtValorMaxPERCLOS.setText)
        self.perclos.valorMinPERCLOS.connect(self.txtValorMinPERCLOS.setText)
        self.perclos.PThreshold.connect(self.txtP70.setText)
        self.perclos.msgLog.connect(self.txtLog.appendPlainText)

        self.perclos.start()

    def update_plot_data(self, l):
        # print("Primeiro item {} - Segundo item {} - Terceiro item {}".format(l[0], l[1], l[2]))
        if (len(self.x) >= 1000):
            self.x = self.x[1:]  # Remove the first x element.
            self.y = self.y[1:]  # Remove the first y
            self.t = self.t[1:]  # Remove the first t

        self.x.append(l[0])
        self.y.append(l[1])  # Add a new random value.
        self.t.append(l[2])

        self.dados.setData(self.x, self.y)
        self.threshold.setData(self.x, self.t)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Segurança Veicular TCC"))

        self.lbValorMaxPERCLOS.setText("Valor Máx.")
        self.lbValorMinPERCLOS.setText("Valor Mín.")
        self.lbP70.setText("P70")
        self.lbBaixoPerclosMedia.setText("B. PERCLOS Med.")
        self.lbAltoPerclos.setText("Alto PERCLOS")
        self.lbPorMinutoResumoPerclos.setText("por min.")
        self.lbBaixoPerclos.setText("Baixo PERCLOS")
        self.lbAltoPerclosMedia.setText("A. PERCLOS Med.")


class BoasVindas(QWidget):
    def __init__(self):
        super(BoasVindas, self).__init__()
        self.horario = QTime()

    def getNome(self):
        msg, ok = QInputDialog.getText(self, 'Bem Vindo!', 'Qual é seu nome?')

        if ok:
            return msg
        else:
            self.getNome()
            return
