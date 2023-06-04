# Imports
import speech_recognition as sr
import threading
import pyodbc
import random
from datetime import datetime
import openai
import sys
import os
import time
import pyautogui
import webbrowser


# Libraris
import classes.appManagement as app
import classes.voice as voice
import classes.spotify as spotify
import database.database as db


# Pre-definitions
def timeGet():
    global hour, minutes, seconds, day, week, mounth, year
    time=datetime.now() 
    hour = int(time.strftime("%H"))
    minutes = int(time.strftime("%M"))
    seconds = time.strftime("%S")
    day = time.strftime("%d")
    week = time.strftime("%A")
    mounth = time.strftime("%B")
    year = time.strftime("%Y")

# Var pre-definitions
context = " "



# Main funcion to back-end
def code():
    # Globals
    global textAudio, response, context

    # Var pre-definitions
    context = " "

    # Creating the Speach Recognition and defines the openai key
    r = sr.Recognizer()

    # Loop to capture and recognize the sound of the microfone
    with sr.Microphone() as source:
        print("->starting audio adjustment<-")
        r.adjust_for_ambient_noise(source, duration=2) # Time to ajust the microfone recognition with the sound of the ambient
        print("->given fit<-")
        print("initialization...\n")
        while True:
            print("listening...\n")
            try:
                basicAudio = r.listen(source)
                textAudio=(r.recognize_google(basicAudio, language="pt-br"))
                textAudio = textAudio.lower() 
                print("recognizing...\n")
                print(textAudio + "\n")


                # Open a app
                if  db.question('abrir aplicativo', textAudio):
                    # Ask what app the user wants open
                    voice.speak("Qual aplicativo voce deseja abrir?")
                    try:
                        basicAudio = r.listen(source)
                        textAudio=(r.recognize_google(basicAudio, language='pt-br'))
                        app.open(textAudio) # Opening the app
                    except:
                        print("#####@ ERROR @#####")

                
                # Speak the time
                elif db.question('horas', textAudio):
                    global hour, minutes, seconds, day, week, mounth, year
                    timeGet()
                    response=("São %d e %d minutos" %(hour ,minutes))
                    voice.speak(response)


                # Ends the code
                elif db.question('desligamento', textAudio):
                    voice.speak(db.answer("desligamento")) 
                    sys.exit()


                # Code to execute comands in windows, like turn of or loggof
                elif db.question("desligar sistema", textAudio):
                    voice.speak(db.answer("desligar sistema"))
                    time.sleep(5)
                    os.system("shutdown /s /t 1")

                elif db.question("sair sistema", textAudio):
                    voice.speak(db.answer("sair sistema"))
                    time.sleep(5)
                    os.system("shutdown -l")

                elif db.question("reiniciar sistema", textAudio):
                    voice.speak(db.answer("reiniciar sistema"))
                    time.sleep(5)
                    os.system("shutdown /r /t 1")


                # Reseta a variavel contexto do chat-gpt
                elif db.question('mudar de assunto', textAudio):
                    context = "-"
                    voice.speak(db.answer("mudar de assunto")) 


                # PyAutoGUI freatures
                elif db.question("abrir gerenciador de tarefas", textAudio):
                    voice.speak(db.answer("abrir gerenciador de tarefas"))
                    pyautogui.hotkey("ctrl", "shift", "esc")

                elif db.question("visao geral das tarefas", textAudio):
                    voice.speak(db.answer("visao geral das tarefas"))
                    pyautogui.hotkey("winleft", "tab")

                elif db.question("nova area de trabalho", textAudio):
                    voice.speak(db.answer("nova area de trabalho"))
                    pyautogui.hotkey("ctrl", "winleft", "d")

                elif db.question("deletar area de trabalho", textAudio):
                    voice.speak(db.answer("deletar area de trabalho"))
                    pyautogui.hotkey("ctrl", "winleft", "f4")

                elif db.question("mover para a are de trabalho a esquerda", textAudio):
                    voice.speak(db.answer("mover para a are de trabalho a esquerda"))
                    pyautogui.hotkey("ctrl", "winleft", "left")

                elif db.question("mover para a are de trabalho a direita", textAudio):
                    voice.speak(db.answer("mover para a are de trabalho a direita"))
                    pyautogui.hotkey("ctrl", "winleft", "right")
                

                # Generate image with openai
                elif db.question('modo geracao de imagem', textAudio):
                    openai.api_key = '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'
                    voice.speak("Descreva a imagem que você deseja Gerar")
                    try:
                        basicAudio = r.listen(source)
                        textAudio=(r.recognize_google(basicAudio, language='pt-br'))

                        response = openai.Image.create(
                        prompt = "Imagem com o estilo cartoon realista e meio aquarela e criativa sobre: " + textAudio,
                        n=1,
                        size="1024x1024"
                        )
                        image_url = response['data'][0]['url']
                        print(image_url)
                        # Open the image in navegator
                        retorno = "Abrindo a Imagem Gerada"
                        voice.speak(retorno)
                        webbrowser.open(image_url)
                    except:
                        print("#####@ ERROR @#####")
                    voice.speak("Gerando Imagem")



                # Sends all the "elses" to chat-gpt
                else:
                    try:
                        openai.api_key = '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'
                        enter = context + "\n" + textAudio + "\n"
                        responseOpenai = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content":enter}
                            ],
                            max_tokens=200
                        )
                        response = responseOpenai['choices'][0]['message']['content']
                        context += textAudio + "\n" + response + "\n"
                        print("---------")
                        print(context)
                        print("---------")
                        voice.speak(response)
                    except openai.APIError as e:
                        response = "Erro... Openai não respondendo..."
                        print(e)
                        voice.speak(response)
                        
                db.logs(textAudio, response)






            # Para valores não identificados
            except sr.UnknownValueError:
                print("...")













# Interface to put the password and the loggin
if __name__ == "__main__":    
    if True:
        # Starts a thread to the back-end code
        thread_code = threading.Thread(target=code)
        thread_code.start()

    # If the password or the loggin is incorrect the code executes the else
    else:
        exit()