import win32gui
import win32con
import subprocess
import class.openAppSecondScreen as openAppSecondScreen
import speedtest

""

# Funcion to open the app
def test():
    # Cria um objeto Speedtest
    teste_velocidade = speedtest.Speedtest()

    # Executa o teste de velocidade
    print("Testando a velocidade de download...")
    velocidade_download = teste_velocidade.download() / 10**6  # Converter para megabits por segundo
    print("Velocidade de download: %.2f Mbps" % velocidade_download)

    print("Testando a velocidade de upload...")
    velocidade_upload = teste_velocidade.upload() / 10**6  # Converter para megabits por segundo
    print("Velocidade de upload: %.2f Mbps" % velocidade_upload)

    print("Testando o ping...")
    ping = teste_velocidade.results.ping
    print("Ping: %.2f ms" % ping)