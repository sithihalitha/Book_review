from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

app = FastAPI()


class Book(BaseModel):
    title: str
    author: str
    publication_year: int

class Review(BaseModel):
    text_review: str
    rating: int = Field(..., ge=1, le=5)


books_db = []
reviews_db = {}


def send_confirmation_email(review_id: int, email: str):
    print(f"Confirmation email sent for review ID {review_id} to {email}")


@app.post("/books/", response_model=Book)
def add_book(book: Book):
    """
    Endpoint to add a new book.

    Functionality:
    - Adds a new book to the system.

    Error Handling and Robustness:
    - Gracefully handles invalid requests.

    Returns:
    - Details of the added book.
    """
    books_db.append(book)
    return book


@app.post("/books/{book_id}/reviews/", response_model=Review)
async def submit_review(book_id: int, review: Review, background_tasks: BackgroundTasks):
    """
    Endpoint to submit a review for a specific book.

    Functionality:
    - Submits a review for a specific book.
    - Sends a confirmation email in the background.

    Error Handling and Robustness:
    - Handles cases where the book is not found.
    - Validates input data to ensure it meets requirements.

    Returns:
    - Submitted review details.
    """
    if book_id < 0 or book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")

    if not (1 <= review.rating <= 5):
        raise HTTPException(status_code=422, detail="Rating must be between 1 and 5")

    if book_id not in reviews_db:
        reviews_db[book_id] = []
    reviews_db[book_id].append(review)
    background_tasks.add_task(send_confirmation_email, len(reviews_db[book_id]), "user@example.com")
    return review


@app.get("/books/", response_model=List[Book])
def get_books(author: Optional[str] = None, publication_year: Optional[int] = None):
    """
    Endpoint to retrieve books with optional filters.

    Functionality:
    - Retrieves all books, with optional filters by author or publication year.

    Returns:
    - List of books matching the filters.
    """
    filtered_books = books_db
    if author:
        filtered_books = [book for book in filtered_books if book.author == author]
    if publication_year:
        filtered_books = [book for book in filtered_books if book.publication_year == publication_year]
    return filtered_books


@app.get("/books/{book_id}/reviews/", response_model=List[Review])
def get_reviews(book_id: int):
    """
    Endpoint to retrieve reviews for a specific book.

    Functionality:
    - Retrieves all reviews for a specific book.

    Error Handling and Robustness:
    - Handles cases where the book is not found.

    Returns:
    - List of reviews for the book.
    """
    if book_id < 0 or book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")
    return reviews_db.get(book_id, [])

# Exception handler for HTTP errors
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# Unit tests with FastAPI's test client
client = TestClient(app)

def test_add_book():
    response = client.post("/books/", json={"title": "Wings of Fire", "author": "A.P.J. Abdul Kalam", "publication_year": 1999})
    assert response.status_code == 200
    assert response.json() == {"title": "Wings of Fire", "author": "A.P.J. Abdul Kalam", "publication_year": 1999}

def test_submit_review():
    response = client.post("/books/0/reviews/", json={"text_review": "Great book!", "rating": 5})
    assert response.status_code == 200
    assert response.json() == {"text_review": "Great book!", "rating": 5}


if __name__ == "__main__":
    import uvicorn
   
