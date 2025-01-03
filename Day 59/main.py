import requests
from post import Post
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

POSTS_DATA_URL = "https://api.npoint.io/c790b4d5cab58020d391"

def return_post_obj(post_data):
    post_id = post_data["id"]
    post_title = post_data["title"]
    post_subtitle = post_data["subtitle"]
    post_body = post_data["body"]

    return Post(post_id, post_title, post_subtitle, post_body)

@app.route('/')
def get_home():
    posts_request = requests.get(url=POSTS_DATA_URL)
    posts_data = posts_request.json()

    posts_obj_list = []
    for post in posts_data:
        post_obj = return_post_obj(post)
        posts_obj_list.append(post_obj)

    return render_template("index.html", posts_obj_list=posts_obj_list)

@app.route('/about')
def get_about():
    return render_template("about.html")

@app.route('/contact')
def get_contact():
    return render_template("contact.html")

@app.route("/post/<int:post_id>")
def get_post(post_id):
    posts_request = requests.get(url=POSTS_DATA_URL)
    posts_data = posts_request.json()

    post_obj = None

    for post in posts_data:
        if post["id"] == post_id:
            post_obj = return_post_obj(post)
            break

    if post_obj: return render_template("post.html", post_obj=post_obj)
    else: return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
