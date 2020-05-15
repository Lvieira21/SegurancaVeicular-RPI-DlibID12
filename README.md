## DISPOSITIVO DE SEGURANÇA VEICULAR COM LEITURA DE EXPRESSÃO FACIAL PARA PREVENÇÃO DE ACIDENTES POR SONO AO VOLANTE

Este repositório é a continuação do meu fork do sistema de segurança veicular, com intuito de fazer uma portabilidade do sistema para rodar num sistema embarcado (Raspberry Pi)



### Objetivo do Projeto

O referido projeto visa elaborar um protótipo computacional capaz de gerar alertas contra o sono e cansaço ao volante, baseado em análise de imagens e técnicas de análise de dados. O sono é definido como um estado funcional, com comportamentos corporais característicos que afetam a mobilidade, caracterizado por baixo reflexo, muitas vezes associado ao cansaço e stress. Então, há reações singulares de expressões faciais ditas universais e determinantes para expressar o sono, o cansaço e o stress, que podem ser aplicadas em sistemas para a prevenção de acidentes automobilísticos. (Almerindo e Raphael)
Implementação de melhoria de algoritmo e troca de Inteligencia artificial de modo que performe melhor no raspberry Pi (Lucas Vieira).
Para maiores informações e códigos das redes neurais convolucionais e inteligencias artificiais criadas e treinadas para este projeto: [CNN para Detecção de pontos faciais](https://github.com/Lvieira21/LandmarkDetectionCNN) e [shape_predictor do dlib customizado](https://github.com/Lvieira21/shapepredictorSistemaSeguranca)

### Regras de Desenvolvimento do Protótipo

Para o referente código, foi utilizado Python v3.6.10 através do ambiente Anaconda, todos os pacotes e bibliotecas foram instalados no ambiente Anaconda. Um caderno de Jupyter foi criado para teste e utilização das bibliotecas do projeto.

Foram utilizadas as seguintes bibliotecas mencionadas na tabela a seguir:

|Biblioteca   |Instalação                            |Site / Documentação|
|----------------|-------------------------------|-----------------------------|
|PyQt 5.9.2|pip install pyqt5          |[Link](http://pyqt.sourceforge.net/Docs/PyQt5/)            |
|PyQTGraph 0.10.0          |pip install pyqtgraph            |[Link](http://www.pyqtgraph.org/)            |
| playsound 1.2.2 | pip install playsound | [Link](https://pypi.org/project/playsound/)|
| DLIB 19.7.0 | pip install dlib | [Link](http://dlib.net/)|
| OpenCV 4.2.0 | pip install opencv2 | [Link](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html)|
| imutils 0.5.3 | pip install imutils | [Link](https://github.com/jrosebr1/imutils)|
| psutil 5.6.7 | pip install psutil | [Link](https://psutil.readthedocs.io/en/latest/)|
| NumPy 1.18.1 | pip install numpy | [Link](http://www.numpy.org/)|
