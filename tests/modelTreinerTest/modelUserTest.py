import tensorflow as tf
from tensorflow import keras
import pickle

# Carregando o tokenizer e o modelo
with open(r"tests\modelTreinerTest\modeltreiner\tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)
model = keras.models.load_model(r"tests\modelTreinerTest\modeltreiner\modelo_classificador")

# Função para classificar frases
def classificar_frase(frase):
    # Pré-processamento da frase de entrada
    sequence = tokenizer.texts_to_sequences([frase])
    padded_sequence = keras.preprocessing.sequence.pad_sequences(sequence, maxlen=model.input_shape[1], padding="post")
    
    # Fazendo a predição
    prediction = model.predict(padded_sequence)
    predicted_class_index = tf.argmax(prediction, axis=1).numpy()[0]
    
    # Carregando frases e classes do arquivo de texto
    frases = []
    classes = []
    with open(r"tests\modelTreinerTest\modeltreiner\frases_classes.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                frases_classes = line.split(",")
                frases.extend(frases_classes[0].split(";"))
                classes.extend([frases_classes[1]])

    predicted_class = classes[predicted_class_index]
    
    return predicted_class

# Exemplo de uso
while True:
    frase = input("Diga a frase que você deseja classificar: ")
    resultado = classificar_frase(frase)
    print(frase, "=> Classe:", resultado)

