from flask import Flask, render_template, request, redirect, flash
import dbhelper

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route('/')
def index():
    books = dbhelper.getall_books()
    return render_template("index.html", books=books)

@app.route('/addbook', methods=['POST'])
def add_book():
    isbn = request.form['isbn']
    title = request.form['title']
    author = request.form['author']
    copyright = request.form['copyright']
    edition = request.form['edition']
    price = request.form['price']
    qty = request.form['qty']
    
    ok = dbhelper.add_record(
        'books',
        isbn=isbn,
        title=title,
        author=author,
        copyright=copyright,
        edition=edition,
        price=price,
        qty=qty
    )
    
    message = "New Book Added" if ok else "Error Adding Book"
    flash(message)
    return redirect('/')

@app.route('/findbook', methods=['POST'])
def find_book():
    isbn = request.form['isbn']
    sql = f"SELECT * FROM books WHERE isbn = '{isbn}'"
    book = dbhelper.getprocess(sql)
    
    if book:
        found_book = book[0]  
        message = (f"Book found: ISBN: {found_book['isbn']}, Title: {found_book['title']}, "
                   f"Author: {found_book['author']}, Copyright: {found_book['copyright']}, "
                   f"Edition: {found_book['edition']}, Price: {found_book['price']}, "
                   f"Quantity: {found_book['qty']}")
    else:
        message = "Book not found."
    
    flash(message)  
    return redirect('/')

@app.route('/deletebook', methods=['POST'])
def delete_book():
    isbn = request.form['isbn']
    ok = dbhelper.delete_record('books', isbn=isbn)  
    message = "Book deleted successfully!" if ok else "Error deleting book."  
    flash(message)  
    return redirect('/')

@app.route('/updatebook', methods=['POST'])
def update_book():
    isbn = request.form['isbn']
    sql = f"""
    UPDATE books SET 
    title = '{request.form['title']}', 
    author = '{request.form['author']}', 
    copyright = '{request.form['copyright']}', 
    edition = '{request.form['edition']}', 
    price = '{request.form['price']}', 
    qty = '{request.form['qty']}'
    WHERE isbn = '{isbn}'
    """
    ok = dbhelper.postprocess(sql)  
    message = "Book updated successfully!" if ok else "Error updating book."  
    flash(message) 
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
