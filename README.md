# Book Review System

This is a RESTful API for a hypothetical book review system built using FastAPI.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/sithihalitha/Book_review.git

2. Navigate to the project directory

    cd Book-review

3. Create a virtual environment

4. pip install -r requirements.txt

5. uvicorn main:app --reload

        The API will be available at http://localhost:8000.


6. Endpoints
    Add a new book:
        Endpoint: POST /books/
        Request body: JSON object containing title, author, and publication_year.
    Submit a review for a book:
        Endpoint: POST /books/{book_id}/reviews/
        Request body: JSON object containing text_review and rating.
    Retrieve all books (with optional filters by author or publication year):
        Endpoint: GET /books/
    Retrieve all reviews for a specific book:
        Endpoint: GET /books/{book_id}/reviews/



You can save this content in a file named `README.md` in the root directory of your project.

