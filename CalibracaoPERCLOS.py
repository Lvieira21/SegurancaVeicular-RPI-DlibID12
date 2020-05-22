import cv2
import dlib
import imutils
import numpy as np
import time
from imutils import face_utils
from imutils.video.pivideostream import PiVideoStream

from AnalisePERCLOS import AnalisePERCLOS
from ArquivoCalibracao import ArquivoCalibracao
from MensagemFalada import MensagemFalada


class CalibracaoPERCLOS(object):

    def __init__(self):
        super(CalibracaoPERCLOS, self).__init__()
        self.arq_predicao = "IA/shape_predictor_ID12_37fl_cfbo_pyis.dat"
        self.detectorCv = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.detector = dlib.get_frontal_face_detector()
        self.predicao = dlib.shape_predictor(self.arq_predicao)

        self.judite = MensagemFalada()
        self.analisePERCLOS = AnalisePERCLOS()
        arquivoCalibracao = ArquivoCalibracao()
        self.valorMaximo, self.valorMinimo, self.nome = arquivoCalibracao.abrirArquivoCalibracao()
        self.framesCalibragem = 100
        self.usuario = ""
        self.display = False

    def calibraPerclos(self):

        self.judite.scriptInicial()
        # Habilitando a captura de video
        cap = PiVideoStream().start()
        time.sleep(2.0)
        start_time = time.time()
        contImgCalibracao, contFPS = 0, 0
        # Matriz da Razao de Aspecto
        self.matrizRA = np.zeros((5, self.framesCalibragem))
        displayFPS = 1  # Atualiza o FPS mostrado a cada segundo(s) setado na variavel.

        b = True
        while b:
            frame = cap.read()
            frameRedimencionado = imutils.resize(frame, width=400)
            rgbImage = cv2.cvtColor(frameRedimencionado, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frameRedimencionado, cv2.COLOR_BGR2GRAY)
            
            
            retangulos = self.detectorCv.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
            
            for (x, y, w, h) in retangulos:
                
                retangulo = dlib.rectangle(int(x), int(y), int(x+w), int(y+h))
                
                self.shape = self.predicao(gray, retangulo)
                self.shape = face_utils.shape_to_np(self.shape)

                # Aquisição de dados para calibrar
                if (contImgCalibracao < self.framesCalibragem):

                    if (contImgCalibracao == 0):
                        print(
                            str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min) + ":" + str(
                                time.localtime().tm_sec) + " - Aquisição de dados para calibração")

                    if (contImgCalibracao == (self.framesCalibragem // 2) - 1):
                        self.judite.scriptRegulagemOlhosAbertos()

                    self.matrizRA[0][contImgCalibracao] = self.analisePERCLOS.razaoDeAspecto(self.shape)
                    self.matrizRA[1][contImgCalibracao] = self.analisePERCLOS.desvioPadrao(contImgCalibracao,
                                                                                           self.matrizRA)
                    self.matrizRA[2][contImgCalibracao] = self.analisePERCLOS.erroPadrao(contImgCalibracao,
                                                                                         self.matrizRA)

                    self.matrizRA = self.preencherDadosDeTeste(contImgCalibracao, self.matrizRA)

                # Calibragem e plotagem dos dados de calibragem no gr�fico
                elif (contImgCalibracao == self.framesCalibragem):
                    self.judite.scriptFimCalibragem()
                    self.matrizRA = self.analisePERCLOS.calibragemAberturaOlhos(self.matrizRA)

                    arquivoCalibracao = ArquivoCalibracao()
                    arquivoCalibracao.gerarArquivoCalibracao(self.matrizRA[0], self.usuario)
                    b = False

            contImgCalibracao += 1

            contFPS = contFPS + 1
            if (time.time() - start_time) > displayFPS:
                fps = int(contFPS / (time.time() - start_time))
                print("FPS: {}".format(fps))
                contFPS = 0
                start_time = time.time()

            # show the frame
            if (self.display):
                cv2.imshow("Calibracao", rgbImage)
                key = cv2.waitKey(1) & 0xFF

                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break

        cv2.destroyAllWindows()
        cap.stop()
        time.sleep(5)

    def gerarArquivoDeDados(self, matrizRA):
        arrayDados = matrizRA.tolist()
        arquivo = GerarArquivoDeDados()
        arquivo.gerarCSV(arrayDados)

    def preencherDadosDeTeste(self, indiceFrameCalibragem, matrizRA):
        matrizRA[4][indiceFrameCalibragem] = 70

        if (indiceFrameCalibragem < len(matrizRA[0])):
            matrizRA[3][indiceFrameCalibragem] = 0
        else:
            matrizRA[3][indiceFrameCalibragem] = 1

        return matrizRA
