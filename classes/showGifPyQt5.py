from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *


def mostrar_gif(window,caminho):
    # Mostra o GIF da imagem topografica
    imagem_topografica = QLabel(window)
    imagem_topografica.setScaledContents(True)
    imagem_topografica.setFixedSize(250, 350)
    imagem_topografica.setGeometry(1650, 50, 700, 700)
    movie_topo = QMovie(caminho)
    imagem_topografica.setMovie(movie_topo)
    movie_topo.start()