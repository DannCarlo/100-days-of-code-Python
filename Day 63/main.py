import mysql.connector
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm as so
from flask import Flask, render_template, request, redirect, url_for

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
def get_items_from_database(stmt):
    result = db.session.execute(stmt)
    return result.scalars().all()

def set_item_to_database(table, data):
    new_obj = table(**data)
    db.session.add(new_obj)
    db.session.commit()

def edit_item_to_database(variable, data, value):
    if data == "rating": variable.rating = value
    db.session.commit()

def delete_item_from_database(stmt):

    book_to_delete = db.session.execute(stmt).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost:3306/new_books_collection"

class Base(so.DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Books(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, unique=True)
    author: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    stmt = db.select(Books).order_by(Books.title)
    books = get_items_from_database(stmt)
    return render_template("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book = {
            "title" : request.form["title"],
            "author" : request.form["author"],
            "rating" : f"{request.form['rating']}/10"
        }

        set_item_to_database(Books, book)
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/delete/<book_id>")
def delete(book_id):
    stmt = db.select(Books).where(Books.id == book_id)
    delete_item_from_database(stmt)
    return redirect(url_for("home"))

@app.route("/edit/<book_id>", methods=["GET", "POST"])
def edit(book_id):
    stmt = db.select(Books).where(Books.id == book_id)
    book = get_items_from_database(stmt)[0]

    if request.method == "POST":
        edit_item_to_database(book, "rating", float(request.form["rating"]))

        return redirect(url_for("home"))

    return render_template("edit.html", book=book)


if __name__ == "__main__":
    app.run(debug=True)

