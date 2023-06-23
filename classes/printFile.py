from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pyautogui

def imprimir_arquivo(arquivo):
    # Configurar as opções do Firefox
    options = Options()
    options.add_argument('--kiosk')

    # Inicializar o driver do Firefox
    driver = webdriver.Firefox(options=options)

    # Abrir o arquivo PDF no navegador
    driver.get(f'file:///{arquivo}')

    time.sleep(0.5)  # Atraso para dar tempo
    pyautogui.click()

    time.sleep(0.5)  # Atraso para dar tempo
    pyautogui.hotkey("ctrl", "p")

    time.sleep(0.5)  # Atraso para dar tempo
    pyautogui.press('enter')

    time.sleep(0.5)

    print("<<Impressão Bem Sussedida>>")

    # Fechar o navegador
    driver.quit()

# Chamada da função para imprimir um arquivo PDF
#imprimir_arquivo(r"C:\Users\t4iga\Downloads\Aula 1.pdf")
