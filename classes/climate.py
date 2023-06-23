# Imports
import requests
import json


# Does the climate prevision
def getPrevision(city):
    API_KEY = '2537c1c37c801829837044d807c5f94d'  # Insire the api key
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url)
    data = json.loads(response.text)
    temperatura = data['main']['temp']
    descricao = data['weather'][0]['description']
    lista = []
    cidade = (f'Previsão do tempo para {city}:')
    temperaturageral = (f'Temperatura: {temperatura}°C')
    descricaoGeral = (f'Descrição: {descricao}')
    lista.append(cidade)
    lista.append(temperaturageral)
    lista.append(descricaoGeral)
    return(lista)