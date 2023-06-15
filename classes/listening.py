import speech_recognition as sr



def listening():
    # Creating the Speach Recognition and defines the openai key
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("->starting audio adjustment<-")
        r.adjust_for_ambient_noise(source, duration=1) # Time to ajust the microfone recognition with the sound of the ambient
        print("->given fit<-")
        print("initialization...\n")
        while True:
            print("listening...\n")
            try:
                basicAudio = r.listen(source)
                textAudio=(r.recognize_google(basicAudio, language="pt-br"))
                textAudio = textAudio.lower() 
                print(textAudio)
                return textAudio

            except sr.UnknownValueError:
                print("#####@ ERROR @#####")