import requests
from bs4 import BeautifulSoup, NavigableString

print("Digite o código ICAO desejado: ", end="")
icao = input()

try:
    # Make request to aisweb.decea.mil.br passing ICAO received
    html_request = requests.get('https://aisweb.decea.mil.br/?i=aerodromos&codigo=' + icao)

    # Notify user if status code for request is different than 200
    if html_request.status_code != 200:
        print('A página não aceitou a requisição das informações do aerodromo, tente novamente')
        exit()
# Catch all exceptions during request and notify user
except:
    print("Uma exceção ocorreu durante a requisição da página, tente novamente")
    exit()

# Start BeautifulSoup with htmlrequest content
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
#find tag with "sunrise" name
sunrise = soup.find(name='sunrise')
# If there isn't any sunrise tags, then this info is unavailable
if (sunrise == None):
    print("Não disponivel!")
else:
    print(sunrise.text)

# Print sunset info
print("Pôr do sol:")
#find tag with "sunset" name
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

# In case TAF/METAR infos are not available let user know
if (met_hr == None):
    print("Não disponiveis!")
else:
    # Iterate over met_hr siblings, we don't have a div around these tags so we have to iterate in the same level
    for tag in met_hr.next_siblings:
        # Print text for "p" tags that don't have empty values
        if (tag.name == 'p' and tag.text != ""):
            print(tag.text)
        
        # Print with ":" for "h5" tags
        if (tag.name == 'h5'):
            print(tag.text + ":")

        # Using hr for the next session as a break point for this iteration because of tags in the same level
        if (tag.name == 'hr' and 'id' in tag.attrs and tag.attrs['id'] == 'cartas'):
            break


print()

# Search for hr with "cartas" as Id
cartas_hr = soup.find("hr", {"id": "cartas"})

# In case "cartas" infos are not available let user know
if (cartas_hr == None):
    print("Cartas:")
    print("Não disponiveis!")
else:
    # Iterate over cartas_hr siblings, we don't have a div around these tags so we have to iterate in the same level
    for tag in cartas_hr.next_siblings:
        # Ignore NavigableString objects found during iteration
        if isinstance(tag, NavigableString):
            continue
        
        # Print with ":" for "h4" tags
        if tag.name == 'h4':
            print(tag.text + ":")

        # For "ul" tags, search their children for "a" tags, each one of these tags represent a single "carta"
        if (tag.name == 'ul'):
            children = tag.findAll("a" , recursive=True)
            # For each "a" tag found print text and href attribute (link to "carta")
            for child in children:
                print("    " + child.text + " (" + str(child.attrs['href']) + ")")

        # Using hr for the next session as a break point for this iteration because of tags in the same level
        if (tag.name == 'hr' and 'id' in tag.attrs and tag.attrs['id'] == 'rotas'):
            break