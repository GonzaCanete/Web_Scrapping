import bs4
import requests
import pandas as pd

# crear url sin numero de pagina
url_base = 'https://books.toscrape.com/catalogue/page-{}.html'

# lista de datos de libros
libros_rating_alto = []

# iterar paginas
for pagina in range(1, 51):
    url_pagina = url_base.format(pagina)
    resultado = requests.get(url_pagina)
    sopa = bs4.BeautifulSoup(resultado.text, 'lxml')

    # seleccionar libros
    libros = sopa.select('.product_pod')

    for libro in libros:
        # chequear que tengan 4 o 5 estrellas
        if libro.select_one('.star-rating.Four') or libro.select_one('.star-rating.Five'):
            # titulo
            titulo = libro.h3.a['title']
            # precio
            precio = libro.select_one('.price_color').get_text()
            # rating (saca la segunda clase de "star-rating X")
            rating = libro.p['class'][1]

            # guardar datos en lista
            libros_rating_alto.append([titulo, precio, rating])

# guardar en CSV con pandas
df = pd.DataFrame(libros_rating_alto, columns=['Titulo', 'Precio', 'Rating'])
df.to_csv('Python/web scrapping/libros_rating_alto.csv', index=False, encoding='utf-8')

print("Datos guardados en libros_rating_alto.csv")


