import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def fetch_book_info(session, book_url):
    try:
        async with session.get(book_url) as response:
            response.raise_for_status()
            soup = BeautifulSoup(await response.text(), 'html.parser')

            book_info = {
                'url': book_url,
                'title': soup.find('h1', class_='Text__title1').get_text(strip=True),
                'author': soup.find('span', class_='ContributorLink__name').get_text(strip=True),
                'rating_stars': soup.find('div', class_='RatingStatistics__rating').get_text(strip=True),
                'rating_count': soup.find('span', attrs={'data-testid': 'ratingsCount'}).get_text(strip=True),
                'reviews': soup.find('span', attrs={'data-testid': 'reviewsCount'}).get_text(strip=True),
                'description': soup.find('div', class_='BookPageMetadataSection__description').get_text(strip=True),
                'genres': [genre.get_text(strip=True) for genre in soup.find_all('span', class_='BookPageMetadataSection__genreButton')],
                'pagecount': soup.find('p', attrs={'data-testid': 'pagesFormat'}).get_text(strip=True),
                'published_date': soup.find('p', attrs={'data-testid': 'publicationInfo'}).get_text(strip=True),
                'language': "English"  
            }

            # # Targeting EditionDetails class
            # edition_details_div = soup.find('div', class_='EditionDetails')
            # if edition_details_div:
            #     edition_details_all_divs = edition_details_div.find_all('div', class_="TruncatedContent")
            #     if len(edition_details_all_divs) >= 4:
            #         book_info['isbn'] = edition_details_all_divs[2].get_text(strip=True)
            #         book_info['asin'] = edition_details_all_divs[3].get_text(strip=True)
            
            return book_info

    except Exception as e:
        logging.error(f"Error while scraping {book_url}: {e}")
        return None

async def run_data_scrapper():
    books_data = []
    books_df = pd.read_json("data/goodreads_books_processed.json", lines=True)
    
    # max_books = 50
    # books_df = books_df.head(max_books)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_book_info(session, books_df.iloc[i]['url']) for i in range(len(books_df))]
        books_data = await asyncio.gather(*tasks) # excecuting all tasks concurrently 

    # Remove None 
    books_data = [book for book in books_data if book is not None]

    # # Save to JSON file
    with open('goodreads_books_extracted.json', 'w') as json_file:
        json.dump(books_data, json_file, indent=4)
    
    logging.info(f"Scraped data for {len(books_data)} books.")


