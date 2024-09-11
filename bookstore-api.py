# Import Flask modules
from flask import Flask, jsonify, abort, request, make_response
from flaskext.mysql import MySQL

# Create an object named app 
app = Flask(__name__)

# Configure MySQL database (this part should later be secured using environment variables or Ansible Vault)
app.config['MYSQL_DATABASE_HOST'] = 'database'  # This will be set dynamically through Ansible.
app.config['MYSQL_DATABASE_USER'] = 'your_mysql_user'  # You should replace this with a secure method for storing passwords.
app.config['MYSQL_DATABASE_PASSWORD'] = 'your_mysql_password'  # Replace with secure method.
app.config['MYSQL_DATABASE_DB'] = 'bookstore_db'
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()

# Initialize the bookstore database and create table if not exists
def init_bookstore_db():
    cursor.execute("SHOW TABLES LIKE 'books';")
    result = cursor.fetchone()
    if not result:
        books_table = """
        CREATE TABLE books(
        book_id INT NOT NULL AUTO_INCREMENT,
        title VARCHAR(100) NOT NULL,
        author VARCHAR(100),
        is_sold BOOLEAN NOT NULL DEFAULT 0,
        PRIMARY KEY (book_id)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        cursor.execute(books_table)
        sample_data = """
        INSERT INTO books (title, author, is_sold)
        VALUES
            ("Where the Crawdads Sing", "Delia Owens", 1),
            ("The Vanishing Half", "Brit Bennett", 0),
            ("1st Case", "James Patterson", 0);
        """
        cursor.execute(sample_data)

# Define the Flask routes for API
@app.route('/')
def home():
    return "Welcome to the Callahan's Bookstore API Service"

@app.route('/books', methods=['GET'])
def get_books():
    query = "SELECT * FROM books;"
    cursor.execute(query)
    books = [{'book_id': row[0], 'title': row[1], 'author': row[2], 'is_sold': bool(row[3])} for row in cursor.fetchall()]
    return jsonify({'books': books})

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    query = f"SELECT * FROM books WHERE book_id={book_id};"
    cursor.execute(query)
    row = cursor.fetchone()
    if row:
        book = {'book_id': row[0], 'title': row[1], 'author': row[2], 'is_sold': bool(row[3])}
        return jsonify({'book': book})
    else:
        abort(404)

@app.route('/books', methods=['POST'])
def add_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    title = request.json['title']
    author = request.json.get('author', '')
    cursor.execute(f"INSERT INTO books (title, author) VALUES ('{title}', '{author}');")
    cursor.execute("SELECT * FROM books WHERE book_id=LAST_INSERT_ID();")
    row = cursor.fetchone()
    book = {'book_id': row[0], 'title': row[1], 'author': row[2], 'is_sold': bool(row[3])}
    return jsonify({'newly added book': book}), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if not request.json:
        abort(400)
    query = f"SELECT * FROM books WHERE book_id={book_id};"
    cursor.execute(query)
    row = cursor.fetchone()
    if not row:
        abort(404)
    title = request.json.get('title', row[1])
    author = request.json.get('author', row[2])
    is_sold = request.json.get('is_sold', row[3])
    cursor.execute(f"UPDATE books SET title='{title}', author='{author}', is_sold={is_sold} WHERE book_id={book_id};")
    return jsonify({'updated book': {'book_id': book_id, 'title': title, 'author': author, 'is_sold': bool(is_sold)}})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    query = f"SELECT * FROM books WHERE book_id={book_id};"
    cursor.execute(query)
    row = cursor.fetchone()
    if not row:
        abort(404)
    cursor.execute(f"DELETE FROM books WHERE book_id={book_id};")
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

if __name__ == '__main__':
    init_bookstore_db()
    app.run(host='0.0.0.0', port=80)
