# -*- coding: utf-8 -*-
'''
Created on 16 de jun de 2018

@author: almer
'''
from PyQt5.Qt import QTime, QThread, pyqtSignal

class Horario(QThread):
    horarioEmTempoReal = pyqtSignal(str)
    startTelaDeLog = pyqtSignal(str)
    
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        
    def run(self):
        time = QTime()
        hora = time.currentTime().toString()
        self.startTelaDeLog.emit(hora + " - Inicialização do Sistema")
        while True:
            hora = time.currentTime().toString()
            self.horarioEmTempoReal.emit(hora)