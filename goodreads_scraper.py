import requests
from bs4 import BeautifulSoup
import csv

def get_complete_url(book_url):
    res = book_url.split('?', 1)
    return 'https://www.goodreads.com' + res[0]

def get_book_genre(book_url):
    res = requests.get(book_url, headers={'User-Agent': 'Mozilla/5.0'})
    data = res.text
    soup = BeautifulSoup(data, 'html.parser')
    genre_tags = soup.find_all('a', class_='actionLinkLite bookPageGenreLink')
    genres = [tag.text.strip() for tag in genre_tags]
    return ', '.join(genres)

def scrape_goodreads_books(search_query, max_pages=5):
    books = []
    page_number = 1

    while page_number <= max_pages:
        res = requests.get(f"https://www.goodreads.com/search?q={search_query}&page={page_number}", headers={'User-Agent': 'Mozilla/5.0'})
        data = res.text
        soup = BeautifulSoup(data, 'html.parser')

        for i in soup.find_all('tr'):
            book_title_tag = i.find('a', class_="bookTitle")
            author_name_tag = i.find('a', class_="authorName")
            rating_tag = i.find('span', class_="minirating")

            if book_title_tag and author_name_tag and rating_tag:
                book_url = get_complete_url(book_title_tag['href'])
                genre = get_book_genre(book_url)

                book_info = {
                    'Book Title': book_title_tag.text.strip(),
                    'Author Name': author_name_tag.text.strip(),
                    'Url Book': book_url,
                    'Book Rating': rating_tag.text.strip().split(' ')[0],
                    'Genre': genre
                }
                books.append(book_info)

        if not soup.find('a', class_='next_page'):
            break

        page_number += 1

    for book in books:
        print('Author Name:', book['Author Name'])
        print('Book Title:', book['Book Title'])
        print('Url Book:', book['Url Book'])
        print('Book Rating:', book['Book Rating'])
        print('Genre:', book['Genre'])
        print("\n")

    csv_file = f"{search_query}_book_res.csv"
    
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)

    print(f'Data has been written to {csv_file}')

scrape_goodreads_books("Book", max_pages=5)
