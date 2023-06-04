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
import classes.other as other


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

    # Creating the connection with the database
    conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=database\mainDb.accdb;'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Creating the Speach Recognition and defines the openai key
    r = sr.Recognizer()

    # Funcion to consult the questions to PROMETEU and check if they are in database
    def question(question):
        global textAudio
        try:
            # Execute a consult
            cursor.execute('SELECT perg FROM question WHERE func = '+"'"+question+"';")
            # Recover the consult data
            rows = cursor.fetchall()
            for row in rows:
                roww = str(row[0])
                if roww in textAudio:
                    return True
        except pyodbc.Error as e:
            print(e)
        
    # Funcion to consult the answer that PROMETEU needs to gave
    def answer(answer):
        try:
            # Execute a consult
            cursor.execute('SELECT resp FROM answer WHERE func = '+"'"+answer+"';")
            # Recover the consult data
            rows = cursor.fetchall()
            preResponse = []
            cont = 0
            for row in rows:
                cont = cont + 1
                roww = str(row[0])
                preResponse.append(roww)
            cont = cont-1
            # Selects a random response and return
            number = random.randint(0, cont)
            response = preResponse[number]
            return response
        except pyodbc.Error as e:
            print(e)

    # Funcion to logs with database
    def logs(textAudio, response):
        time=datetime.now() 
        hour = int(time.strftime("%H"))
        minutes = int(time.strftime("%M"))
        seconds = time.strftime("%S")
        day = time.strftime("%d")
        week = time.strftime("%A")
        mounth = time.strftime("%B")
        year = time.strftime("%Y")
        try:
            year = str(year)
            mounth = str(mounth)
            week = str(week)
            day = str(day)
            hour = str(hour)
            minutes = str(minutes)
            seconds = str(seconds)
            # Defines the date
            date = str(year+"/"+mounth+"/"+day+":"+week+"/"+hour+":"+minutes+":"+seconds)
            response = str(response)
            textAudio = str(textAudio)
            cursor.execute("INSERT INTO logs(usuario, jarvis, data) VALUES ('"+textAudio+"','"+response+"','"+date+"');")
            # Save the alterations in the logs tabble
            conn.commit()
        # If haves a exeption the code prints what exeption have
        except pyodbc.Error as e:
            print(e)


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
                if  question('abrir aplicativo'):
                    # Ask what app the user wants open
                    voice.speak("Qual aplicativo voce deseja abrir?")
                    try:
                        basicAudio = r.listen(source)
                        textAudio=(r.recognize_google(basicAudio, language='pt-br'))
                        app.open(textAudio) # Opening the app
                    except:
                        print("#####@ ERROR @#####")

                
                # Speak the time
                elif question('horas'):
                    global hour, minutes, seconds, day, week, mounth, year
                    timeGet()
                    response=("São %d e %d minutos" %(hour ,minutes))
                    voice.speak(response)


                # Ends the code
                elif question('desligamento'):
                    voice.speak(answer("desligamento")) 
                    sys.exit()


                # Code to execute comands in windows, like turn of or loggof
                elif question("desligar sistema"):
                    voice.speak(answer("desligar sistema"))
                    time.sleep(5)
                    os.system("shutdown /s /t 1")

                elif question("sair sistema"):
                    voice.speak(answer("sair sistema"))
                    time.sleep(5)
                    os.system("shutdown -l")

                elif question("reiniciar sistema"):
                    voice.speak(answer("reiniciar sistema"))
                    time.sleep(5)
                    os.system("shutdown /r /t 1")


                # Reseta a variavel contexto do chat-gpt
                elif question('mudar de assunto'):
                    context = "-"
                    voice.speak(answer("mudar de assunto")) 


                # PyAutoGUI freatures
                elif question("abrir gerenciador de tarefas"):
                    voice.speak(answer("abrir gerenciador de tarefas"))
                    pyautogui.hotkey("ctrl", "shift", "esc")

                elif question("visao geral das tarefas"):
                    voice.speak(answer("visao geral das tarefas"))
                    pyautogui.hotkey("winleft", "tab")

                elif question("nova area de trabalho"):
                    voice.speak(answer("nova area de trabalho"))
                    pyautogui.hotkey("ctrl", "winleft", "d")

                elif question("deletar area de trabalho"):
                    voice.speak(answer("deletar area de trabalho"))
                    pyautogui.hotkey("ctrl", "winleft", "f4")

                elif question("mover para a are de trabalho a esquerda"):
                    voice.speak(answer("mover para a are de trabalho a esquerda"))
                    pyautogui.hotkey("ctrl", "winleft", "left")

                elif question("mover para a are de trabalho a direita"):
                    voice.speak(answer("mover para a are de trabalho a direita"))
                    pyautogui.hotkey("ctrl", "winleft", "right")
                

                # Generate image with openai
                elif question('modo geracao de imagem'):
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
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content":enter}
                            ],
                            max_tokens=200
                        )
                        chat = response['choices'][0]['message']['content']
                        context += textAudio + "\n" + chat + "\n"
                        print("---------")
                        print(context)
                        print("---------")
                        voice.speak(chat)
                    except openai.APIError as e:
                        response = "Erro... Openai não respondendo..."
                        print(e)
                        voice.speak(response)
                        

                logs(textAudio, chat)






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