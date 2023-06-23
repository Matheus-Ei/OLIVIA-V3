import pywhatkit as kit
import time
import pyautogui
import pygetwindow as gw

def sendMessage(number, message):
    country_code = "+55"
    print("Enviando Mensagem...")
    kit.sendwhatmsg_instantly(f"{country_code}{number}", message, wait_time=8)
    
    time.sleep(0.5)  # Atraso para dar tempo de o WhatsApp abrir e a mensagem ser digitada
    pyautogui.click()
    time.sleep(0.5)  # Atraso para dar tempo de o WhatsApp abrir e a mensagem ser digitada

    pyautogui.press('enter')

    time.sleep(0.5)

    pyautogui.hotkey('ctrl', 'w')
    print("<<Mensagem Enviada com Sussesso>>")



