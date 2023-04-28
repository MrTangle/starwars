import requests
import csv
import io
import json


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


def ordered_top_ten_by_films(people):
    # Creamos un diccionario para llevar el conteo de apariciones de cada personaje
    num_films = {}

# Recorremos cada diccionario de personaje y contamos sus apariciones en las películas
    for person in people:
        for film_url in person["films"]:
            if film_url not in num_films:
                num_films[film_url] = 0
            num_films[film_url] += 1

# Ordenamos los personajes de mayor a menor número de apariciones
    ordered_people = sorted(people, key=lambda x: sum(num_films[f] for f in x["films"]), reverse=True)

# Obtenemos una lista con los 10 primeros personajes de la lista ordenada
    top10_people = ordered_people[:10]
    return top10_people


#Hacer una función que meta en un diccionario a todos los personajes que están en people con las claves nombre, especie, altura y apariencias, 

def filter_people(top10_people):
    filter_list = []

    for person in top10_people:
        new_dict = {
            'name': person['name'],
            'species': '',
            'gender': person['gender'],
            'height': person['height']
        }
        species_url = person['species'][0] if person['species'] else ''
        if species_url:
            species_response = requests.get(species_url)
            species_data = json.loads(species_response.text)
            species_name = species_data.get('name', '')
            new_dict['species'] = species_name
        filter_list.append(new_dict)

    return filter_list


def order_people_by_height(filter_list):
    def get_height(person):
        try:
            return int(person["height"])
        except ValueError:
            return float('inf')

    return sorted(filter_list, key=get_height, reverse=True)



def csv_to_httpbin(filter_list):
# Define la URL de httpbin
    url = 'https://httpbin.org/post'

    # Define las cabeceras del archivo CSV
    headers = {'Content-Type': 'text/csv'}

    # Crea una función para generar el archivo CSV en streaming
    def generate_csv(filter_list):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(filter_list[0].keys())
        for d in filter_list:
            writer.writerow(d.values())
            yield output.getvalue().encode('utf-8')
            output.seek(0)
            output.truncate(0)

    # Envía el archivo CSV a httpbin en streaming
    response = requests.post(url, headers=headers, data=generate_csv(filter_list), stream=True)

    # Imprime la respuesta de httpbin
    return response.text