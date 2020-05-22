import time
from playsound import playsound

class MensagemFalada(object):
    '''
    classdocs
    '''

    def scriptInicial(self):
        playsound("Mensagens Faladas/Inicializando-sistema-de-audio.mp3")
        time.sleep(1)
        playsound("Mensagens Faladas/boas-vindas.mp3")
        time.sleep(1)
        playsound("Mensagens Faladas/auxilio-calibracao.mp3")
        time.sleep(1)
        playsound("Mensagens Faladas/auxilio-calibracao-olhos-fechados.mp3")
        time.sleep(4)
        self.scriptContagem()
    
    def scriptContagem(self):
        playsound("Mensagens Faladas/contar-um.mp3")
        time.sleep(1)
        playsound("Mensagens Faladas/contar-dois.mp3")
        time.sleep(1)
        playsound("Mensagens Faladas/contar-tres.mp3")
        time.sleep(1)
        
    def scriptRegulagemOlhosAbertos(self):
        playsound("Mensagens Faladas/ok-auxilio-calibracao-olhos-abertos.mp3")
        time.sleep(2)
        self.scriptContagem()
    
    def scriptFimCalibragem(self):
        playsound("Mensagens Faladas/ok.mp3")
        
    def scriptIniciarExecucao(self):
        playsound("Mensagens Faladas/iniciar-viagem.mp3")
    
    def scriptAlerta(self):
        playsound("Mensagens Faladas/alerta.mp3")
        time.sleep(6)

    def scriptBeep(self):
        playsound("Beep/beep.mp3")
        time.sleep(0.3)