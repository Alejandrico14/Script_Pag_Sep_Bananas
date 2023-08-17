import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Tipos de libros
tag_books = ('LMP', 'MLA', 'PAA', 'PCA', 'PEA', 'SDA', 'TPA', 'CMA', 'SHA')

# URL bases para la descarga de las imágenes y la búsqueda del libro
base_url = 'https://www.conaliteg.sep.gob.mx/2023/c/'
base2_url = 'https://www.conaliteg.sep.gob.mx/2023/'

# Función para descargar imágenes
def descargar_imagenes(url, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    absolute_path = os.path.abspath(output_folder)
    base = "000"

    for img_cont in range(1, 400):
        img_num = f"{base}{img_cont}"[-len(base):]
        img_url = f'{url}{img_num}.jpg'
        img_name = img_url.split('/')[-1]
        img_path = os.path.join(output_folder, img_name)

        response = requests.get(img_url)

        if response.status_code == 200:
            with open(img_path, 'wb') as img_file:
                img_file.write(response.content)
            print(f'Imagen descargada: {img_name}')
        else:
            break

    return absolute_path

# Bucle para descargar imágenes
for i in range(0, 8):
    for tag in tag_books:
        try:
            # URL del libro y de búsqueda
            libro_url = f'{base_url}P{i}{tag}/'
            busqueda_url = f'{base2_url}P{i}{tag}.htm#page/2'

            response = requests.get(busqueda_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Buscar imágenes
            img_tags = soup.find_all('img')

            output_folder = f'P{i}{tag}'
            absolute_path = descargar_imagenes(libro_url, output_folder)

            print('Descarga completada.')
            print(f'Ruta absoluta de la carpeta de imágenes descargadas: {absolute_path}')

        except requests.exceptions.RequestException as e:
            print(f'No se pudo acceder a {libro_url}: {e}')
            continue
