from sklearn.feature_extraction.text import TfidfVectorizer
from nlp.text_processing import clean_text
import os 
import json


# Load the goodreads_books.json
def load_books_data(filepath):
    try:
        with open(filepath, "r") as file:
            books_data = json.load(file)
    except:
        return None

    return books_data


def create_tfidf_matrix(book_descriptions):
    """
    Create a Tf-IDF matrix for the given book description.
    """
    # tfidf_vectorizer = TfidfVectorizer()
    tfidf = TfidfVectorizer(stop_words='english', max_features=10000)
    tfidf_matrix = tfidf.fit_transform(book_descriptions)
    return tfidf_matrix, tfidf


def get_book_descriptions(books_data):
    """
    Clean and extract description from books data. 
    Add title and author to make it more efficent. 
    """
    cleaned_books = list()
    for book in books_data:
        text = book["description"] + " " + book["title"] + " " + book["author"] + " " + " ".join(book["genres"])
        cleaned_text = clean_text(text)
        cleaned_books.append(cleaned_text)
    
    return cleaned_books