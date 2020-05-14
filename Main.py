# -*- coding: utf-8 -*-
'''
Created on 16 de jun de 2018

@author: almer
'''
from PyQt5 import QtWidgets
from View import Ui_MainWindow

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    MainWindow.move(200, 200)
    MainWindow.setFixedSize(1400, 720)
    MainWindow.setWindowTitle("Sistema de Seguranção Veicular")
    
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.executarPERCLOS()
    sys.exit(app.exec_())