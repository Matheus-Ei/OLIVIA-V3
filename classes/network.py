import win32gui
import win32con
import subprocess
import classes.openAppSecondScreen as openAppSecondScreen
import speedtest


# Funcion to open the app
def pingg(teste_velocidade):
    print("Testando o ping...")
    ping = teste_velocidade.results.ping
    ping = ("Ping: %.2f ms" % ping)

    return ping

# Funcion to open the app
def velocidade_downloadd(teste_velocidade):
    # Executa o teste de velocidade
    print("Testando a velocidade de download...")
    velocidade_download = teste_velocidade.download() / 10**6  # Converter para megabits por segundo
    velocidade_download = ("Velocidade de download: %.2f Mbps" % velocidade_download)

    return velocidade_download


# Funcion to open the app
def velocidade_uploadd(teste_velocidade):

    print("Testando a velocidade de upload...")
    velocidade_upload = teste_velocidade.upload() / 10**6  # Converter para megabits por segundo
    velocidade_upload = ("Velocidade de upload: %.2f Mbps" % velocidade_upload)

    return velocidade_upload