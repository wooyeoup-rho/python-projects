from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "golly_no_one_would_guess_this"

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["UPLOAD_FOLDER"] = "static/files"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

# CREATE TABLE IN DB
class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already registered.", "danger")
            return redirect(url_for("login"))
        else:
            hashed_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

            user = User(
                name=name,
                email=email,
                password=hashed_password
            )

            db.session.add(user)
            db.session.commit()
            login_user(user)

        return redirect(url_for("secrets"))
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully", "success")
            return redirect(url_for("secrets"))

        flash("Invalid credentials", "danger")
        return redirect(url_for("login"))
    else:
        return render_template("login.html")

@app.route("/secrets")
@login_required
def secrets():
    return render_template("secrets.html", user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/download")
@login_required
def download():
    return send_from_directory(
        app.config["UPLOAD_FOLDER"], "cheat_sheet.pdf", as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)
