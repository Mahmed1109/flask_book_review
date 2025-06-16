from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)
DATA_FILE = 'books.json'
books = []

def load_books():
    global books
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            books = json.load(f)

def save_books():
    with open(DATA_FILE, 'w') as f:
        json.dump(books, f, indent=2)

@app.route('/')
def index():
    query = request.args.get('q', '').lower()
    sort = request.args.get('sort', '')

    filtered_books = books

    if query:
        filtered_books = [
            book for book in books
            if query in book['title'].lower() or query in book['author'].lower()
        ]

    def parse_date(book):
        return datetime.strptime(book.get('date', ''), '%Y-%m-%d %H:%M')

    if sort == 'high':
        filtered_books = sorted(filtered_books, key=lambda x: x.get('rating', 0), reverse=True)
    elif sort == 'low':
        filtered_books = sorted(filtered_books, key=lambda x: x.get('rating', 0))
    elif sort == 'date_new':
        filtered_books = sorted(filtered_books, key=parse_date, reverse=True)
    elif sort == 'date_old':
        filtered_books = sorted(filtered_books, key=parse_date)

    return render_template('index.html', books=filtered_books, query=query, sort=sort)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        review = request.form['review']
        rating = int(request.form['rating'])
        date_posted = datetime.now().strftime('%Y-%m-%d %H:%M')

        books.append({
            'title': title,
            'author': author,
            'review': review,
            'rating': rating,
            'date': date_posted
        })
        save_books()
        return redirect(url_for('index'))

    return render_template('add_book.html')

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if book_id < 0 or book_id >= len(books):
        return "Book not found", 404

    book = books[book_id]

    if request.method == 'POST':
        book['title'] = request.form['title']
        book['author'] = request.form['author']
        book['review'] = request.form['review']
        book['rating'] = int(request.form['rating'])
        book['date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        save_books()
        return redirect(url_for('index'))

    return render_template('edit_book.html', book=book, book_id=book_id)

@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if 0 <= book_id < len(books):
        del books[book_id]
        save_books()
    return redirect(url_for('index'))

if __name__ == '__main__':
    load_books()
    app.run(debug=True)
