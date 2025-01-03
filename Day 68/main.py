from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from urllib.parse import unquote

def get_items_from_database(stmt):
    result = db.session.execute(stmt)
    return result.scalars().all()

def set_item_to_database(table, data):
    new_obj = table(**data)
    db.session.add(new_obj)
    db.session.commit()

    return new_obj


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/files/"
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


# FLASK LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    stmt = db.select(User).where(User.id == user_id)
    users = get_items_from_database(stmt)
    return users[0]



@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == "POST":
        email = request.form["email"]

        stmt = db.select(User).where(User.email == email)
        users = get_items_from_database(stmt)

        if users:
            flash('User already exist.')
            return redirect(url_for('register'))

        password = request.form["password"]
        password = generate_password_hash(password, "pbkdf2", salt_length=8)

        user_data = {
            "name" : request.form["name"],
            "email" : email,
            "password" : password
        }

        new_user = set_item_to_database(User, user_data)
        login_user(new_user, remember=True)

        if request.form["next"].strip(): next_page = url_for(request.form["next"][1:].strip())
        else: next_page = False

        return redirect(next_page or url_for("home"))

    return render_template("register.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == "POST":
        stmt = db.select(User).where(User.email == request.form["email"])
        users = get_items_from_database(stmt)

        if not users or not check_password_hash(users[0].password, request.form["password"]):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        authenticated_user = users[0]
        login_user(authenticated_user, remember=True)

        print(request.form["next"])

        if request.form["next"].strip(): next_page = url_for(request.form["next"][1:].strip())
        else: next_page = False

        return redirect(next_page or url_for("home"))

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/download')
@login_required
def download():
    return send_from_directory(app.config["UPLOAD_FOLDER"], "cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
