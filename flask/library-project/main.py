from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from wtforms import FloatField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class Base(DeclarativeBase):
  pass

app = Flask(__name__)
Bootstrap5(app)
app.config["SECRET_KEY"] = "really_secret_book_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-library.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Book(db.Model):
    __tablename__ = "library"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

class BookForm(FlaskForm):
    book_name = StringField(
        "Book Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter the book title"}
    )

    book_author = StringField(
        "Book Author",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter the book's author"}
    )

    book_rating = FloatField(
        "Book Rating",
        validators=[DataRequired(), NumberRange(0, 10)],
        render_kw={"placeholder": "Enter the book's rating from 0 to 10"}
    )

    submit = SubmitField(
        "Submit",
        render_kw={"class": "btn btn-warning space-above"}
    )

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    books = []

    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        books = result.scalars().all()

    return render_template("index.html", library=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = BookForm()

    if form.validate_on_submit():
        title = form.book_name.data
        author = form.book_author.data
        rating = form.book_rating.data

        with app.app_context():
            book = Book(title=title, author=author, rating=rating)
            db.session.add(book)
            db.session.commit()

        return redirect(url_for("home"))
    else:
        return render_template("add.html", form=form)

@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    form = BookForm()

    if request.method == "GET":
        book = Book()

        with app.app_context():
            book = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()

        form.book_name.default = book.title
        form.book_author.default = book.author
        form.book_rating.default = book.rating
        form.process()

        return render_template("edit.html", form=form, book=book)
    else:
        new_title = form.book_name.data
        new_author = form.book_author.data
        new_rating = form.book_rating.data

        with app.app_context():
            book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
            book_to_update.title = new_title
            book_to_update.author = new_author
            book_to_update.rating = new_rating
            db.session.commit()

        return redirect(url_for("home"))

@app.route("/delete/<int:book_id>", methods=["GET", "POST"])
def delete(book_id):
    with app.app_context():
        book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

