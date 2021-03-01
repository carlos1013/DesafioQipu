import requests

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

print(html_request)