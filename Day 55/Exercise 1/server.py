from flask import Flask

app = Flask(__name__)

def make_bold(function):
    def return_function():
        return f"<b>{function()}</b>"
    return return_function

def make_underline(function):
    def return_function():
        return f"<u>{function()}</u>"
    return return_function

def make_emphasize(function):
    def return_function():
        return f"<em>{function()}</em>"
    return return_function

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/bye")
@make_bold
@make_underline
@make_emphasize
def bye():
    return "Bye!"

if __name__ == "__main__":
    app.run(debug=True)