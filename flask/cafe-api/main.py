from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func, Integer, String, Boolean

SECRET_KEY = "wow_super_secret"

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Read Record
@app.route("/random")
def random_cafe():
    cafe = Cafe()

    with app.app_context():
        result = db.session.execute(db.select(Cafe).order_by(func.random())).first()
        cafe = result[0] if result else None

    cafe_dict = dict(cafe.__dict__)
    cafe_dict.pop("_sa_instance_state", None)

    return jsonify(cafe=cafe_dict)

@app.route("/all")
def all_cafes():
    cafe_list = []
    with app.app_context():
        cafes = db.session.execute(db.select(Cafe)).scalars()
        for cafe in cafes:
            cafe_dict = dict(cafe.__dict__)
            cafe_dict.pop("_sa_instance_state", None)
            cafe_list.append(cafe_dict)

    return jsonify(cafes=cafe_list)

@app.route("/search")
def search_cafe():
    loc = request.args.get("loc")

    if not loc:
        return jsonify(error={"Bad Request": "Missing 'loc' parameter"}), 400

    cafe_list = []
    with app.app_context():
        cafes = db.session.execute(db.select(Cafe).where(Cafe.location == loc)).scalars().all()

        if cafes:
            for cafe in cafes:
                cafe_dict = dict(cafe.__dict__)
                cafe_dict.pop("_sa_instance_state", None)
                cafe_list.append(cafe_dict)
            return jsonify(cafes=cafe_list)
        else:
            return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location"}), 404

# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    with app.app_context():
        name = request.form.get("name")
        map_url = request.form.get("map_url")
        img_url = request.form.get("img_url")
        location = request.form.get("location")
        seats = request.form.get("seats")
        has_toilet = request.form.get("has_toilet") == "true"  # Convert to bool
        has_wifi = request.form.get("has_wifi") == "true"
        has_sockets = request.form.get("has_sockets") == "true"
        can_take_calls = request.form.get("can_take_calls") == "true"
        coffee_price = request.form.get("coffee_price")

        cafe = Cafe(
            name = name,
            map_url = map_url,
            img_url = img_url,
            location = location,
            seats = seats,
            has_toilet = has_toilet,
            has_wifi = has_wifi,
            has_sockets = has_sockets,
            can_take_calls = can_take_calls,
            coffee_price = coffee_price,
        )
        db.session.add(cafe)
        db.session.commit()
    return jsonify(response={"Success": "Successfully added the new cafe."})

# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    with app.app_context():
        cafe = db.get_or_404(
            Cafe, cafe_id,
            description=f"Sorry a cafe with that id was not found in the database."
        )
        new_price = request.args.get("new_price")

        cafe.coffee_price = new_price
        db.session.commit()

    return jsonify(response={"Success": "Successfully updated the price."})

# HTTP DELETE - Delete Record
@app.route("/delete/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api_key")

    if api_key != SECRET_KEY:
        return jsonify(response={"Error": "Sorry, that's not allowed. Make sure you have the correct api key."})
    else:
        with app.app_context():
            cafe = db.get_or_404(
                Cafe, cafe_id,
                description=f"Sorry a cafe with that id was not found in the database."
            )

            db.session.delete(cafe)
            db.session.commit()

        return jsonify(response={"Success": "Successfully deleted the entry."})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
