# r"modelTreinerTest\modeltreiner\frases_classes.txt"
# r"modelTreinerTest\modeltreiner\tokenizer.pickle"
# r"modelTreinerTest\modeltreiner\modelo_classificador"


import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import regularizers
import pickle

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
            #classes.extend([frases_classes[1]] * len(frases_classes[0].split(";")))

# Transformando classes em um conjunto para obter todas as classes únicas
unique_classes = list(set(classes))

# Mapeando cada classe única para um índice numérico
class_to_index = {classe: i for i, classe in enumerate(unique_classes)}

# Convertendo as classes em rótulos numéricos
labels = np.array([class_to_index[classe] for classe in classes])

# Pré-processamento dos dados de entrada
tokenizer = keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(frases)
sequences = tokenizer.texts_to_sequences(frases)
vocab_size = len(tokenizer.word_index) + 1

# Padding para garantir que todas as sequências tenham o mesmo tamanho
max_length = max(len(seq) for seq in sequences)
padded_sequences = keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_length, padding="post")

# Modelo de rede neural
model = keras.Sequential()
model.add(layers.Embedding(vocab_size, 16, input_length=max_length))
model.add(layers.Bidirectional(layers.GRU(32, return_sequences=True)))
model.add(layers.Bidirectional(layers.GRU(32)))
model.add(layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(len(unique_classes), activation="softmax"))

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# Ajuste de hiperparâmetros e treinamento do modelo
model.fit(padded_sequences, labels, epochs=10000, batch_size=32, validation_split=0.2)

# Salvando o tokenizer e o modelo treinado
with open(r"tests\modelTreinerTest\modeltreiner\tokenizer.pickle", "wb") as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
model.save(r"tests\modelTreinerTest\modeltreiner\modelo_classificador")



