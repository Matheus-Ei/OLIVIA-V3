# Imports
import speech_recognition
import pyttsx3
import threading
import pyodbc
import random
import datetime





# Main funcion to back-end
def code():

    # Creating the connection with the database
    conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=database\mainDb.accdb;'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()


    # Funcion to consult the questions to PROMETEU and check if they are in database
    def question(question, textAudio):
        try:
            # Execute a consult
            cursor.execute('SELECT perg FROM perguntas WHERE func = '+"'"+question+"';")
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
            cursor.execute('SELECT resp FROM respostas WHERE func = '+"'"+answer+"';")
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

    # Função para logs na tabela logs no banco de dados
    def logs(textAudio, response):
        time=datetime.now() 
        hour = int(time.strftime("%H"))
        minutes = int(time.strftime("%M"))
        seconds = time.strftime("%S")
        day = time.strftime("%d")
        week = time.strftime("%A")
        mount = time.strftime("%B")
        year = time.strftime("%Y")
        try:
            # Defines the date
            date = str(year+"/"+mount+"/"+day+":"+week+"/"+hour+":"+minutes+":"+seconds)
            cursor.execute("INSERT INTO logs(usuario, jarvis, data) VALUES ('"+textAudio+"','"+response+"','"+date+"');")
            # Save the alterations in the logs tabble
            conn.commit()
        # If haves a exeption the code prints what exeption have
        except pyodbc.Error as e:
            print(e)















# Interface to put the password and the loggin
if __name__ == "__main__":    
    if True:
        # Starts a thread to the back-end code
        thread_code = threading.Thread(target=code)
        thread_code.start()

    # If the password or the loggin is incorrect the code executes the else
    else:
        exit()