from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
books = []

@app.route('/')
def index():
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        review = request.form['review']
        date_posted = datetime.now().strftime('%Y-%m-%d %H:%M')

        books.append({
            'title': title,
            'author': author,
            'review': review,
            'date': date_posted
        })

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
        book['date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        return redirect(url_for('index'))

    return render_template('edit_book.html', book=book, book_id=book_id)

@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if 0 <= book_id < len(books):
        del books[book_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
