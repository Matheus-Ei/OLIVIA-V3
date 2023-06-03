import win32gui
import win32con
import subprocess

def inFrontOff(app_title):
    # Find the called app
    app_window = win32gui.FindWindow(None, app_title)
    print(app_window)
    if app_window:
        try:
            win32gui.SetForegroundWindow(app_window)
            win32gui.SetWindowPos(app_window, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        except TypeError:
            print("#####@ TypeError @#####")
        except win32gui.SetForegroundWindow:
            print('#####@ SetForegroundWindow ERROR @#####')
    else:
        print("-> app not found <-")


def open(atalho):
    # Dicionary with the apps
    aplicativos = {
        'calculadora': 'C:\\Windows\\System32\\calc.exe',
        'bloco de notas': 'C:\\Windows\\System32\\notepad.exe',
        'explorador de arquivos': 'C:\\Windows\\explorer.exe',
        'ópera': 'C:\\Users\\t4iga\\AppData\\Local\\Programs\\Opera\\launcher.exe',
        'navegador': 'C:\\Users\\t4iga\\AppData\\Local\\Programs\\Opera\\launcher.exe',
        'canva': 'C:\\Users\\t4iga\\AppData\\Local\\Programs\\Canva\\Canva.exe',
    }
    # Funcion to open the app
    def abrir_aplicativo(atalho):
        if atalho in aplicativos:
            caminho = aplicativos[atalho]
            subprocess.Popen(caminho)
            print(f"App '{atalho}' has been opened")
        else:
            print(f"The app '{atalho}' not found")

    abrir_aplicativo(atalho)