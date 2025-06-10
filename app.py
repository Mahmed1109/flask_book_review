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
    if query:
        filtered = [
            b for b in books
            if query in b['title'].lower() or query in b['author'].lower()
        ]
    else:
        filtered = books
    return render_template('index.html', books=filtered, query=query)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        books.append({
            'title': request.form['title'],
            'author': request.form['author'],
            'review': request.form['review'],
            'rating': int(request.form['rating']),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        })
        save_books()
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if not (0 <= book_id < len(books)):
        return "Not found", 404
    book = books[book_id]
    if request.method == 'POST':
        book.update({
            'title': request.form['title'],
            'author': request.form['author'],
            'review': request.form['review'],
            'rating': int(request.form['rating']),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        })
        save_books()
        return redirect(url_for('index'))
    return render_template('edit_book.html', book=book, book_id=book_id)

@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if 0 <= book_id < len(books):
        books.pop(book_id)
        save_books()
    return redirect(url_for('index'))

if __name__ == '__main__':
    load_books()
    app.run(debug=True)
