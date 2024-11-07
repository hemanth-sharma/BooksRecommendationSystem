from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from nlp.recommendation import recommend_books
from nlp.feature_extraction import load_books_data, create_tfidf_matrix, get_book_descriptions

# Initialize router 
router = APIRouter()

# Load the books data and create Tf-IDF matrix 
filepath = "data/goodreads_books_clean.json"
try:
    books_data = load_books_data(filepath)
    book_descriptions = get_book_descriptions(books_data)
    tfidf_matrix, tfidf_vectorizer = create_tfidf_matrix(book_descriptions)
except Exception as e:
    raise RuntimeError(f"Error initializeing model: {e} ")


# User input: pydantic model
class RecommendationQuery(BaseModel):
    user_input: str


@router.post("/recommend")
async def get_recommendations(request: RecommendationQuery):
    """
    Endpoint to get book recommendations based on user input.
    """
    try:
        recommendations = recommend_books(
            request.user_input, tfidf_matrix, tfidf_vectorizer, books_data, top_n=5
        )
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {e}")
    