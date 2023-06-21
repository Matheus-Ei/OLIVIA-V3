from googlesearch import search
import requests
from bs4 import BeautifulSoup
import classes.openaiCodes as opp
import wikipediaapi

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


def searchWiki(query):
    # Criar uma instância da API da Wikipedia
    wiki_wiki = wikipediaapi.Wikipedia('pt')

    page_py = wiki_wiki.page(query)

    # Verificar se a página existe
    if page_py.exists():
        # Imprimir o título da página
        print("Título: %s" % page_py.title)
        print("")
    
        a=page_py.text
        
        aLength = len(a)
        if aLength > 500:
            if aLength > 1000:
                if aLength > 2000:
                    a = a[:aLength//6]
                else:
                    a = a[:aLength//4]  
            else:
                a = a[:aLength//2]
                


        responseopp = str(opp.chat("Explique o conteudo a seguir: " + a + "  não poupe detalhes, caso tenham detalhes como datas e informações imutaveis como localizações, não as mude e inclua na resposta"))
        return responseopp
    else:
        print("A página não foi encontrada.")