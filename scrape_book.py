import requests
from bs4 import BeautifulSoup
import csv

# Définir l'URL de la page du livre
url = 'https://books.toscrape.com/catalogue/walt-disneys-alice-in-wonderland_777/index.html'

# Faire une requête HTTP pour récupérer le contenu de la page
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extraire les données nécessaires
    product_page_url = url
    upc_element = soup.find('th', string='UPC')
    upc = upc_element.find_next('td').text if upc_element else None

    title = soup.find('h1').text
    # Extraire le prix TTC
    price_including_tax_element = soup.find('p', class_='price_color')
    price_including_tax = price_including_tax_element.text.strip() if price_including_tax_element else None

    # Extraire le prix HT en cherchant un élément spécifique contenant cette information
    price_excluding_tax_element = soup.find('p', class_='price_excluding_tax')
    price_excluding_tax = price_excluding_tax_element.text.strip() if price_excluding_tax_element else None

    # Extraire le nombre disponible
    number_available = soup.find('p', class_='instock availability').text.strip()

    # Extraire la description du produit
    product_description = soup.find('meta', attrs={'name': 'description'})['content']

    # Extraire la catégorie
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()

    # Extraire la note de révision
    review_rating = soup.find('p', class_='star-rating')['class'][1]

    # Extraire l'URL de l'image
    image_url = soup.find('div', class_='item active').find('img')['src']

    # Enregistrer les données dans un fichier CSV
    with open('book_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Écrire les en-têtes de colonnes
        writer.writerow(['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
      
        # Écrire les données extraites dans le fichier CSV
        writer.writerow([product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
else:
    print('La requête a échoué')
    


# URL de la catégorie "Children's"
url_book = 'https://books.toscrape.com/catalogue/category/books/childrens_11/page-1.html'

def scrape_category_books(url_book):
    all_books_data = []  # Liste pour stocker les données de tous les livres

    # Fonction pour extraire les données de tous les livres d'une page
    def scrape_page_books(url_book):
        response = requests.get(url_book)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            books = soup.find_all('article', class_='product_pod')
            for book in books:
                # Extraire les données du livre et les ajouter à la liste
                book_data = extract_book_data(book)
                all_books_data.append(book_data)
            
            # Trouver le lien vers la page suivante et appeler récursivement la fonction si nécessaire
            next_page_link = soup.find('li', class_='next')
            if next_page_link:
                next_page_url = 'https://books.toscrape.com/catalogue/category/books/childrens_11/page-2.html' + next_page_link.find('a')['href'] 
                scrape_page_books(next_page_url)

    # Fonction pour extraire les données d'un livre à partir de sa balise HTML
    def extract_book_data(book):
        # Initialiser un dictionnaire pour stocker les données du livre
        book_data = {}

        # Code pour extraire les données du livre à partir de la balise 'book'
        product_page_url = 'https://books.toscrape.com/catalogue' + book.find('h3').find('a')['href']
        upc = book.find('p', class_='star-rating')['class'][1]
        title = book.find('h3').find('a').text
        price_including_tax = book.find('p', class_='price_color').text

        price_excluding_tax = book.find_all('p')[2].text
        
        number_available = book.find('p', class_='instock availability').text.strip()

        # Extraire la description du produit
        product_description_tag = book.find('meta', attrs={'name': 'description'})
        product_description = product_description_tag['content'] if product_description_tag else None
    
        category = 'Childrens'
        review_rating = book.find('p', class_='star-rating')['class'][1]
        image_url = 'https://books.toscrape.com/' + book.find('img')['src']
      
        # Ajoutez les données extraites au dictionnaire
        book_data['product_page_url'] = product_page_url
        book_data['universal_product_code (upc)'] = upc
        book_data['title'] = title
        book_data['price_including_tax'] = price_including_tax
        book_data['price_excluding_tax'] = price_excluding_tax
        book_data['number_available'] = number_available
        book_data['product_description'] = product_description
        book_data['category'] = category
        book_data['review_rating'] = review_rating
        book_data['image_url'] = image_url
        # Afficher les données du livre pour déboguer
        print(book_data)

        # Retourner le dictionnaire contenant les données du livre
        return book_data

    # Appeler la fonction pour extraire les données de tous les livres de la catégorie
    scrape_page_books(url_book)

    # Écrire les données dans un fichier CSV
    with open('category_books.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['product_page_url', 'universal_product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'] 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for book_data in all_books_data:
            writer.writerow(book_data)

# Appel de la fonction principale pour commencer le scraping
scrape_category_books(url_book)
