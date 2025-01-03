import random
from flask import Flask

app = Flask(__name__)

generated_number = None

@app.route("/")
def generate_number():
    global generated_number

    generated_number = random.randint(0, 9)

    return ("<h1>Guess a number from 0 to 9</h1>"
            "<img src=\"https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif\"/>")

@app.route("/<int:number>")
def check_number(number):
    global generated_number

    if number < generated_number:
        return ("<h1 style=\"color:violet\">Too low, try again!</h1>"
                "<img src=\"https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif\"/>")
    elif number > generated_number:
        return ("<h1 style=\"color:red\">Too high, try again!</h1>"
                "<img src=\"https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif\"/>")
    else:
        return ("<h1 style=\"color:green\">You found me!</h1>"
                "<img src=\"https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif\"/>")

if __name__ == "__main__":
    app.run(debug=True)