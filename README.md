## DISPOSITIVO DE SEGURANÇA VEICULAR COM LEITURA DE EXPRESSÃO FACIAL PARA PREVENÇÃO DE ACIDENTES POR SONO AO VOLANTE

Este repositório é um fork do projeto original de dispositivo de segurança feito por Almerindo Abreu, Raphael Marques e como Orientador, o DSc Irineu Neto.
Este projeto visa a continuação deste projeto original, tentando tratar as questões de desempenho no Raspberry Pi por meio de tratamento de código e mudança de inteligencia artificial. 

[Pesquisa Acadêmica - Faculdade Salesiana Maria Auxiliadora](http://www.fsma.edu.br/site/projetos/prototipacao-de-um-sistema-de-seguranca-veicular-para-alertas-contra-o-sono-e-cansaco-via-reconhecimento-de-imagens/)


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
|gTTS 2.1.1|pip install gtts|[Link](http://pyqt.sourceforge.net/Docs/PyQt5/)|
| PyGame 1.9.6 | pip install pygame | [Link](https://www.pygame.org/docs/)|
| DLIB 19.7.0 | pip install dlib | [Link](http://dlib.net/)|
| OpenCV 4.2.0 | pip install opencv2 | [Link](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html)|
| Imutils 0.5.3 | pip install imutils | [Link](https://github.com/jrosebr1/imutils)|
| psutil 5.6.7 | pip install psutil | [Link](https://psutil.readthedocs.io/en/latest/)|
| NumPy 1.18.1 | pip install numpy | [Link](http://www.numpy.org/)|
