from dotenv import load_dotenv, dotenv_values
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import requests

# CONSTANTS
load_dotenv()
config = dotenv_values(".env")

API_TOKEN = config.get("TMDB_API_TOKEN")
TMDB_SEARCH_ENDPOINT = "https://api.themoviedb.org/3/search/movie"
TMDB_DETAILS_ENDPOINT = "https://api.themoviedb.org/3/movie"
MOVIE_IMAGE_ENDPOINT = "http://image.tmdb.org/t/p/w500"

app = Flask(__name__)
app.config['SECRET_KEY'] = "super_secret_movie_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies-collection.db"
Bootstrap5(app)

# DB CREATION
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# TABLE
class Movie(db.Model):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

class MovieEditForm(FlaskForm):
    movie_rating = FloatField(
        "Your Rating",
        validators=[DataRequired(), NumberRange(0, 10)],
        render_kw={"placeholder": "Out of 10"}
    )

    movie_review = StringField(
        "Your Review",
        validators=[DataRequired()]
    )

    submit = SubmitField(
        "Submit"
    )

class MovieAddForm(FlaskForm):
    movie_title = StringField(
        "Movie Title",
        validators=[DataRequired()]
    )

    submit = SubmitField(
        "Find Movie"
    )

# ROUTES
@app.route("/")
def home():
    movies = []

    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.rating))
        movies = result.scalars().all()

    for i, movie in enumerate(movies):
        movie.ranking = len(movies) - i

    return render_template("index.html", movies=movies)

@app.route("/add", methods=["GET", "POST"])
def add():
    form = MovieAddForm()

    if request.method == "POST":
        title = form.movie_title.data

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_TOKEN}"
        }

        params = {
            "query": title
        }

        response = requests.get(TMDB_SEARCH_ENDPOINT, params=params, headers=headers)
        response.raise_for_status()

        movies = response.json()["results"]

        return render_template("select.html", movies=movies)

    else:
        return render_template("add.html", form=form)

@app.route("/select/<int:movie_id>", methods=["GET", "POST"])
def select(movie_id):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    response = requests.get(f"{TMDB_DETAILS_ENDPOINT}/{movie_id}", headers=headers)
    response.raise_for_status()

    data = response.json()

    with app.app_context():
        movie = Movie(
            title=data["original_title"],
            year=data["release_date"].split("-")[0],
            description=data["overview"],
            rating=0,
            ranking=0,
            review=0,
            img_url=f"{MOVIE_IMAGE_ENDPOINT}{data['poster_path']}"
        )
        db.session.add(movie)
        db.session.commit()

    movie = Movie()

    with app.app_context():
        movie = db.session.execute(db.select(Movie).where(Movie.title == data["original_title"])).scalar()

    return redirect(url_for("edit", movie_id=movie.id))

@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    form = MovieEditForm()

    if request.method == "POST":
        new_rating = form.movie_rating.data
        new_review = form.movie_review.data

        with app.app_context():
            movie = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
            movie.rating = new_rating
            movie.review = new_review
            db.session.commit()

        return redirect(url_for("home"))
    else:
        movie = Movie()

        with app.app_context():
            movie = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()

        form.movie_rating.default = movie.rating
        form.movie_review.default = movie.review
        form.process()

        return render_template("edit.html", form=form)

@app.route("/delete/<int:movie_id>")
def delete(movie_id):
    with app.app_context():
        book_to_delete = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
