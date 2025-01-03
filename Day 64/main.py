import os
from email.policy import default

import sqlalchemy.orm as so
import sqlalchemy as sa
import requests
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import NumberRange, Optional, DataRequired
from sqlalchemy.dialects.mysql import LONGTEXT

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
MOVIE_API_TOKEN = os.environ.get("MOVIE_API_TOKEN")
MOVIE_API_KEY = os.environ.get("MOVIE_API_KEY")
MOVIE_AUTH = os.environ.get("MOVIE_AUTH")

MOVIE_SEARCH_BY_TITLE_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_SEARCH_BY_ID_URL = "https://api.themoviedb.org/3/movie/"

MOVIE_HEADER = {
    "Authorization" : MOVIE_AUTH
}

def get_items_from_database(stmt):
    result = db.session.execute(stmt)
    return result.scalars().all()

def edit_item_to_database(obj, attr, value):
    setattr(obj, attr, value)
    db.session.commit()

def delete_item_from_database(stmt):
    book_to_delete = db.session.execute(stmt).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()

def set_item_to_database(table, data):
    new_obj = table(**data)
    db.session.add(new_obj)
    db.session.commit()

def review_order_by_rankings(table):
    stmt = db.select(table).where(table.rating != None)
    objs = get_items_from_database(stmt)

    objs.sort(key=lambda x: x.rating, reverse=True)

    for idx, obj in enumerate(objs):
        edit_item_to_database(obj, "ranking", idx + 1)

def get_movies_by_title_from_web(movie_title):
    global MOVIE_HEADER, MOVIE_SEARCH_BY_TITLE_URL

    url_params = dict(query=movie_title)

    url_request = requests.get(url=MOVIE_SEARCH_BY_TITLE_URL, params=url_params, headers=MOVIE_HEADER)
    url_data = url_request.json()

    return url_data["results"]

def get_movie_detail_by_id_from_web(url):
    global MOVIE_HEADER

    url_request = requests.get(url=url, headers=MOVIE_HEADER)
    url_data = url_request.json()

    title = url_data["title"]
    year = int(url_data["release_date"].split("-")[0])
    description = url_data["overview"]
    img_url = "https://image.tmdb.org/t/p/w500" + url_data["poster_path"]

    movie_obj_data = {
        "title" : title,
        "year" : year,
        "description" : description,
        "img_url" : img_url
    }

    return movie_obj_data


# EDIT TABLE
class EditForm(FlaskForm):
    rating = DecimalField('Your rating out of 10 (eg. 7.5)', validators=[DataRequired(), NumberRange(min=0, max=10)])
    review = StringField("Your review", validators=[DataRequired()])
    submit = SubmitField('Submit')


# CREATE TABLE
class CreateForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost:3306/movie_reviews"
Bootstrap5(app)

# CREATE DB
class Base(so.DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movies(db.Model):
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, unique=True)
    year: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    description: so.Mapped[str] = so.mapped_column(LONGTEXT, nullable=False)
    rating: so.Mapped[float] = so.mapped_column(sa.Float, nullable=True)
    ranking: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    review: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    img_url: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)

    def __repr__(self):
        return f"<Movie {self.title}>"

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    stmt = db.select(Movies).order_by(Movies.ranking.desc())
    movies = get_items_from_database(stmt)
    return render_template("index.html", movies=movies)

@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    stmt = db.select(Movies).where(Movies.id == movie_id)
    movies = get_items_from_database(stmt)
    movie = movies[0]

    form = EditForm()

    if form.validate_on_submit():
        if form.rating.data:
            edit_item_to_database(movie, "rating", form.rating.data)
        if form.review.data:
            edit_item_to_database(movie, "review", form.review.data)

        review_order_by_rankings(Movies)
        return redirect(url_for("home"))

    return render_template("edit.html", movie=movie, form=form)

@app.route("/delete/<int:movie_id>")
def delete(movie_id):
    stmt = db.select(Movies).where(Movies.id == movie_id)
    delete_item_from_database(stmt)

    return redirect(url_for("home"))

@app.route("/add", methods=["GET", "POST"], defaults={"movie_id" : None})
@app.route("/add/<int:movie_id>")
def add(movie_id):
    if movie_id:
        movie_url = MOVIE_SEARCH_BY_ID_URL + str(movie_id)

        movie_obj_data = get_movie_detail_by_id_from_web(movie_url)

        set_item_to_database(Movies, movie_obj_data)

        stmt = db.select(Movies).where(Movies.title == movie_obj_data["title"])
        movies = get_items_from_database(stmt)
        movie = movies[0]

        return redirect(url_for("edit", movie_id=movie.id))
    else:
        form = CreateForm()
        if form.validate_on_submit():
            movie_title = form.title.data

            movie_list = get_movies_by_title_from_web(movie_title)

            return render_template("select.html", movie_list=movie_list)

        return render_template("add.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
