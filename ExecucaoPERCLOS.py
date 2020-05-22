import cv2, dlib, time
import imutils
from imutils import face_utils
from imutils.video.pivideostream import PiVideoStream

from AnalisePERCLOS import AnalisePERCLOS
from ArquivoCalibracao import ArquivoCalibracao
from MensagemFalada import MensagemFalada

class ExecucaoPERCLOS(object):

    def __init__(self):
        super(ExecucaoPERCLOS, self).__init__()
        self.arq_predicao = "IA/shape_predictor_ID12_37fl_cfbo_pyis.dat"
        self.detectorCv = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.detector = dlib.get_frontal_face_detector()
        self.predicao = dlib.shape_predictor(self.arq_predicao)
        self.threshold = 70

        self.judite = MensagemFalada()
        self.analisePERCLOS = AnalisePERCLOS()
        arquivoCalibracao = ArquivoCalibracao()
        self.valorMaximo, self.valorMinimo, self.nome = arquivoCalibracao.abrirArquivoCalibracao()
        self.usuario = "" # Por ser um dispositivo plug and play,
        self.display = False


    def execucaoPERCLOS(self):

        # Habilitando a captura de video
        cap = PiVideoStream().start()
        self.judite.scriptIniciarExecucao()
        time.sleep(2.0)
        start_time = time.time()
        displayFPS = 1  # Atualiza o FPS mostrado a cada segundo(s) setado na variavel.

        # contadores para frameSkip e janela de Baixo PERCLOS
        cont, janelaBaixoPERCLOS, contFPS = 0, 0, 0

        while True:
            frame = cap.read()
            frameRedimencionado = imutils.resize(frame, width=400)
            rgbImage = cv2.cvtColor(frameRedimencionado, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frameRedimencionado, cv2.COLOR_BGR2GRAY)

            # detectar o rosto
            retangulos = self.detectorCv.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

            for (x, y, w, h) in retangulos:

                retangulo = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))

                self.shape = self.predicao(gray, retangulo)
                self.shape = face_utils.shape_to_np(self.shape)

                # Printa os landmark points do rosto
#                 for (x, y) in self.shape:
#                     cv2.circle(rgbImage, (x, y), 1, (0, 0, 255), -1)

                limitePercentualAbertura = self.threshold

                aberturaPerclos = ((self.analisePERCLOS.razaoDeAspecto(self.shape) - self.valorMinimo) / (
                        self.valorMaximo - self.valorMinimo) * 100)

                # Verificar e Alertar
                if (aberturaPerclos < limitePercentualAbertura):
                    print("PERCLOS: " + str(aberturaPerclos))
                    janelaBaixoPERCLOS += 1
                    if (janelaBaixoPERCLOS > 15):

                        self.judite.scriptBeep()

                        if (janelaBaixoPERCLOS > 15 and janelaBaixoPERCLOS % 25 == 0):
                            self.judite.scriptAlerta()

                else:
                    janelaBaixoPERCLOS = 0

            cont = cont + 1
            # função para contar FPS
            contFPS = contFPS + 1
            if (time.time() - start_time) > displayFPS:
                fps = int(contFPS / (time.time() - start_time))
                print(fps)
#                 cv2.putText(frameRedimencionado, "FPS: {}".format(fps), (10, 30),
#                             cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
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