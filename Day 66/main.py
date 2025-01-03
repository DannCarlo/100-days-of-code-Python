import random
import json
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
API_KEYS = ["1", "2", "3"]


def return_invalid_request_json():
    data = {
        "error" : {
            "Invalid" : "Sorry, an invalid request was submitted."
        }
    }

    return jsonify(data)

def return_no_cafe_from_id_json():
    data = {
        "error" : {
            "NotFound" : "Sorry, a cafe with that ID was not found in the database."
        }
    }

    return jsonify(data)

def return_no_cafe_location_json():
    data = {
        "error" : {
            "NotFound" : "Sorry, we don't have a cafe at that location."
        }
    }

    return jsonify(data)

def return_success_add_cafe_json():
    data = {
        "response" : {
            "Success" : "Successfully added the new cafe."
        }
    }

    return jsonify(data)

def return_success_edit_cafe_json():
    data = {
        "response" : {
            "SuccessEdit" : "Successfully edited a cafe information in database."
        }
    }

    return jsonify(data)

def return_error_api_key_json():
    data = {
        "error" : {
            "NoAccess" : "Sorry, that's not allowed. Make sure you have the correct API KEY."
        }
    }

    return jsonify(data)

def return_success_cafe_delete_json():
    data = {
        "response" : {
            "SuccessDelete" : "Successfully deleted a cafe in database."
        }
    }

    return jsonify(data)


def return_cafe_data(cafe):
    data = {
        "can_take_calls" : cafe.can_take_calls,
        "coffee_price" : cafe.coffee_price,
        "has_sockets" : cafe.has_sockets,
        "has_toilets" : cafe.has_toilet,
        "has_wifi" : cafe.has_wifi,
        "id" : cafe.id,
        "img_url" : cafe.img_url,
        "location" : cafe.location,
        "map_url" : cafe.map_url,
        "name" : cafe.name,
        "seats" : cafe.seats
    }
    return data

def get_items_from_database(stmt):
    result = db.session.execute(stmt)
    return result.scalars().all()

def edit_items_from_database(obj, attr, val):
    setattr(obj, attr, val)
    db.session.commit()

def delete_items_from_database(obj):
    db.session.delete(obj)
    db.session.commit()

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def random_cafe():
    stmt = db.select(Cafe)
    cafes = get_items_from_database(stmt)
    random_cafe = random.choice(cafes)

    data = {
        "cafe" : return_cafe_data(random_cafe)
    }

    return jsonify(data)

@app.route("/all")
def all_cafe():
    stmt = db.select(Cafe)
    cafes = get_items_from_database(stmt)

    all_data = {
        "cafes" : []
    }

    for cafe in cafes:
        all_data["cafes"].append(return_cafe_data(cafe))

    return jsonify(all_data)

@app.route("/search")
def search_cafe():
    queries_dict = request.args

    if "loc" not in queries_dict:
        return return_no_cafe_location_json()

    location = f"Cafe.location == '{queries_dict['loc']}'" if queries_dict["loc"] else ""
    stmt = db.select(Cafe).where(eval(location))
    cafes = get_items_from_database(stmt)

    all_data = {
        "cafes" : []
    }

    for cafe in cafes:
        all_data["cafes"].append(return_cafe_data(cafe))

    return jsonify(all_data)


# HTTP POST - Create Record
@app.post("/add")
def add_cafe():
    if request.args:

        if "loc" in request.args:
            return return_success_add_cafe_json()
    else:
        return return_invalid_request_json()

# HTTP PUT/PATCH - Update Record
@app.patch("/update-price/<int:cafe_id>")
def update_cafe_price(cafe_id):
    if "new_price" not in request.args:
        return return_invalid_request_json

    new_price = request.args["new_price"]

    stmt = db.select(Cafe).where(Cafe.id == cafe_id)
    cafes = get_items_from_database(stmt)

    if cafes:
        cafe = cafes[0]

        edit_items_from_database(cafe, "coffee_price", new_price)

        return return_success_edit_cafe_json()

    return return_no_cafe_from_id_json()


# HTTP DELETE - Delete Record
@app.delete("/report-closed/<int:cafe_id>")
def delete_cafe(cafe_id):
    if "api_key" not in request.args:
        return return_invalid_request_json()

    api_key = request.args["api_key"]

    if api_key not in API_KEYS:
        return return_error_api_key_json()

    stmt = db.select(Cafe).where(Cafe.id == cafe_id)
    cafes = get_items_from_database(stmt)

    if cafes:
        cafe = cafes[0]

        delete_items_from_database(cafe)

        return return_success_edit_cafe_json()

    return return_no_cafe_from_id_json()


if __name__ == '__main__':
    app.run(debug=True)
