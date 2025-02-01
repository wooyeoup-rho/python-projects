from datetime import datetime
from flask import Flask, render_template
import requests

app = Flask(__name__)

response = requests.get("https://api.npoint.io/674f5423f73deab1e9a7")
response.raise_for_status()
blog_posts = response.json()

@app.route("/")
def home():
    current_year = datetime.now().year
    return render_template("index.html", header_image="home-bg.jpg", heading="Clean Blog", subheading="A Blog Theme by Start Bootstrap", blog_posts=blog_posts, year=current_year)

@app.route("/contact")
def contact():
    return render_template("contact.html", header_image="contact-bg.jpg", heading="Contact Me", subheading="Have questions? I have answers.")

@app.route("/about")
def about():
    return render_template("about.html", header_image="about-bg.jpg", heading="About Me", subheading="This is what I do.")

@app.route("/post/<int:blog_id>")
def blog_post(blog_id):
    post = blog_posts[blog_id - 1]

    return render_template("post.html", post=post["body"], header_image=post["image_url"], heading=post["title"], subheading=post["subtitle"])

if __name__ == "__main__":
    app.run(debug=True)
