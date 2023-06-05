import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pickle

# Dados de treinamento
frases = ["abrir aplicativo", "que horas são?", "tchau, falou", "desligar o sistema", "sair do sistema", "reiniciar sistema", "mudar de assunto", "abrir o gerenciador de tarefas", "abrir a visão fas tarefas", "criar uma nova area de trabalho", "deletar uma area de trabalho", "area de trabalho anterior", "proxima area de trabalho", "pular essa musica vai para a proxima", "pausar essa musica", "toque a musica", "selecionar uma musica", "selecionar uma playlist", "gerar uma imagem", "gerar uma senha"]
classes = ["abrirApp", "horario", "desligarCode", "desligarWindows", "sairWindows", "reiniciarWindows", "mudarAssunto", "abrirGerenciadorTarefas", "visaoTarefas", "novaAreaTrabalho", "deletarAreaTrabalho", "moverAreaTrabalhoEsquerda", "moverAreaTrabalhoDireita", "pularMusica", "pausarMusica", "playMusica", "selecionarMusica", "selecionarPlaylist", "gerarImagem", "gerarSenha"]
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
model.add(layers.Dense(len(classes), activation="softmax"))  # Camada de saída com um neurônio para cada classe

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Treinamento do modelo
model.fit(padded_sequences, labels, epochs=10000)

# Salvando o tokenizer e o modelo treinado
with open(r"neuralNetwork\sentenceClassifier\tokenizer.pickle", "wb") as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
model.save(r"neuralNetwork\sentenceClassifier\modelo_classificador")
