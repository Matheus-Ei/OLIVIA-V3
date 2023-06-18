from googlesearch import search
import requests
from bs4 import BeautifulSoup
import classes.openaiii as opp

def searchGoogle(query):
    a = " "
    # Search Google
    for j in search(query, num_results=1):
        #print(j)

        response = requests.get(url=j)
        #print(response)

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the information you need
        title = soup.find('title').get_text()
        paragraphs = [p.get_text() for p in soup.find_all('p')]

        # Print the information in a nicely formatted way
        print('Title: {}\n'.format(title))
        print('Paragraphs:')
        for p in paragraphs:
            a = a + " " + p
        aLength = len(a)
        if aLength > 500:
            a = a[:aLength//2]
            print(a)


    responseopp = str(opp.chat("Explique o conteudo a seguir: " + a + "  não poupe detalhes, caso tenham detalhes como datas e informações imutaveis como localizações, não as mude e inclua na resposta"))
    print(responseopp)
    return(responseopp)