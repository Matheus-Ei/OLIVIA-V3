# Imports
import speech_recognition as sr
import threading
from datetime import datetime
import openai
import sys
import os
import time
import pyautogui
import webbrowser
import re
import pygetwindow as gw
import pyautogui
from pywinauto import Desktop
import speedtest


# Libraris
import classes.appManagement as app
import classes.voice as voice
import classes.spotify as spotify
import database.database as db
import classes.passwords as passwords
import classes.climate as climate
import classes.listening as listening
import classes.openaiCodes as openaifreatures
import classes.searchs as searchs
import classes.message.email as email
import classes.message.whatsapp as whatsapp
import classes.network as ntw
import classes.translator as personalTranslator


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
textAudio = " "
response = " "




# Main function to back-end
def code():
    # Globals
    global textAudio, response, context, enter

    # Var pre-definitions
    context = " "
    enter = " "

    # Creating the Speech Recognition and defines the openai key
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


                if "prometeu" in textAudio or "jarvis" in textAudio:
                    textAudio = textAudio.replace("prometeu", "")
                    try:
                        openai.api_key = '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'
                        enter = context + "\n" + textAudio + "\n"
                        print(enter)
                        responseOpenai = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo-0301",
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



                else:
                    # Open a app
                    if  db.simpleQuestion("abrirAPP", textAudio):
                        # Code to open task mananger
                        if db.simpleQuestion("gerenciador de tarefas", textAudio):
                            voice.speak(db.answer("abrir gerenciador de tarefas"))
                            pyautogui.hotkey("ctrl", "shift", "esc")
                        # Code to Open a Commun app
                        else:
                            loopv = 0
                            aplicativos = [
                                'calculator',
                                'notepad',
                                'explorer',
                                'opera',
                                'navegator',
                                'canva',
                                'visual studio code',
                                'blender',
                            ]
                            while loopv < len(aplicativos):
                                if aplicativos[loopv] in textAudio:
                                    app.open(aplicativos[loopv]) # Opening the app
                                loopv = loopv+1

                    
                    # Speak the time
                    elif db.simpleQuestion("horas", textAudio):
                        global hour, minutes, seconds, day, week, mounth, year
                        timeGet()
                        response=("São %d e %d minutos" %(hour ,minutes))
                        voice.speak(response)


                    # Code to turn off
                    elif db.simpleQuestion("desligamento", textAudio):
                        # Ends the code
                        if db.simpleQuestion("codigo", textAudio):
                            voice.speak("Desativando o código!") 
                            sys.exit()
                        #Code to turn off windows
                        elif db.simpleQuestion("windows", textAudio):
                            voice.speak("Desligando o windows em 5 segundos!")
                            time.sleep(5)
                            os.system("shutdown /s /t 1")


                    # Code to Logof
                    elif db.simpleQuestion("sair", textAudio):
                        #Code to logof windows
                        if db.simpleQuestion("windows", textAudio):
                            voice.speak("Saindo do windows em 5 segundos")
                            time.sleep(5)
                            os.system("shutdown -l")


                    # Code to restart
                    elif db.simpleQuestion("reiniciar", textAudio):
                        # restarts the code
                        if db.simpleQuestion("codigo", textAudio):
                            voice.speak("Reiniciando a execução do código")
                            nome_procurado = "Visual Studio Code" # Search the name of the app
                            desktop = Desktop(backend="uia")
                            janela = desktop.window(title_re=".*{}.*".format(nome_procurado))
                            janela.set_focus() # Activate the window
                            pyautogui.hotkey("ctrl", "shift", "f5")
                        # Code to restart windows
                        elif db.simpleQuestion("windows", textAudio):
                            voice.speak("Reiniciando o Windows em 5 segundos!")
                            time.sleep(5)
                            os.system("shutdown /r /t 1")
                        # Reset the var of context in the GPT-Chat
                        elif db.simpleQuestion("contexto", textAudio):
                            context = "-"
                            voice.speak("Mudando de Assunto") 


                    # Desktop Commands
                    elif db.simpleQuestion("area de trabalho", textAudio):
                        # New Desktop
                        if db.simpleQuestion("criar", textAudio):
                            voice.speak("Criando uma nova area de trabalho")
                            pyautogui.hotkey("ctrl", "winleft", "d")
                        # Delete Desktop
                        elif db.simpleQuestion("deletar", textAudio):
                            voice.speak("Deletando a area de trabalho!")
                            pyautogui.hotkey("ctrl", "winleft", "f4")
                        # Desktop before
                        elif db.simpleQuestion("anterior", textAudio):
                            voice.speak("Movendo para a area de trabalho anterior!")
                            pyautogui.hotkey("ctrl", "winleft", "left")

                        # Next Desktop
                        elif db.simpleQuestion("proxima", textAudio):
                            voice.speak("Movendo para a proxima area de trabalho!")
                            pyautogui.hotkey("ctrl", "winleft", "right")


                    # Music Commands
                    elif db.simpleQuestion("musicas", textAudio):
                        # Next song in spotify
                        if db.simpleQuestion("pular", textAudio):
                            retorno = "Pulando musica"
                            voice.speak(retorno)
                            spotify.next()
                        # Play in music
                        elif db.simpleQuestion("play", textAudio):
                            retorno = "Tocando musica"
                            voice.speak(retorno)
                            spotify.play()
                        # Pause in music
                        elif db.simpleQuestion("pausar", textAudio):
                            retorno = "Pausando musica"
                            voice.speak(retorno)
                            spotify.pause()
                        # Select a music
                        elif db.simpleQuestion("selecionar", textAudio):
                            retorno = "Tocando a musica selecionada"
                            voice.speak(retorno)
                            selectedMusic = db.simpleQuestionPerg("musicas", textAudio)
                            selectedMusic = db.simpleQuestionPerg("selecionar", selectedMusic)
                            print(selectedMusic)
                            spotify.selectSong(selectedMusic)


                    # Playlists Commands
                    elif db.simpleQuestion("playlist", textAudio):
                        # Selects a playlist
                        if db.simpleQuestion("selecionar", textAudio):
                            retorno = "Tocando a playlist selecionada"
                            voice.speak(retorno)
                            selectedMusic = db.simpleQuestionPerg("playlist", textAudio)
                            selectedMusic = db.simpleQuestionPerg("selecionar", selectedMusic)
                            print(selectedMusic)
                            spotify.selectPlaylist(selectedMusic)
                    

                    # Generate thinks
                    elif db.simpleQuestion("gerar", textAudio):
                        # Generate image
                        if db.simpleQuestion("imagem", textAudio):
                            gerarOutraImagem = True
                            while gerarOutraImagem == True:
                                generateCommand = db.simpleQuestionPerg("gerar", textAudio)
                                generateCommand = db.simpleQuestionPerg("imagem", generateCommand)
                                openaifreatures.generateImage(generateCommand)
                        # Generate a password
                        elif db.simpleQuestion("senha", textAudio):
                            inteiro = re.findall(r'\d+', textAudio)
                            try:
                                inteiro = inteiro[0]
                            except IndexError:
                                inteiro = "20"
                                print("IndexError")
                            except TypeError:
                                print("TypeError")
                            if inteiro in textAudio:
                                inteiro = int(inteiro)
                                voice.speak("Gerando senha")
                                response = passwords.genPassword(inteiro)
                                print(response)
                                voice.speak("Senha gerada e printada")
                            # Turns on the pattern value
                            else:
                                voice.speak("Gerando senha")
                                response = passwords.genPassword(20)
                                print(response)
                                voice.speak("Senha gerada: " + response)


                    # Get the climate prevision
                    elif db.simpleQuestion("clima", textAudio):
                        prevClimate = climate.getPrevision("Chapecó")
                        for climat in prevClimate:    
                            voice.speak(climat)


                    # Activate the emergenci mode
                    elif db.question("emergencia",  textAudio):
                        voice.speak("Primeiramente qual é o tipo de emergencia? Vou te dar alguns conselhos dependendo disso! fale apenas a emergencia!")
                        textAudio = listening.listening()
                        if "incêndio" in textAudio or "fogo" in textAudio:
                            voice.speak("Modo incêndio ativado!")
                            textAudio = "Me fale como lidar com esse tipo de emergencia " + textAudio + " me diga o tempo que eu normalmente teria, alem de como agir, com o que devo me preocupar, entre outras coisas que voce julgar importantes"
                            textAudio = openaifreatures.chat(textAudio)
                            voice.speak(textAudio)
                            voice.speak("Você deseja que eu ligue para os bombeiros?")
                            textAudio = listening.listening()

                        elif "médica" in textAudio or "machucado" in textAudio or "quebrado" in textAudio or "doênte" in textAudio:
                            voice.speak("Modo Emergência médica ativado!")
                            voice.speak("Qual é o tipo de emergência médica?")
                            textAudio = listening.listening()
                            textAudio = "Me fale como lidar com esse tipo de emergencia " + textAudio + " me diga o tempo que eu normalmente teria, alem de como agir, com o que devo me preocupar, entre outras coisas que voce julgar importantes"
                            textAudio = openaifreatures.chat(textAudio)
                            voice.speak(textAudio)
                            voice.speak("Você deseja que eu ligue para uma ambulancia?")
                            textAudio = listening.listening()

                        elif "assalto" in textAudio or "bandidos" in textAudio or "matar" in textAudio or "matou" in textAudio or "polícial" in textAudio:
                            voice.speak("Modo Emergência policial ativado!")
                            textAudio = "Me fale como lidar com esse tipo de emergencia " + textAudio + " me diga o tempo que eu normalmente teria, alem de como agir, com o que devo me preocupar, entre outras coisas que voce julgar importantes"
                            textAudio = openaifreatures.chat(textAudio)
                            voice.speak(textAudio)
                            voice.speak("Você deseja que eu ligue para a polícia?")
                            textAudio = listening.listening()

                        else:
                            textAudio = "Me fale como lidar com esse tipo de emergencia " + textAudio + " me diga o tempo que eu normalmente teria, alem de como agir, com o que devo me preocupar, entre outras coisas que voce julgar importantes"
                            textAudio = openaifreatures.chat(textAudio)
                            voice.speak(textAudio)


                    # Funcion to search somethink
                    elif db.simpleQuestion("pesquisa", textAudio):
                        # Funcion to search somethink in google
                        if "google" in textAudio:
                            generateCommand = db.simpleQuestionPerg("pesquisa", textAudio)
                            generateCommand = db.simpleQuestionPerg("google", generateCommand)
                            searching = searchs.searchGoogle(generateCommand)
                            voice.speak(searching)
                        # Funcion to search somethink in wikipedia
                        elif "wikipédia" in textAudio:
                            generateCommand = db.simpleQuestionPerg("pesquisa", textAudio)
                            generateCommand = db.simpleQuestionPerg("wikipedia", generateCommand)
                            searching = searchs.searchWiki(generateCommand)
                            voice.speak(searching)
                        # Funcion to send everithink
                        else:
                            voice.speak("Você não definiu em qual mecanismo de busca deseja procurar!")

                    
                    # Funcion to send a message
                    elif db.simpleQuestion("enviar", textAudio):
                        if "whatsapp" in textAudio:
                            print("Whatsapp")
                            numbers = {"mãe": "63 9985-0556",
                                    "pai": "63 9919-0929",
                                    "giovanna": "55 9937-2808"}
                            for numberName in numbers.keys():
                                if numberName in textAudio:
                                    number = numbers[numberName]
                                    message = textAudio.split(numberName)[-1]
                                    voice.speak("Você realmente deseja enviar essa mensagem? " + message)
                                    send = listening.listening()
                                    if "sim" in send:
                                        whatsapp.sendMessage(number, message)
                                        voice.speak("Enviando mensagem para " + numberName)
                        elif "e-mail" in textAudio:
                            print("Email")
                            #email.sendEmail(destinatario, Assunto, message)
                        else:
                            retorno = "Para enviar algo você deve especificar a Via"
                            voice.speak(retorno)

                    
                    elif db.simpleQuestion("fechar", textAudio):
                        aplication = db.simpleQuestionPerg("fechar", textAudio)
                        #aplication = aplication.replace(" ", "")
                        aplication = aplication.split()
                        for carac in aplication:
                            caracteres = list(carac)
                            contador = len(caracteres)
                            print(contador)
                            print(caracteres)
                            if contador>4:
                                print(carac)
                                if app.close(carac):
                                    voice.speak("Aplicativo fechado!")



                    elif db.simpleQuestion("testar", textAudio):
                        # Creates the speedtest object
                        testeVelocidade = speedtest.Speedtest()
                        # Tests the Values
                        downloadSpeed = ntw.velocidade_downloadd(testeVelocidade)
                        uploadSpeed = ntw.velocidade_uploadd(testeVelocidade)
                        ping = ntw.pingg(testeVelocidade)
                        # Enter in the condicionals values
                        if db.simpleQuestion("ping", textAudio):
                            voice.speak(ping)
                        if db.simpleQuestion("download", textAudio):
                            voice.speak(downloadSpeed)
                        if db.simpleQuestion("upload", textAudio):
                            voice.speak(uploadSpeed)


                        

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