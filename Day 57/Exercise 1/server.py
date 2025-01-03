import requests
from flask import Flask, render_template

app = Flask(__name__)

GENDERIZE_URL = "https://api.genderize.io?name="
AGIFY_URL = "https://api.agify.io?name="

@app.route("/guess/<name>")
def run_page(name):
    genderize_request = requests.get(url=GENDERIZE_URL+name)
    genderize_data = genderize_request.json()

    gender = genderize_data["gender"]

    agify_request = requests.get(url=AGIFY_URL+name)
    agify_data = agify_request.json()

    age = agify_data["age"]

    return render_template("index.html", name=name, gender=gender, age=age)

if __name__ == "__main__":
    app.run(debug=True)