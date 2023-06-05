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
import tensorflow as tf
from tensorflow import keras
import pickle


# Libraris
import classes.appManagement as app
import classes.voice as voice
import classes.spotify as spotify
import database.database as db
import classes.passwords as passwords
import classes.climate as climate


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




# Main funcion to back-end
def code():
    # Globals
    global textAudio, response, context, enter

    # Var pre-definitions
    context = " "
    enter = " "

    # Creating the Speach Recognition and defines the openai key
    r = sr.Recognizer()

    # Loading the tokenizer and the model
    with open(r"neuralNetwork\sentenceClassifier\tokenizer.pickle", "rb") as handle:
        tokenizer = pickle.load(handle)
    model = keras.models.load_model(r"neuralNetwork\sentenceClassifier\modelo_classificador")
    # funcion to classify the sentences
    def classificar_frase(frase):
        sequence = tokenizer.texts_to_sequences([frase])
        padded_sequence = keras.preprocessing.sequence.pad_sequences(sequence, maxlen=model.input_shape[1], padding="post")
        prediction = model.predict(padded_sequence)
        predicted_class_index = tf.argmax(prediction, axis=1).numpy()[0]

        # Definition of the possibles classes
        classes = ["abrirApp", "horario", "desligarCode", "desligarWindows", "sairWindows", "reiniciarWindows", "mudarAssunto", "abrirGerenciadorTarefas", "visaoTarefas", "novaAreaTrabalho", "deletarAreaTrabalho", "moverAreaTrabalhoEsquerda", "moverAreaTrabalhoDireita", "pularMusica", "pausarMusica", "playMusica", "selecionarMusica", "selecionarPlaylist", "gerarImagem", "gerarSenha"]

        predicted_class = classes[predicted_class_index]
        return predicted_class
    

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


                if "prometeu" in textAudio:
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
                    # Getting the class of the textAudio
                    neuralResult = classificar_frase(textAudio)
                    print(textAudio, "=> Classe:", neuralResult)


                    # Open a app
                    if  neuralResult == "abrirApp":
                        # Ask what app the user wants open
                        voice.speak("Qual aplicativo voce deseja abrir?")
                        try:
                            basicAudio = r.listen(source)
                            textAudio=(r.recognize_google(basicAudio, language='pt-br'))
                            app.open(textAudio) # Opening the app
                        except:
                            print("#####@ ERROR @#####")

                    
                    # Speak the time
                    elif neuralResult == "horario":
                        global hour, minutes, seconds, day, week, mounth, year
                        timeGet()
                        response=("São %d e %d minutos" %(hour ,minutes))
                        voice.speak(response)


                    # Ends the code
                    elif neuralResult == "desligarCode":
                        voice.speak(db.answer("desligamento")) 
                        sys.exit()


                    # Code to execute comands in windows, like turn of or loggof
                    elif neuralResult == "desligarWindows":
                        voice.speak(db.answer("desligar sistema"))
                        time.sleep(5)
                        os.system("shutdown /s /t 1")

                    elif neuralResult == "sairWindows":
                        voice.speak(db.answer("sair sistema"))
                        time.sleep(5)
                        os.system("shutdown -l")

                    elif neuralResult == "reiniciarWindows":
                        voice.speak(db.answer("reiniciar sistema"))
                        time.sleep(5)
                        os.system("shutdown /r /t 1")


                    # Reseta a variavel contexto do chat-gpt
                    elif neuralResult == "mudarAssunto":
                        context = "-"
                        voice.speak(db.answer("mudar de assunto")) 


                    # PyAutoGUI freatures
                    elif neuralResult == "abrirGerenciadorTarefas":
                        voice.speak(db.answer("abrir gerenciador de tarefas"))
                        pyautogui.hotkey("ctrl", "shift", "esc")

                    elif neuralResult == "visaoTarefas":
                        voice.speak(db.answer("visao geral das tarefas"))
                        pyautogui.hotkey("winleft", "tab")

                    elif neuralResult == "novaAreaTrabalho":
                        voice.speak(db.answer("nova area de trabalho"))
                        pyautogui.hotkey("ctrl", "winleft", "d")

                    elif neuralResult == "deletarAreaTrabalho":
                        voice.speak(db.answer("deletar area de trabalho"))
                        pyautogui.hotkey("ctrl", "winleft", "f4")

                    elif neuralResult == "moverAreaTrabalhoEsquerda":
                        voice.speak(db.answer("mover para a are de trabalho a esquerda"))
                        pyautogui.hotkey("ctrl", "winleft", "left")

                    elif neuralResult == "moverAreaTrabalhoDireita":
                        voice.speak(db.answer("mover para a are de trabalho a direita"))
                        pyautogui.hotkey("ctrl", "winleft", "right")


                    # Next song in spotify
                    elif neuralResult == "pularMusica":
                        db.answer("pular musica")
                        voice.speak(retorno)
                        spotify.next()

                    # Play in music
                    elif neuralResult == "playMusica":
                        db.answer("play musica")
                        voice.speak(retorno)
                        spotify.play()

                    # Pause in music
                    elif neuralResult == "pausarMusica":
                        db.answer("pausar musica")
                        voice.speak(retorno)
                        spotify.pause()
                                        
                    # Select a music
                    elif neuralResult == "selecionarMusica":
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
                    elif neuralResult == "selecionarPlaylist":
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
                    elif neuralResult == "gerarImagem":
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
                            voice.speak("Gerando Imagem")
                            image_url = response['data'][0]['url']
                            print(image_url)
                            # Open the image in navegator
                            retorno = "Abrindo a Imagem Gerada"
                            voice.speak(retorno)
                            webbrowser.open(image_url)
                        except:
                            print("#####@ ERROR @#####")


                    # Generate a password
                    elif neuralResult == "gerarSenha":
                        voice.speak("Gerando senha")
                        response = passwords.genPassword(20)
                        print(response)
                        voice.speak("Senha gerada " + response)


                    elif neuralResult == "":
                        voice.speak(climate.getPrevision("Chapecó"))
                        
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