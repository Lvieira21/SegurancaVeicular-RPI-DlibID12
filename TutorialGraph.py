from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
from random import randint


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.x = [0]  # time points
        self.y = [0]  # data points

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        if (len(self.x) >= 100):
            self.x = self.x[1:]  # Remove the first y element.
            self.y = self.y[1:]  # Remove the first
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y.append(randint(0, 100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
