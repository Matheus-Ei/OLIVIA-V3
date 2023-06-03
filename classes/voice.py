# Imports
import os
import pygame
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import pyttsx3



# Função para fala normal, mais demorada, porem com qualidade melhor
def speak(data):
    voice = 'en-US-SteffanNeural'
    voice2 = 'pt-BR-AntonioNeural'
    voice3 = 'pt-BR-FranciscaNeural'

    data = data.replace('\n'," ")
    
    command = f'edge-tts --rate="+10%" --voice "{voice3}" --text "{data}" --write-media "Sons/data.mp3"'
    os.system(command)

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("Sons/data.mp3")
    

    try:
        pygame.mixer.music.play()
        print(data)

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(e)
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()



# Função para fala rápida, porem com qualidade menor
def fast_speak(texto):
    # Inicializa o mecanismo de síntese de voz
    engine = pyttsx3.init()
    # Sintetiza o texto
    engine.save_to_file(texto, "Sons/data.mp3")
    engine.setProperty("rate", 400)  # Aumenta a velocidade em 50%
    engine.runAndWait()
    # Carrega o áudio gerado
    audio = AudioSegment.from_wav("Sons/data.mp3")
    # Ajusta o volume (por exemplo, 6 dB para aumentar em 6 decibéis)
    volume_adjustment = 6
    audio = audio + volume_adjustment
    play(audio)