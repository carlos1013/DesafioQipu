import requests
from bs4 import BeautifulSoup, NavigableString

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

print()

# Print sunrise info
print("Nascer do sol:")
sunrise = soup.find(name='sunrise')
# If there isn't any sunrise tags, then this info is unavailable
if (sunrise == None):
    print("Não disponivel!")
else:
    print(sunrise.text)

# Print sunset info
print("Pôr do sol:")
sunset = soup.find(name='sunset')
# If there isn't any sunset tags, then this info is unavailable
if (sunset == None):
    print("Não disponivel!")
else:
    print(sunset.text)

print()

# Search for hr with "met" as Id
met_hr = soup.find("hr", {"id": "met"})
print("Informações TAF/METAR:")

if (met_hr == None):
    print("Não disponiveis!")
else:
    for tag in met_hr.next_siblings:
        if (tag.name == 'p' and tag.text != ""):
            print(tag.text)
        
        if (tag.name == 'h5'):
            print(tag.text + ":")

        if (tag.name == 'hr' and 'id' in tag.attrs and tag.attrs['id'] == 'cartas'):
            break


print()

cartas_hr = soup.find("hr", {"id": "cartas"})
if (cartas_hr == None):
    print("Cartas:")
    print("Não disponiveis!")
else:
    for tag in cartas_hr.next_siblings:
        if isinstance(tag, NavigableString):
            continue

        if tag.name == 'h4':
            print(tag.text + ":")

        if (tag.name == 'ul'):
            children = tag.findAll("a" , recursive=True)
            for child in children:
                print("    " + child.text + " (" + str(child.attrs['href']) + ")")

        if (tag.name == 'hr' and 'id' in tag.attrs and tag.attrs['id'] == 'rotas'):
            break