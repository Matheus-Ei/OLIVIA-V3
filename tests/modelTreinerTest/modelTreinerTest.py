import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pickle
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

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
            classes.extend([frases_classes[1]] * len(frases_classes[0].split(";")))
print(classes)
print(frases)

labels = np.zeros((len(frases), len(classes)))  # Matriz de rótulos inicialmente preenchida com zeros

# Atribui 1 aos rótulos correspondentes
for i, classe in enumerate(classes):
    labels[:, i] = np.array([classe == c for c in classes])

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
model.add(layers.GlobalAveragePooling1D())
model.add(Dense(units=16, activation='relu'))
model.add(layers.Reshape((1, -1)))  # Reshape para adicionar uma dimensão extra
model.add(LSTM(128))
model.add(Dropout(0.2))
model.add(Dense(units=16, activation='relu'))
model.add(Dropout(0.2))
model.add(layers.Dense(len(classes), activation="softmax"))  # Camada de saída com um neurônio para cada classe

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Treinamento do modelo
model.fit(padded_sequences, labels, epochs=3000)

# Salvando o tokenizer e o modelo treinado
with open(r"tests\modelTreinerTest\modeltreiner\tokenizer.pickle", "wb") as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
model.save(r"tests\modelTreinerTest\modeltreiner\modelo_classificador")