import pygetwindow as gw
import subprocess
import time

def openApp(caminho, nome):
    posicao_x = 1920
    posicao_y = 10

    # Execute o comando para abrir o aplicativo
    subprocess.Popen(caminho)

    # Aguarde um pequeno intervalo para garantir que o aplicativo tenha tempo para abrir
    time.sleep(1)
    
    try:
        janela = gw.getWindowsWithTitle(nome)[0]

        # Unmaximize the window
        janela.restore()

        # Defina a posição da janela
        janela.moveTo(posicao_x, posicao_y)

        # Maximize a janela (opcional)
        janela.maximize()
        # Traga a janela para frente (opcional)
        janela.activate()

    except  IndexError:
        print("--> Aplicativo " + nome + " Não encontrado <--")




