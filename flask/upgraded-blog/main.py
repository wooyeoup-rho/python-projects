from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "my_super_secret_blog_key"
Bootstrap5(app)
ckeditor = CKEditor(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()

# FORM
class PostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content")
    submit = SubmitField("Submit")

@app.route("/")
def get_all_posts():
    posts = []

    with app.app_context():
        posts = db.session.execute(db.select(BlogPost)).scalars().all()

    return render_template("index.html", all_posts=posts)

@app.route("/<post_id>")
def show_post(post_id):
    with app.app_context():
        post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    return render_template("post.html", post=post)


@app.route("/add", methods=["GET", "POST"])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        new_blog = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=datetime.now().strftime("%B %d, %Y"),
            author=form.author.data,
            img_url=form.img_url.data,
            body=form.body.data,
        )

        with app.app_context():
            db.session.add(new_blog)
            db.session.commit()

        return redirect(url_for("get_all_posts"))
    else:
        return render_template("make-post.html", form=form, title="New Post")

@app.route("/edit/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    form = PostForm()

    if form.validate_on_submit():
        with app.app_context():
            post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
            post.title = form.title.data
            post.subtitle = form.subtitle.data
            post.author = form.author.data
            post.img_url = form.img_url.data
            post.body = form.body.data
            db.session.commit()

        return redirect(url_for("show_post", post_id=post_id))
    else:
        with app.app_context():
            post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
            form.title.data = post.title
            form.subtitle.data = post.subtitle
            form.author.data = post.author
            form.img_url.data = post.img_url
            form.body.data = post.body

        return render_template("make-post.html", form=form, title="Edit Post")

@app.route("/delete/<post_id>")
def delete_post(post_id):
    with app.app_context():
        post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
        db.session.delete(post)
        db.session.commit()

    return redirect(url_for("get_all_posts"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True, port=5003)
