
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nlp.feature_extraction import load_books_data, create_tfidf_matrix, get_book_descriptions

def get_user_input_vector(user_input, tfidf_vectorizer):
    """
    Convert the user's input into a TF-IDF vector.
    """
    return tfidf_vectorizer.transform([user_input])

def recommend_books(user_input, tfidf_matrix, tfidf_vectorizer, books_data, top_n=5):
    """
    Recommend books based on user input by calculating cosine similarity.
    """
    # Get the user's input vector
    user_vector = get_user_input_vector(user_input, tfidf_vectorizer)
    
    # Calculate the cosine similarity between the user's input and each book's description
    cosine_similarities = cosine_similarity(user_vector, tfidf_matrix)
    
    # Flatten the cosine similarity matrix (it will be a 2D array) and get the indices sorted by similarity
    similarity_scores = cosine_similarities.flatten()
    sorted_indices = np.argsort(similarity_scores, axis=0)[::-1]  # Sort in descending order
    
    # Get the top N most similar books
    top_books = []
    for index in sorted_indices[:top_n]:
        book = books_data[index]
        top_books.append({
            'url': book['url'],
            'title': book['title'],
            'author': book['author'],
            'description': book['description'],
            'similarity': similarity_scores[index],
            'genres': book['genres']

        })
    
    return top_books

