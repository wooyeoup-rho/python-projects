from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Book(db.Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

db.init_app(app)

with app.app_context():
    # db.create_all()

    # book = Book(
    #     title = "And Then There Were Nuns",
    #     author = "Agathy Christy",
    #     rating = 3
    # )
    # db.session.add(book)
    # db.session.commit()

    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result
    for book in all_books:
        print(book)