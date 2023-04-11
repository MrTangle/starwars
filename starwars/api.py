import requests


def get_people(): # Función para obtener todos los personajes
    people = [] # Hay que meter todos los datos de la API en un sitio, en este caso en una lista de diccionarios
    url = "https://swapi.dev/api/people/?format=json" # Guardamos la url de la api en una variable en formato json para no tener que formatear los datos
    while url:
        try:
            response = requests.get(url) # Pilla todos los datos de la url y los mete en un objeto response
            response = response.json() # Convierte el objeto response en un objeto json para poder trabajar con él
            people += response["results"] # Añadimos todos los personajes de una página a la lista people
            url = response.get("next") # Hacemos petición get a la url que aparece en la clave "next", que es la siguiente página, y la definimos como la nueva url a analizar
            
        except TimeoutError:
            print("Esto no responde, fuera.")
            break

    return people

#Hacer una función que meta en un diccionario a todos los personajes que están en people con las claves nombre, especie, altura y apariencias, 

def filter_people(people):
    nueva_lista = []

    for personaje in people:
        nuevo_diccionario = {
            'name': personaje['name'],
            'species': personaje['species'],
            'gender': personaje['gender'],
            'height': personaje['height']
        }
        nueva_lista.append(nuevo_diccionario)

    return nueva_lista


def order_people_by_height(nueva_lista):
    def get_height(personaje):
        try:
            return int(personaje["height"])
        except ValueError:
            return float('inf')

    return sorted(nueva_lista, key=get_height, reverse=True)

'''
def order_people_by_height(nueva_lista):
    return sorted(nueva_lista, key=lambda x: float(x["height"]), reverse=True)
'''