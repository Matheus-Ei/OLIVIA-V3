import cv2
import face_recognition
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import *
import numpy as np
import time
import win32gui
import win32con


def app_na_frente(app_title):
    # Encontre o identificador da janela do aplicativo pelo título
    app_window = win32gui.FindWindow(None, app_title)

    if app_window:
        try:
            # Defina o aplicativo como a janela ativa
            win32gui.SetForegroundWindow(app_window)

            # Defina a janela do aplicativo como "topmost" (acima das outras janelas)
            win32gui.SetWindowPos(app_window, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

            # Opcionalmente, restaure a janela (caso esteja minimizada)
            win32gui.ShowWindow(app_window, win32con.SW_RESTORE)
        except TypeError:
            print("#####@Erro de Tipo@#####")
        except win32gui.SetForegroundWindow:
            print('#####@Erro da SetForegroundWindow@#####')

    else:
        print("Aplicativo não encontrado")



def global_reconhecimento_facial():
    def reconhecimento_facial():
        global retorno
        def pre_processamento(imagem):
            gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            return gray

        # Carregar o modelo pré-treinado para detecção de faces
        detector_rosto = cv2.CascadeClassifier("Classes\ReconhecimentoFacial\haarcascade_frontalface_default.xml")

        # Iniciar a captura de vídeo da câmera
        captura = cv2.VideoCapture(0)
        show_camera(captura)

        def capturar_imagens(caminho, nome_pessoa, quantidade_imagens):
            contador = 0
            imagens = []

            while contador < quantidade_imagens:
                ret, frame = captura.read()
                gray = pre_processamento(frame)
                faces = detector_rosto.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                tamanho_face = (100, 100)

                for (x, y, w, h) in faces:
                    roi_gray = cv2.resize(gray[y:y+h, x:x+w], tamanho_face)
                    caminho_imagem = caminho + "/" + nome_pessoa + "_" + str(contador) + ".jpg"
                    cv2.imwrite(caminho_imagem, roi_gray)
                    imagens.append(roi_gray)
                    contador += 1
                
                try:
                    # Desenhar um retângulo ao redor da face
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                except UnboundLocalError:
                    print("Nenhuma Face Detectada...")

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            return imagens

        caminho_pasta = "Classes\ReconhecimentoFacial\Faces"
        nome_pessoa = "Matheus"
        quantidade_imagens = 1

        imagens_capturadas = capturar_imagens(caminho_pasta, nome_pessoa, quantidade_imagens)




        # Carregar imagem em que deseja realizar o reconhecimento facial
        Referencia = face_recognition.load_image_file("Classes\ReconhecimentoFacial\Faces\Cadastros\Matheus_1.jpg")
        Referencia_encode = face_recognition.face_encodings(Referencia)[0]

        Retorno_loop = True
        while Retorno_loop == True:
            try:
                Camera = face_recognition.load_image_file("Classes\ReconhecimentoFacial\Faces\Matheus_0.jpg")
                Camera_encode = face_recognition.face_encodings(Camera)[0]
                Retorno_loop = False
            except IndexError:
                imagens_capturadas = capturar_imagens(caminho_pasta, nome_pessoa, quantidade_imagens)
                print("Falha no reconhecimento, fique parado para refazer...")

        # Comparar o rosto encontrado com o rosto de referência
        matches = face_recognition.compare_faces([Referencia_encode], Camera_encode)

        if matches == [True]:
            cv2.destroyAllWindows()
            return True

        else:
            cv2.destroyAllWindows()
            return False
        




    import cv2

    def detect_faces(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('Classes/ReconhecimentoFacial/haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        draw_rectangles(frame, faces)
        return faces

    def draw_rectangles(frame, faces):
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    def show_camera(cap):
        start_time = time.time()
        while True:
            ret, frame = cap.read()  # Ler o próximo frame da câmera
            detect_faces(frame)
            if ret:
                cv2.imshow("Visualizador de Camera", frame)
                app_na_frente("Visualizador de Camera")

            # Verifique se a tecla 'q' foi pressionada para sair do loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Verifique se passaram 3 segundos
            current_time = time.time()
            if current_time - start_time >= 3:
                return
        # Feche a janela da câmera e libere os recursos
        cap.release()
        cv2.destroyAllWindows()

    if reconhecimento_facial():
        return True
    else:
        return False