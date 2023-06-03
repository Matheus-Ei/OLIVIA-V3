import win32gui
import win32con
import subprocess

def app_na_frente(app_title):
    # Encontre o identificador da janela do aplicativo pelo título
    app_window = win32gui.FindWindow(None, app_title)
    print(app_window)

    if app_window:
        try:
            # Defina o aplicativo como a janela ativa
            win32gui.SetForegroundWindow(app_window)

            # Defina a janela do aplicativo como "topmost" (acima das outras janelas)
            win32gui.SetWindowPos(app_window, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

            # Opcionalmente, restaure a janela (caso esteja minimizada)
            win32gui.ShowWindow(app_window, win32con.SW_RESTORE)
        except TypeError:
            print("#####@Erro de Tipo@#####")
        #except win32gui.SetForegroundWindow:
            #print('#####@Erro da SetForegroundWindow@#####')

    else:
        print("Aplicativo não encontrado")


def abrir_app(atalho):
    # Dicionário com os atalhos e caminhos dos aplicativos
    aplicativos = {
        'calculadora': 'C:\\Windows\\System32\\calc.exe',
        'bloco de notas': 'C:\\Windows\\System32\\notepad.exe',
        'explorador de arquivos': 'C:\\Windows\\explorer.exe',
        'ópera': 'C:\\Users\\t4iga\\AppData\\Local\\Programs\\Opera\\launcher.exe',
        'navegador': 'C:\\Users\\t4iga\\AppData\\Local\\Programs\\Opera\\launcher.exe',
        'canva': 'C:\\Users\\t4iga\\AppData\\Local\\Programs\\Canva\\Canva.exe',
    }
    # Função para abrir um aplicativo a partir de um atalho
    def abrir_aplicativo(atalho):
        if atalho in aplicativos:
            caminho = aplicativos[atalho]
            subprocess.Popen(caminho)
            print(f"Aplicativo '{atalho}' aberto.")
        else:
            print(f"Atalho '{atalho}' não encontrado.")

    abrir_aplicativo(atalho)