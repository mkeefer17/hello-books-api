from app import db
from app.models.author import Author
from flask import Blueprint, jsonify, make_response, request, abort
from app.book_routes import validate_model

authors_bp = Blueprint("hello_world", __name__)

@authors_bp.route("/<author_id>/books", methods=["GET"])

def read_books(author_id):

    author = validate_model(Author, author_id)

    books_response = []
    for book in author.books:
        books_response.append(
            {
            "id": book.id,
            "title": book.title,
            "description": book.description
            }
        )
    return jsonify(books_response)


@authors_bp.route("/<author_id>/books", methods=["POST"])
def create_book(author_id):

    author = validate_model(Author, author_id)

    request_body = request.get_json()
    new_book = Book(
        title=request_body["title"],
        description=request_body["description"],
        author=author
    )
    db.session.add(new_book)
    db.session.commit()
    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)