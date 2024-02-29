import requests
import csv
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urljoin
import csv
import matplotlib.pyplot as plt
soup = BeautifulSoup("<html><p>This is <b>invalid HTML</p></html>", "html.parser")
req = requests.get('https://en.wikipedia.org/wiki/Python_(programming_language)')


##Partie I##

    # Définir l'URL de la page du livre
url = 'https://books.toscrape.com/catalogue/walt-disneys-alice-in-wonderland_777/index.html'

# Faire une requête HTTP pour récupérer le contenu de la page
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
        
    product_page_url = url

    upc_element = soup.find('th', string='UPC')
    upc = upc_element.find_next('td').text if upc_element else None

    title = soup.find('h1').text
        
    price_including_tax_element = soup.select_one('table.table-striped tr:nth-child(4) td')
    price_including_tax = price_including_tax_element.text.strip() if price_including_tax_element else None

    price_excluding_tax_element = soup.select_one('table.table-striped tr:nth-child(3) td')
    price_excluding_tax = price_excluding_tax_element.text.strip() if price_excluding_tax_element else None

    number_available_element = soup.select_one('table.table-striped tr:nth-child(6) td')
    number_available = number_available_element.text.strip() if number_available_element else ''

    product_description = soup.find('meta', attrs={'name': 'description'})['content']

    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()

    review_rating = soup.find('p', class_='star-rating')['class'][1]

    image_url = soup.find('div', class_='item active').find('img')['src']


        # Enregistrer les données dans un fichier CSV
    with open('book_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
        
        writer.writerow([product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
else:
    print('La requête a échoué')
        


###Partie II####

def extract_category_urls(category_url):
    
    book_urls = []

    response = requests.get(category_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        books = soup.find_all('h3')  
        for book in books:
            book_url = book.find('a')['href']  
            book_url = urllib.parse.urljoin(category_url, book_url)
            book_urls.append(book_url)

        # Check for pagination and extract book URLs from other pages if necessary
        next_page = soup.find('li', class_='next')
        if next_page:
            next_page_url = next_page.find('a')['href']
            next_page_url = urllib.parse.urljoin(category_url, next_page_url)
            book_urls += extract_category_urls(next_page_url)

    return book_urls

# Test the function with the Travel category URL
category_url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'
travel_book_urls = extract_category_urls(category_url)
print(travel_book_urls)

def extract_book_data(book_url):
    
    book_data = {}

    response = requests.get(book_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        book_data['product_page_url'] = book_url
        book_data['universal_product_code'] = soup.find('th', string='UPC').find_next('td').text.strip()
        book_data['title'] = soup.find('h1').text.strip()
        book_data['price_including_tax'] = soup.select_one('table.table-striped tr:nth-child(4) td').text.strip()
        book_data['price_excluding_tax'] = soup.select_one('table.table-striped tr:nth-child(3) td').text.strip()
        book_data['number_available'] = soup.select_one('table.table-striped tr:nth-child(6) td').text.strip()
        book_data['product_description'] = soup.find('meta', attrs={'name': 'description'})['content']
        book_data['category'] = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
        book_data['review_rating'] = soup.find('p', class_='star-rating')['class'][1]
        book_data['image_url'] = soup.find('div', class_='item active').find('img')['src']

    return book_data

def extract_books_data(category_urls):
    
    books_data = []

    for book_url in category_urls:
        book_data = extract_book_data(book_url)
        books_data.append(book_data)

    return books_data

def write_to_csv(data, filename):
    
    if data:
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f'Data has been written to {filename}')
    else:
        print('No data to write.')

category_url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'
travel_book_urls = extract_category_urls(category_url)

travel_books_data = extract_books_data(travel_book_urls)

write_to_csv(travel_books_data, 'travel_books.csv')



###Partie III###



def extract_category_urls(category_url):
    book_urls = []
    response = requests.get(category_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        books = soup.find_all('h3')
        for book in books:
            book_url = book.find('a')['href']
            book_url = urllib.parse.urljoin(category_url, book_url)
            book_urls.append(book_url)
        next_page = soup.find('li', class_='next')
        if next_page:
            next_page_url = next_page.find('a')['href']
            next_page_url = urllib.parse.urljoin(category_url, next_page_url)
            book_urls += extract_category_urls(next_page_url)
    return book_urls

def extract_book_data(book_url):
    book_data = {}
    response = requests.get(book_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        book_data['product_page_url'] = book_url
        book_data['universal_product_code'] = soup.find('th', string='UPC').find_next('td').text.strip()
        book_data['title'] = soup.find('h1').text.strip()
        book_data['price_including_tax'] = soup.select_one('table.table-striped tr:nth-child(4) td').text.strip()
        book_data['price_excluding_tax'] = soup.select_one('table.table-striped tr:nth-child(3) td').text.strip()
        book_data['number_available'] = soup.select_one('table.table-striped tr:nth-child(6) td').text.strip()
        book_data['product_description'] = soup.find('meta', attrs={'name': 'description'})['content']
        book_data['category'] = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
        book_data['review_rating'] = soup.find('p', class_='star-rating')['class'][1]
        book_data['image_url'] = soup.find('div', class_='item active').find('img')['src']
    return book_data


def extract_books_data(category_urls):
    all_books_data = []
    for category_url in category_urls:
        book_urls = extract_category_urls(category_url)
        category_books_data = []  # Stocker les données de chaque catégorie
        for book_url in book_urls:
            book_data = extract_book_data(book_url)
            category_books_data.append(book_data)
        all_books_data.append(category_books_data)  # Ajouter les données de la catégorie
    return all_books_data

def write_to_csv(data, filename):
    if data:
        keys = data[0].keys()  # Vérifier si la liste n'est pas vide avant d'accéder à l'élément à l'index 0
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f'Data has been written to {filename}')
    else:
        print('No data to write.')

# URLs des catégories de livres
category_urls = [
    'https://books.toscrape.com/catalogue/category/books/travel_2/index.html',
    'https://books.toscrape.com/catalogue/category/books/mystery_3/index.html',
    'https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html',
    'https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html',
    'https://books.toscrape.com/catalogue/category/books/classics_6/index.html',
    'https://books.toscrape.com/catalogue/category/books/philosophy_7/index.htmls',
    'https://books.toscrape.com/catalogue/category/books/romance_8/index.html',
    'https://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html',
    'https://books.toscrape.com/catalogue/category/books/fiction_10/index.html',
    'https://books.toscrape.com/catalogue/category/books/childrens_11/index.html',
    'https://books.toscrape.com/catalogue/category/books/religion_12/index.html',
    'https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html',
    'https://books.toscrape.com/catalogue/category/books/music_14/index.html',
    'https://books.toscrape.com/catalogue/category/books/default_15/index.html',
    'https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html',
    'https://books.toscrape.com/catalogue/category/books/sports-and-games_17/index.html',
    'https://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html',
    'https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html',
    'https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html'
    'https://books.toscrape.com/catalogue/category/books/new-adult_20/index.html',
    'https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html',
    'https://books.toscrape.com/catalogue/category/books/science_22/index.html',
    'https://books.toscrape.com/catalogue/category/books/poetry_23/index.html',
    'https://books.toscrape.com/catalogue/category/books/paranormal_24/index.html',
    'https://books.toscrape.com/catalogue/category/books/art_25/index.html',
    'https://books.toscrape.com/catalogue/category/books/psychology_26/index.html',
    'https://books.toscrape.com/catalogue/category/books/psychology_26/index.html',
    'https://books.toscrape.com/catalogue/category/books/parenting_28/index.html',
    'https://books.toscrape.com/catalogue/category/books/adult-fiction_29/index.html',
    'https://books.toscrape.com/catalogue/category/books/humor_30/index.html',
    'https://books.toscrape.com/catalogue/category/books/horror_31/index.html',
    'https://books.toscrape.com/catalogue/category/books/history_32/index.html',
    'https://books.toscrape.com/catalogue/category/books/food-and-drink_33/index.html',
    'https://books.toscrape.com/catalogue/category/books/christian-fiction_34/index.html',
    'https://books.toscrape.com/catalogue/category/books/business_35/index.html',
    'https://books.toscrape.com/catalogue/category/books/biography_36/index.html',
    'https://books.toscrape.com/catalogue/category/books/thriller_37/index.html',
    'https://books.toscrape.com/catalogue/category/books/contemporary_38/index.html',
    'https://books.toscrape.com/catalogue/category/books/spirituality_39/index.html',
    'https://books.toscrape.com/catalogue/category/books/academic_40/index.html',
    'https://books.toscrape.com/catalogue/category/books/self-help_41/index.html',
    'https://books.toscrape.com/catalogue/category/books/self-help_41/index.html',
    'https://books.toscrape.com/catalogue/category/books/christian_43/index.html',
    'https://books.toscrape.com/catalogue/category/books/suspense_44/index.html',
    'https://books.toscrape.com/catalogue/category/books/short-stories_45/index.html',
    'https://books.toscrape.com/catalogue/category/books/novels_46/index.html',
    'https://books.toscrape.com/catalogue/category/books/health_47/index.html',
    'https://books.toscrape.com/catalogue/category/books/politics_48/index.html',
    'https://books.toscrape.com/catalogue/category/books/cultural_49/index.html',
    'https://books.toscrape.com/catalogue/category/books/erotica_50/index.html',
    'https://books.toscrape.com/catalogue/category/books/crime_51/index.html'
    # Ajoutez ici les autres URLS de catégories de livres
]

# Extraire les données de tous les livres
books_data = extract_books_data(category_urls)

# Écrire les données dans des fichiers CSV distincts pour chaque catégorie
for idx, category_data in enumerate(books_data):
    category_name = category_urls[idx].split('/')[-2].lower().replace(' ', '_')  # Extraire le nom de la catégorie
    filename = f'{category_name}_books.csv'
    write_to_csv(category_data, filename)



###Partie IV####
# Fonction pour télécharger les images
from urllib.parse import urljoin

# Fonction pour télécharger les images
def download_images(books_data):
    for category_books in books_data:
        for book_data in category_books:
            image_url = book_data['image_url']
            # Construire l'URL absolue de l'image
            absolute_image_url = urljoin('https://books.toscrape.com/catalogue/', image_url)
            # Télécharger l'image
            response = requests.get(absolute_image_url)
            if response.status_code == 200:
                # Extraire le nom de fichier à partir de l'URL
                image_filename = image_url.split('/')[-1]
                # Enregistrer l'image avec le nom de fichier approprié dans le dossier "images"
                with open(f'images/{image_filename}', 'wb') as f:
                    f.write(response.content)
                print(f"Image {image_filename} téléchargée avec succès.")
            else:
                print(f"Erreur lors du téléchargement de l'image {image_url}: {response.status_code}")

# Appel de la fonction pour télécharger les images
download_images(books_data)



###Bonus I###
# Fonction pour calculer le nombre de livres par catégorie
def count_books_per_category(books_data):
    books_per_category = {}
    for category_books in books_data:
        for book_data in category_books:
            category = book_data['category']
            if category in books_per_category:
                books_per_category[category] += 1
            else:
                books_per_category[category] = 1
    return books_per_category

# Appel de la fonction pour calculer le nombre de livres par catégorie
books_per_category = count_books_per_category(books_data)

# Écriture des données dans un fichier CSV
with open('books_per_category.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Category', 'Number of Books'])
    for category, count in books_per_category.items():
        writer.writerow([category, count])

# Création du diagramme circulaire
categories = list(books_per_category.keys())
book_counts = list(books_per_category.values())

plt.figure(figsize=(10, 6))
plt.pie(book_counts, labels=categories, autopct='%1.1f%%', startangle=140)
plt.title('Number of Books per Category')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
