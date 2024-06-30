from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize Flask application
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    def __init__(self, book_name, author, publisher):
        self.book_name = book_name
        self.author = author
        self.publisher = publisher

# Book Schema (for serialization/deserialization)
class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'book_name', 'author', 'publisher')

# Initialize Book schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Routes

# Create a Book
@app.route('/book', methods=['POST'])
def add_book():
    book_name = request.json['book_name']
    author = request.json['author']
    publisher = request.json['publisher']

    new_book = Book(book_name=book_name, author=author, publisher=publisher)

    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book), 201

# Get all Books
@app.route('/books', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result)

# Get single Book
@app.route('/book/<id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    return book_schema.jsonify(book)

# Update a Book
@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)

    book_name = request.json['book_name']
    author = request.json['author']
    publisher = request.json['publisher']

    book.book_name = book_name
    book.author = author
    book.publisher = publisher

    db.session.commit()

    return book_schema.jsonify(book)

# Delete Book
@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return book_schema.jsonify(book)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
