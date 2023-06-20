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
import pygetwindow as gw
import pyautogui
from pywinauto import Desktop



# Libraris
import classes.appManagement as app
import classes.voice as voice
import classes.spotify as spotify
import database.database as db
import classes.passwords as passwords
import classes.climate as climate
import classes.listening as listening
import classes.openaiii as openaifreatures
import classes.openAppSecondScreen as openAppSecondScreen
import classes.searchs as searchs


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

                    #Code to logof windows
                    elif db.question("sair sistema", textAudio):
                        voice.speak(db.answer("sair sistema"))
                        time.sleep(5)
                        os.system("shutdown -l")


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
                    elif db.question("mudar de assunto", textAudio):
                        context = "-"
                        voice.speak(db.answer("mudar de assunto")) 


                    # PyAutoGUI freatures
                    elif db.question("abrir gerenciador de tarefas", textAudio):
                        voice.speak(db.answer("abrir gerenciador de tarefas"))
                        pyautogui.hotkey("ctrl", "shift", "esc")

                    elif db.simpleQuestion("area de trabalho", textAudio):
                        if db.simpleQuestion("criar", textAudio):
                            voice.speak("Criando uma nova area de trabalho")
                            pyautogui.hotkey("ctrl", "winleft", "d")

                        elif db.simpleQuestion("deletar", textAudio):
                            voice.speak("Deletando a area de trabalho!")
                            pyautogui.hotkey("ctrl", "winleft", "f4")

                        elif db.simpleQuestion("anterior", textAudio):
                            voice.speak("Movendo para a area de trabalho anterior!")
                            pyautogui.hotkey("ctrl", "winleft", "left")

                        elif db.simpleQuestion("proxima", textAudio):
                            voice.speak("Movendo para a proxima area de trabalho!")
                            pyautogui.hotkey("ctrl", "winleft", "right")


                    # Next song in spotify
                    elif db.question("pular musica", textAudio):
                        retorno = db.answer("pular musica")
                        voice.speak(retorno)
                        spotify.next()

                    # Play in music
                    elif db.question("play musica", textAudio):
                        retorno = db.answer("play musica")
                        voice.speak(retorno)
                        spotify.play()

                    # Pause in music
                    elif db.question("pausar musica", textAudio):
                        retorno = db.answer("pausar musica")
                        voice.speak(retorno)
                        spotify.pause()
                                        
                    # Select a music
                    elif db.question("selecionar musica", textAudio):
                        voice.speak("Diga o nome da musica que você quer que eu toque")
                        retorno = "Diga o nome da musica que você quer que eu toque"
                        try:
                            Music = r.listen(source)
                            textAudio=(r.recognize_google(Music, language='pt-br'))
                        except:
                            print("Deu um Erro!!")
                        retorno = "Reproduzindo a música que você pediu!"
                        voice.speak(retorno)
                        spotify.selectSong(textAudio)

                    # Selects a playlist
                    elif db.question("tocar playlist", textAudio):
                        voice.speak("Diga o nome da playlist que você quer que eu toque")
                        retorno = "Diga o nome da playlist que você quer que eu toque"
                        try:
                            Music = r.listen(source)
                            textAudio=(r.recognize_google(Music, language='pt-br'))
                        except:
                            print("Deu um Erro!!") 
                        retorno = "Reproduzindo a playlist que você pediu!"
                        voice.speak(retorno)
                        spotify.selectPlaylist(textAudio)
                    

                    # Generate image with openai
                    elif db.question("modo geracao de imagem", textAudio):
                        gerarOutraImagem = True
                        while gerarOutraImagem == True:
                            openai.api_key = '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'
                            voice.speak("Descreva a imagem que você deseja Gerar")
                            try:
                                textAudio = listening.listening()
                                voice.speak("Gerando Imagem " + textAudio)

                                response = openai.Image.create(
                                prompt = textAudio,
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

                            voice.speak("Você deseja gerar outra imagem?")
                            textAudio = listening.listening()
                            if "não" in textAudio:
                                voice.speak("Beleza, eu não irei gerar outra imagem")
                                gerarOutraImagem = False


                    # Generate a password
                    elif db.question("gerar senha", textAudio):
                        voice.speak("Gerando senha")
                        response = passwords.genPassword(20)
                        print(response)
                        voice.speak("Senha gerada " + response)


                    # Get the climate prevision
                    elif db.question("checar clima", textAudio):
                        prevClimate = str(climate.getPrevision("Chapecó"))
                        voice.speak(prevClimate)


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
                    

                    # Activates the music mode and only recive music commands
                    elif db.question("modo musica", textAudio):
                        loop = True
                        voice.speak("Modo musica ativado!")
                        while loop == True:
                            with sr.Microphone() as sourceMusic:
                                try:
                                    basicAudioMusic = r.listen(sourceMusic)
                                    textAudio=(r.recognize_google(basicAudioMusic, language="pt-br"))
                                    textAudio = textAudio.lower() 
                                    print("recognizing...\n")
                                    print(textAudio + "\n")

                                    # Next song in spotify
                                    if db.question("pular musica", textAudio):
                                        retorno = db.answer("pular musica")
                                        voice.speak(retorno)
                                        spotify.next()

                                    # Play in music
                                    elif db.question("play musica", textAudio):
                                        retorno = db.answer("play musica")
                                        voice.speak(retorno)
                                        spotify.play()

                                    # Pause in music
                                    elif db.question("pausar musica", textAudio):
                                        retorno = db.answer("pausar musica")
                                        voice.speak(retorno)
                                        spotify.pause()
                                                        
                                    # Select a music
                                    elif db.question("selecionar musica", textAudio):
                                        voice.speak("Diga o nome da musica que você quer que eu toque")
                                        retorno = "Diga o nome da musica que você quer que eu toque"
                                        try:
                                            Music = r.listen(source)
                                            textAudio=(r.recognize_google(Music, language='pt-br'))
                                        except:
                                            print("Deu um Erro!!")
                                        retorno = "Reproduzindo a música que você pediu!"
                                        voice.speak(retorno)
                                        spotify.selectSong(textAudio)

                                    # Selects a playlist
                                    elif db.question("tocar playlist", textAudio):
                                        voice.speak("Diga o nome da playlist que você quer que eu toque")
                                        retorno = "Diga o nome da playlist que você quer que eu toque"
                                        try:
                                            Music = r.listen(source)
                                            textAudio=(r.recognize_google(Music, language='pt-br'))
                                        except:
                                            print("Deu um Erro!!") 
                                        retorno = "Reproduzindo a playlist que você pediu!"
                                        voice.speak(retorno)
                                        spotify.selectPlaylist(textAudio)

                                    elif "desativar o modo música" in textAudio or "sair do modo música" in textAudio:
                                        loop = False
                                        voice.speak("Desativando o modo música!")

                                    else:
                                        print("--> Modo musica ativado <--")
                                        print("--> Para desativar fale 'desativar o modo musica' ou 'sair do modo musica' <--")

                                except sr.UnknownValueError:
                                    print("--> Modo musica ativado <--")


                    elif db.question("pesquisa", textAudio):

                        if "google" in textAudio:
                            searching = searchs.searchGoogle(textAudio)
                            voice.speak(searching)

                        


                        
                        

                        
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