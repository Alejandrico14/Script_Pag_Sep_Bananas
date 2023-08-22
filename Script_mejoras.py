
#Aqui antes de hacer todo, debemos de instalar el "tqdm" que es una biblioteca para qué esto 
# si pueda funcionar sin muchos problemas 
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm  # Importa la clase tqdm para la barra de progreso

# Aquí tenemos los tipos de libros
tag_books = ('LMP', 'MLA', 'PAA', 'PCA', 'PEA', 'SDA', 'TPA', 'CMA', 'SHA')
base_url = 'https://www.conaliteg.sep.gob.mx/2023/c/'
base2_url = 'https://www.conaliteg.sep.gob.mx/2023/'

def descargar_imagenes(url, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    absolute_path = os.path.abspath(output_folder)
    base = "000"

    # Usar tqdm para mostrar la barra de progreso
    for img_cont in tqdm(range(1, 400), desc='Descargando imágenes'):
        img_num = f"{base}{img_cont}"[-len(base):]
        img_url = f'{url}{img_num}.jpg'
        img_name = img_url.split('/')[-1]
        img_path = os.path.join(output_folder, img_name)

        response = requests.get(img_url)

        if response.status_code == 200:
            with open(img_path, 'wb') as img_file:
                img_file.write(response.content)
        else:
            break

    return absolute_path

# Bucle para descargar imágenes
for i in range(0, 8):
    for tag in tag_books:
        try:
            libro_url = f'{base_url}P{i}{tag}/'
            busqueda_url = f'{base2_url}P{i}{tag}.htm#page/2'

            response = requests.get(busqueda_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            output_folder = f'P{i}{tag}'
            absolute_path = descargar_imagenes(libro_url, output_folder)

            print('Descarga completada.')
            print(f'Ruta absoluta de la carpeta de imágenes descargadas: {absolute_path}')

        except requests.exceptions.RequestException as e:
            print(f'No se pudo acceder a {libro_url}: {e}')
            continue
        except requests.exceptions.RequestException as e:
            print(f'No se pudo acceder a {libro_url}: {e}')
            continue
