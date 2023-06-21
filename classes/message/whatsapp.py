import pywhatkit as kit
import time
import pyautogui
import pygetwindow as gw

def sendMessage(number, message):
    country_code = "+55"
    print("Enviando Mensagem...")
    kit.sendwhatmsg_instantly(f"{country_code}{number}", message, wait_time=5)
    
    time.sleep(1)  # Atraso para dar tempo de o WhatsApp abrir e a mensagem ser digitada

    janela = gw.getWindowsWithTitle("Opera")[0]
    # Traga a janela para frente (opcional)
    janela.activate()

    time.sleep(1)  # Atraso para dar tempo de o WhatsApp abrir e a mensagem ser digitada

    pyautogui.press('enter')

    time.sleep(1)

    pyautogui.hotkey('ctrl', 'w')
    print("<<Mensagem Enviada com Sussesso>>")

#sendMessage("63 9985-0556", "Olá, Isso é um teste")



