from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from flask_ckeditor.utils import cleanify
import datetime as dt

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''
def get_items_from_database(stmt):
    result = db.session.execute(stmt)
    return result.scalars().all()

def set_item_to_database(table, data):
    new_obj = table(**data)
    db.session.add(new_obj)
    db.session.commit()

def edit_items_from_database(obj, attr, val):
    setattr(obj, attr, val)
    db.session.commit()

def delete_items_from_database(obj):
    db.session.delete(obj)
    db.session.commit()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CKEDITOR INSTANCE
ckeditor = CKEditor()
ckeditor.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


class BlogForm(FlaskForm):
    title = StringField("Blog Title", validators=[DataRequired()])
    subtitle = StringField("Blog Subtitle", validators=[DataRequired()])
    body = CKEditorField("Blog Body", validators=[DataRequired()])
    author = StringField("Author's Name", validators=[DataRequired()])
    img_url = URLField("URL for background image", validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    stmt = db.select(BlogPost).order_by(BlogPost.id.desc())
    posts = get_items_from_database(stmt)

    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    stmt = db.select(BlogPost).where(BlogPost.id == post_id)
    posts = get_items_from_database(stmt)
    requested_post = posts[0]

    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route("/new-post", methods=["POST", "GET"])
def create_post():
    form = BlogForm()

    if form.validate_on_submit():
        print("borat")
        datetime_now = dt.datetime.now()

        blog_data = {
            "title" : form.title.data,
            "subtitle" : form.subtitle.data,
            "date" : datetime_now,
            "body" : cleanify(form.body.data),
            "author" : form.author.data,
            "img_url" : form.img_url.data
        }

        set_item_to_database(BlogPost, blog_data)

        return redirect(url_for("get_all_posts"))

    return render_template("make-post.html", form=form)

# TODO: edit_post() to change an existing blog post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    stmt = db.select(BlogPost).where(BlogPost.id == post_id)
    posts = get_items_from_database(stmt)
    requested_post = posts[0]

    blog_data = {
        "title" : requested_post.title,
        "subtitle" : requested_post.subtitle,
        "body" : requested_post.body,
        "author" : requested_post.author,
        "img_url" : requested_post.img_url
    }

    form = BlogForm(**blog_data)

    if form.validate_on_submit():
        for key in blog_data:
            if key == "body": value_str = f"cleanify(form.{key}.data)"
            else: value_str = f"form.{key}.data"
            edit_items_from_database(requested_post, key, eval(value_str))

        return redirect(url_for("show_post", post_id=requested_post.id))

    return render_template("make-post.html", form=form, isForEdit=True)

# TODO: delete_post() to remove a blog post from the database
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    stmt = db.select(BlogPost).where(BlogPost.id == post_id)
    posts = get_items_from_database(stmt)
    requested_post = posts[0]

    delete_items_from_database(requested_post)

    return redirect(url_for("get_all_posts"))

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")





# APP TEMPLATE FILTERS
@app.template_filter("strptime")
def modify_date_string(date, date_format="%B %d, %Y at %I:%M%p"):
    new_datetime = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    return new_datetime.strftime(date_format)

if __name__ == "__main__":
    app.run(debug=True, port=5003)

