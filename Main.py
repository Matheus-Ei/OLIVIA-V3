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
                    if  db.question("abrir aplicativo", textAudio):
                        # Ask what app the user wants open
                        voice.speak("Qual aplicativo voce deseja abrir?")
                        try:
                            basicAudio = r.listen(source)
                            textAudio=(r.recognize_google(basicAudio, language='pt-br'))
                            app.open(textAudio) # Opening the app
                        except:
                            print("#####@ ERROR @#####")

                    
                    # Speak the time
                    elif db.question("horas", textAudio):
                        global hour, minutes, seconds, day, week, mounth, year
                        timeGet()
                        response=("São %d e %d minutos" %(hour ,minutes))
                        voice.speak(response)


                    # Ends the code
                    elif db.question("desligamento", textAudio):
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


                    # Reset the var of context in the GPT-Chat
                    elif db.question("mudar de assunto", textAudio):
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

                    elif db.question("mover para a area de trabalho a esquerda", textAudio):
                        voice.speak(db.answer("mover para a are de trabalho a esquerda"))
                        pyautogui.hotkey("ctrl", "winleft", "left")

                    elif db.question("mover para a are de trabalho a direita", textAudio):
                        voice.speak(db.answer("mover para a are de trabalho a direita"))
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


                    # Reset the execution of the code
                    elif db.question("reiniciar o codigo", textAudio):
                        voice.speak("Reiniciando a execução do código")
                        nome_procurado = "Visual Studio Code" # Search the name of the app

                        desktop = Desktop(backend="uia")
                        janela = desktop.window(title_re=".*{}.*".format(nome_procurado))
                        janela.set_focus() # Activate the window

                        print(janela)

                        pyautogui.hotkey("ctrl", "shift", "f5")


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