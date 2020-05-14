import csv

class GerarArquivoDeDados(object):
    
    def __init__(self):
        super(GerarArquivoDeDados, self).__init__()
        
    def gerarCSV(self, dados):
        c = csv.writer(open("DadosCalibragem.csv", "w"))
        print(str(dados))
        frame = 0
        for i in range(len(dados[0])):
            frame += 1
            c.writerow([frame, dados[0][i], dados[1][i], dados[2][i], dados[3][i], dados[4][i]])
