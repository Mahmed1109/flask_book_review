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

if __name__ == '__main__':
    app.run(debug=True)
