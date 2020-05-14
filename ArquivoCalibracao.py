import csv

class ArquivoCalibracao(object):
    
    def __init__(self):
        super(ArquivoCalibracao, self).__init__()
        
    def gerarArquivoCalibracao(self, dados, nome):
        c = csv.writer(open('Calibragem.csv', 'w'))
        c.writerow([dados.max(), dados.min(), nome])
        
    def abrirArquivoCalibracao(self):
        with open('Calibragem.csv', 'r') as file:
            c = csv.reader(file, delimiter=',')
            for linha in c:
                max, min, nome = linha
                return float(max), float(min), str(nome)
