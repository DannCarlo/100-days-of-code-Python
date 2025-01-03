from flask import Flask, render_template, request
import requests

SENDER_EMAIL = "email@yahoo.com"
SENDER_PW = ""

SENDER_EMAIL_HOST = SENDER_EMAIL.split("@")[1]

if SENDER_EMAIL_HOST == "yahoo.com":
    SMTP_HOST = "smtp.mail.yahoo.com"
elif SENDER_EMAIL_HOST == "gmail.com":
    SMTP_HOST = "smtp.gmail.com"
else:
    SMTP_HOST = "outlook.office365.com"

posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)

# FLASK ROUTE FUNCTIONS
@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    else:
        import smtplib

        message = (f"name: {request.form['name']}\n"
                   f"email: {request.form['email']}\n"
                   f"phone: {request.form['phone']}\n"
                   f"message: {request.form['message']}")

        with smtplib.SMTP(SMTP_HOST, port=587) as connection:
            connection.starttls()
            connection.login(user=SENDER_EMAIL, password=SENDER_PW)
            connection.sendmail(from_addr=SENDER_EMAIL,
                                to_addrs=SENDER_EMAIL,
                                msg=f"Subject: New message from your website!\n\n{message}")

        return render_template("contact.html", message_successful = True)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
