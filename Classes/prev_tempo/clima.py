# Imports
import requests
import json


# Faz a Previsão do Tempo
def previsao_do_tempo():
    # Insira sua chave da API do OpenWeatherMap
    API_KEY = '2537c1c37c801829837044d807c5f94d'
    
    # Insira o nome da cidade para a qual deseja obter a previsão do tempo
    cidade = 'Chapeco'
    # Monta a URL para a chamada da API
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}'
    # Faz a chamada da API
    response = requests.get(url)
    # Verifica se a chamada foi bem-sucedida
    data = json.loads(response.text)
    # Extrai as informações relevantes da resposta da API
    temperatura = data['main']['temp']
    descricao = data['weather'][0]['description']
    # Exibe a previsão do tempo
    print(f'Previsão do tempo para {cidade}:')
    print(f'Temperatura: {temperatura}°C')
    print(f'Descrição: {descricao}')
