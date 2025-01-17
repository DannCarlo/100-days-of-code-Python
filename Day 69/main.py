from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
# Import your forms from the forms.py
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm


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

    return new_obj

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

# TODO: Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    user = db.session.get(Users, user_id)
    return user


# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    author: Mapped["Users"] = relationship(back_populates="posts")
    comments: Mapped[list["Comments"]] = relationship(back_populates="post")

    def __repr__(self):
        return f"<BlogPost {self.title}>"


# TODO: Create a User table for all your registered users.
class Users(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(1000), nullable=False)

    posts: Mapped[list["BlogPost"]] = relationship(back_populates="author")
    comments: Mapped[list["Comments"]] = relationship(back_populates="author")

    def __repr__(self):
        return f"<User {self.id}>"

# TODO: Create a User table for all your registered users.
class Comments(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_posts.id"))
    body: Mapped[str] = mapped_column(Text, nullable=False)

    author: Mapped["Users"] = relationship(back_populates="comments")
    post: Mapped[list["BlogPost"]] = relationship(back_populates="comments")

    def __repr__(self):
        return f"<User {self.id}>"

# Gravatar integration
gravatar = Gravatar(app, size=100, rating='g', default='retro',
                    force_default=False, force_lower=False,
                    use_ssl=False, base_url=None)


with app.app_context():
    db.create_all()


# DECORATOR FUNCTIONS
def admin_only(func):
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        if current_user.get_id() != "1":
            return abort(403)
        return func(*args, **kwargs)
    return wrapper_function



# TODO: Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data

        stmt = db.select(Users).where(Users.email == email)
        users = get_items_from_database(stmt)

        if users:
            flash('User already exist. Login with the given email.')
            return redirect(url_for('login'))

        password = form.password.data
        password = generate_password_hash(password, "pbkdf2", salt_length=8)

        user_data = {
            "name" : form.name.data,
            "email" : email,
            "password" : password
        }

        new_user = set_item_to_database(Users, user_data)
        login_user(new_user, remember=True)

        return redirect(url_for("get_all_posts"))

    return render_template("register.html", form=form)


# TODO: Retrieve a user from the database based on their email. 
@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("get_all_posts"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        stmt = db.select(Users).where(Users.email == email)
        users = get_items_from_database(stmt)

        if not users or not check_password_hash(users[0].password, password):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        active_user = users[0]
        login_user(active_user)

        return redirect(url_for("get_all_posts"))

    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    stmt = db.select(BlogPost)
    posts = get_items_from_database(stmt)
    return render_template("index.html", all_posts=posts)


# TODO: Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods=["POST", "GET"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)

    form = CommentForm()

    if current_user.is_authenticated and form.validate_on_submit():
        comment_data = {
            "author_id" : current_user.get_id(),
            "post_id" : post_id,
            "body" : form.body.data,
        }

        set_item_to_database(Comments, comment_data)

    return render_template("post.html", post=requested_post, form=form)


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@login_required
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post_data = {
            "title" : form.title.data,
            "subtitle" : form.subtitle.data,
            "body" : form.body.data,
            "img_url" : form.img_url.data,
            "author_id" : current_user.get_id(),
            "date" : date.today().strftime("%B %d, %Y")
        }

        set_item_to_database(BlogPost, post_data)

        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
@login_required
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
