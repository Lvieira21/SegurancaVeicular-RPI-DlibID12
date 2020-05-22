# -*- coding: utf-8 -*-
'''
Created on 21 de mai de 2020

@author: Lucas
'''
from CalibracaoPERCLOS import CalibracaoPERCLOS
from ExecucaoPERCLOS import ExecucaoPERCLOS

perclosCalib = CalibracaoPERCLOS()
perclosExec = ExecucaoPERCLOS()

if __name__ == "__main__":

    perclosCalib.calibraPerclos()
    perclosExec.execucaoPERCLOS()
