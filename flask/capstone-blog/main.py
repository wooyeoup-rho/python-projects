from dotenv import load_dotenv, dotenv_values
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, request
import requests, smtplib

load_dotenv()
config = dotenv_values(".env")

EMAIL = config.get("SENDING_EMAIL")
EMAIL_PASSWORD = config.get("SENDING_EMAIL_PWD")

app = Flask(__name__)

response = requests.get("https://api.npoint.io/674f5423f73deab1e9a7")
response.raise_for_status()
blog_posts = response.json()

@app.route("/")
def home():
    return render_template("index.html", blog_posts=blog_posts)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        msg["Subject"] = "New message!"

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        html_content = f"""
        <html>
        <body>
            <p><b>Name:</b> {name}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Phone:</b> {phone}</p>
            <p><b>Message:</b><br/>{message}</p>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=EMAIL_PASSWORD)
            connection.sendmail(msg["From"], msg["To"], msg.as_string())

        return render_template("contact.html", heading="Message Sent")
    else:
        return render_template("contact.html", heading="Contact Me")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post/<int:blog_id>")
def blog_post(blog_id):
    post = blog_posts[blog_id - 1]

    return render_template("post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)
