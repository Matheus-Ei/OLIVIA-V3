# Imports
import os
import pygame
from pydub import AudioSegment
from pydub.playback import play
import pyttsx3



# Function for normal speech, longer, but with better quality
def speak(data):
    voice = 'en-US-SteffanNeural'
    voice2 = 'pt-BR-AntonioNeural'
    voice3 = 'pt-BR-FranciscaNeural'
    data = data.replace('\n'," ")
    command = f'edge-tts --rate="+10%" --voice "{voice3}" --text "{data}" --write-media "sounds/voice/data.mp3"'
    os.system(command) # Sends the command to CMD

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/voice/data.mp3") # Loads the sound to pygame
    try:
        pygame.mixer.music.play() # Speack the text in the sound with pygame
        print("-> "+data+" <-")
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(e)
    
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()



# Function for fast speech, but with lower quality
def fast_speak(texto):
    engine = pyttsx3.init() # Starts the text-speack
    engine.save_to_file(texto, "Sons/data.mp3")
    engine.setProperty("rate", 400) # Speed Change
    engine.runAndWait()
    audio = AudioSegment.from_wav("Sons/data.mp3")
    volume_adjustment = 6 # Adjusts the volume
    audio = audio + volume_adjustment
    play(audio)