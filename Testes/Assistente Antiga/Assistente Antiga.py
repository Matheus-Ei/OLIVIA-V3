#Imports
from audioop import error
from calendar import c
from inspect import EndOfBlock
from math import log
from re import X
from typing import Text
from wave import Error
from xmlrpc.client import boolean
import keyboard
from pynput.keyboard import Listener, Key
import speech_recognition as sr
import pyttsx3
import gtts
from datetime import datetime
import random
import sys
import requests
from bs4 import BeautifulSoup


#Informações do usuario
Nome_do_usuario = "Matheus"
Cidade_do_usuario = "Chapecó"


#Reproduz os sons iniciais da assistente
# playsound("Assistente pessoal!\note.wav")


#Cria o reconhecedor de voz e o leitor de texto
r = sr.Recognizer()
engine = pyttsx3.init()
volume = engine.getProperty('volume')
rate = engine.getProperty('rate')
engine.setProperty('volume', volume+10)
engine.setProperty('rate', rate-30)


#Localização no tempo(Horas)
tempo=datetime.now() 
hora = int(tempo.strftime("%H"))
minutos = int(tempo.strftime("%M"))
segundos = tempo.strftime("%S")
Dia_da_semana = tempo.strftime("%A")
Mes_do_ano = tempo.strftime("%B")
Ano = tempo.strftime("%Y")


#Previsão do tempo(Clima)
busca =f"A Previsão do tempo em {Cidade_do_usuario} é de "
url = f"https://www.google.com/search?q={busca}"
rq = requests.get(url)
s= BeautifulSoup(rq.text, "html.parser")
update = s.find("div",class_="BNeawe").text


    #Ler uma informação
def ler_uma_informação():
    arquivo = open('info.txt', 'r')
    for linha in arquivo:
        print(linha)
    arquivo.close()


    #Escrever uma nova informação
def escrever_uma_nova_informação():
    arquivo = open('info.txt', 'w')
    nova_informação=("Temporariamente nada")
    arquivo.write(nova_informação)
    arquivo.close()


#Função resposta 1
def função_resposta():
    with sr.Microphone() as source:
        while True:
            try:
                audio = r.listen(source)
                audio_tratado=('O')
                audio_tratado=(r.recognize_google(audio, language='pt-BR'))
                audio_tratado = audio_tratado.lower()
                if audio_tratado == "modo ativo" or audio_tratado=="ativação":
                    print("<===============>")
                    print(audio_tratado)
                    print("<===============>")
                    return Nome_do_usuario

            except sr.UnknownValueError:
                return audio


#Função resposta para buscas
def função_resposta_para_buscas():
    with sr.Microphone() as source:
        while True:
            print("Diga o que você quer que eu pesquise")
            try:
                audio = r.listen(source)
                audio_tratado=('O')
                audio_tratado=(r.recognize_google(audio, language='pt-BR'))
                audio_tratado = audio_tratado.lower()

                busca=audio_tratado
                url = f"https://www.google.com/search?q={busca}"
                rq = requests.get(url)
                s= BeautifulSoup(rq.text, "html.parser")
                update = s.find("div",class_="BNeawe").text

                if update==int or update==float or update==bool:
                    engine.say("Não achei nenhum resultado que eu possa te falar claramente chefe")
                    return Nome_do_usuario
                else:
                    a="O resultado da pesquisa é esse: %s"%(update)
                    engine.say(a)
                    print(a)
                    return Nome_do_usuario

            except sr.UnknownValueError:
                return audio


#Abre o microfone pra captura
with sr.Microphone() as source:
    while True:
        try:
            audio = r.listen(source)
            audio_tratado=('O')
            audio_tratado=(r.recognize_google(audio, language='pt-BR'))
            audio_tratado = audio_tratado.lower()
            print("<===============>")
            print(audio_tratado)
            print("<===============>")

        except sr.UnknownValueError:
            numero_aleatório_para_falta_de_entendimento = random.randint(1, 5)
            falta_de_entendimento = "Nada"
            if numero_aleatório_para_falta_de_entendimento == 1:
                falta_de_entendimento = "NÃO ENTENDI O QUE VOCÊ FALOU!"
            
            if numero_aleatório_para_falta_de_entendimento == 2:
                falta_de_entendimento = "VOCÊ PODERIA REPETIR O QUE FALOU?"

            if numero_aleatório_para_falta_de_entendimento == 3:
                falta_de_entendimento = "TA CANTANDO HAHAHA"

            if numero_aleatório_para_falta_de_entendimento == 4:
                falta_de_entendimento = "FALA MAIS DEVAGAR MATHEUS!"

            if numero_aleatório_para_falta_de_entendimento == 5:
                falta_de_entendimento = "EU ATÉ TE RESPONDERIA SE EU TIVESSE ENTENDIDO!"

            print("<===============>")
            print(falta_de_entendimento)
            engine.say(falta_de_entendimento)
            print("<===============>")


