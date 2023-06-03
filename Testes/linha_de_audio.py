import sys
import pyaudio
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush


def ola(janela):
    class AudioVisualizer(QMainWindow):
        def __init__(janela):
            super().__init__()

            # Configuração da janela principal
            janela.setWindowTitle("Visualizador de Áudio")

            # Configuração do PyAudio
            janela.audio = pyaudio.PyAudio()
            janela.stream = janela.audio.open(format=pyaudio.paInt16,
                                        channels=1,
                                        rate=44100,
                                        input=True,
                                        frames_per_buffer=1024,
                                        stream_callback=janela.audio_callback)

            janela.data = np.zeros(1024)

            # Configuração do QTimer para atualização periódica
            janela.timer = QTimer()
            janela.timer.timeout.connect(janela.update_visualization)
            janela.timer.start(50)  # Atualização a cada 50 ms

            # Configuração dos parâmetros de visualização
            janela.line_length = 400  # Comprimento da linha
            janela.smoothing_factor = 0.05  # Fator de suavização dos dados de áudio

        def audio_callback(janela, in_data, frame_count, time_info, status):
            # Converte os dados de áudio em um array numpy
            audio_data = np.frombuffer(in_data, dtype=np.int16)

            # Realiza algum processamento no áudio, se necessário
            # Aqui você pode aplicar algoritmos de processamento de áudio

            # Suaviza os dados de áudio aplicando uma média móvel
            janela.data = (1 - janela.smoothing_factor) * janela.data + janela.smoothing_factor * audio_data

            return None, pyaudio.paContinue

        def update_visualization(janela):
            # Atualiza a exibição gráfica
            janela.update()

        def paintEvent(janela, event):
            painter = QPainter(janela)
            painter.setRenderHint(QPainter.Antialiasing)

            # Define as propriedades da linha
            pen = QPen()
            pen.setColor(Qt.white)  # Define a cor da linha como branca
            pen.setWidth(3)
            painter.setPen(pen)

            # Calcula a posição y da linha com base nos dados de áudio
            height = janela.height()
            center = height / 2

            # Cria um QPainterPath para desenhar a linha contorcida
            path = QPainterPath()

            # Calcula a posição x inicial e o incremento para a linha contorcida
            increment = janela.line_length / len(janela.data)

            # Desenha a linha contorcida com base nos dados de áudio
            for i, audio_value in enumerate(janela.data):
                x = i * increment
                y = center + audio_value / 40  # Ajuste a sensibilidade aqui
                if i == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)

            # Desenha o QPainterPath na janela
            painter.drawPath(path)

            painter.end()


def audio_visualizer(app):
    ola(app)

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Janela com GIF Animado")
# Define a cor de fundo como preto
palette = window.palette()
palette.setColor(window.backgroundRole(), QColor(0, 0, 0))
window.setPalette(palette)
audio_visualizer(window)
window.show()
sys.exit(app.exec())