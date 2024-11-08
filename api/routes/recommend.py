from fastapi import APIRouter, HTTPException, Form, Depends
from pydantic import BaseModel
from nlp.recommendation import recommend_books
from nlp.feature_extraction import load_books_data, create_tfidf_matrix, get_book_descriptions
from fastapi.templating import Jinja2Templates


# Initialize router 
router = APIRouter()

templates = Jinja2Templates(directory="api/templates")

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
    book_query: str

    @classmethod
    def as_form(cls, book_query: str= Form(...)):
        return cls(book_query=book_query)
        

@router.post("/recommend")
async def get_recommendations(request: RecommendationQuery = Depends(RecommendationQuery.as_form)):
    """
    Endpoint to get book recommendations based on user input.
    """
    print("request = ", request)
    try:
        books = recommend_books(
            request.book_query, tfidf_matrix, tfidf_vectorizer, books_data, top_n=5
        )
        return templates.TemplateResponse(
            "index.html", {"request": request.dict(), "books": books, "book_query": request.book_query}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {e}")
    