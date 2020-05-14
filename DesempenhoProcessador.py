import psutil
from PyQt5.Qt import QThread, pyqtSignal


class DesempenhoProcessador(QThread):
    desempenhoCPU = pyqtSignal(str)
    
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
    
    def run(self):
        while True:
            self.lerDesempenhoCPU()

    def lerDesempenhoCPU(self):
        cpu = psutil.cpu_percent(interval=1)
        self.desempenhoCPU.emit(str(cpu) + " %")