#Codigos das respostas
    #Modo suspenção
        if audio_tratado=="modo suspensão" or audio_tratado=="modo suspenso" or audio_tratado=="modo soneca":
            função_resposta()


    #Comprimentos de boas vindas
        if audio_tratado=="oi" or audio_tratado=="olá" or audio_tratado=="bom dia" or audio_tratado=="boa tarde" or audio_tratado=="boa noite" or audio_tratado=="opa" or audio_tratado=="salve"  or audio_tratado=="e aí" or audio_tratado=="como vai" or audio_tratado=="fala":
            numero = random.randint(1, 9)

            if numero == 1:
                a=("Oi")
            if numero == 2:
                a=("Olá")
            if numero == 3:
                if(18 > hora > 12):
                    a=("Boa tarde")
                elif(hora < 12):
                    a=("Bom dia!")
                elif(hora > 18):
                    a=("Boa noite!")
            if numero == 4:
                a=("Opa")
            if numero == 5:
                a=("Salve")
            if numero == 6:
                a=("Como vai")
            if numero == 7:
                a=("Eai")
            if numero == 8:
                a=("diga")
            if numero == 9:
                a=("fala")

            engine.say(a)
            print(a)


    #Que horas são?
        if audio_tratado=="que horas são" or audio_tratado=="horas" or audio_tratado=="me fala as horas Silvia" or audio_tratado=="me fala as horas":
            a=("São %d e %d minutos" %(hora,minutos))
            engine.say(a)
            print(a)


    #Comprimento de finalização de conversa
        if audio_tratado=="até mais" or audio_tratado=="falou" or audio_tratado=="desligar" or audio_tratado=="pode descansar" or audio_tratado=="tchau" or audio_tratado=="vai dormir":
            numero = random.randint(1, 5)

            if numero == 1:
                a=("Aguardo sua proxima ordem")
            if numero == 2:
                a=("Até mais")
            if numero == 3:
                a=("Tchau senhor %s"%(Nome_do_usuario))
            if numero == 4:
                a=("Falou chefe")
            if numero == 5:
                a=("Vou me desligar para economizar energia")
            
            print(a)
            engine.say(a)
            exit()


    #Códigos executados quando a inteligencia não sabe fazer algo
        if audio_tratado=="pegue água para mim" or audio_tratado=="pega água para mim" or audio_tratado=="cozinha para mim" or audio_tratado=="canta" or audio_tratado=="você sabe cantar" or audio_tratado=="faz um rap pra mim" or audio_tratado=="o que vai acontecer amanhã":
            numero = random.randint(1, 5)

            if numero == 1:
                a=("Eu não fui programada para isso")
            if numero == 2:
                a=("%s, você sabe que eu não sei fazer isso, você que me programou pombas!"%(Nome_do_usuario))
            if numero == 3:
                a=("Não sei como faz isso!")
            if numero == 4:
                a=("Isso você mesmo vai ter que fazer por que eu não sei fazer")
            if numero == 5:
                a=("Boa ordem, pena que eu não sei fazer isso! você vai ter que se virar")

            print(a)
            engine.say(a)


    #Modo bom dia
        if audio_tratado=="modo bom dia" or audio_tratado=="protocolo bom dia":
            print("Bom dia chefe! acabou de acordar? hahaha! bom independente disso os dados de hoje são")
            engine.say("Bom dia chefe! acabou de acordar? hahaha! bom independente disso os dados de hoje são")

            a=("%d e %d minutos" %(hora,minutos))
            engine.say(a)
            print(a)

            a = (busca + update)
            print(a)
            engine.say(a)

            print("Que o seu dia seja ótimo e cheio de felicidades, alias, lavar o rosto ajuda a acordar mais rápido e tomando um mate você vai ficar mais ativo, tenha um bom dia.")
            print("Modo bom dia encerrado")
            engine.say("Que o seu dia seja ótimo e cheio de felicidades, lavar o rosto ajuda a acordar mais rápido e tomando um mate você vai ficar mais ativo, tenha um bom dia. Modo bom dia encerrado")


    #Pesquisa comum no google
        if audio_tratado=="pesquisa no google":
            função_resposta_para_buscas()


    #Qual é a temperatura atual
        if audio_tratado=="qual é a temperatura atual" or audio_tratado=="agora estão quantos graus" or audio_tratado=="qual é a temperatura":
            a = (busca + update)
            print(a)
            engine.say(a)


#Fim do codigo
        engine.runAndWait()