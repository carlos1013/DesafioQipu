import requests
from bs4 import BeautifulSoup

print("Digite o código ICAO desejado: ", end="")
icao = input()

try:
    html_request = requests.get('https://aisweb.decea.mil.br/?i=aerodromos&codigo=' + icao)
    if html_request.status_code != 200:
        #TODO - change this error message
        print('Não foi possível acessar as informações da página, tente novamente')
        exit()
except:
    print("Uma exceção ocorreu durante a requisição da página, tente novamente")
    exit()

soup = BeautifulSoup(html_request.content, 'html.parser')

# Search response for any alert div with "O aeródromo não foi encontrado" as content
# In this case ICAO is invalid
for div in soup.findAll("div", {"class": "alert"}):
    if "O aeródromo não foi encontrado" in str(div):
        print ("Aeródromo com o código ICAO fornecido não encontrado!")
        exit()