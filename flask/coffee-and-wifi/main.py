from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config["SECRET_KEY"] = "really_cool_secret_key"
Bootstrap5(app)

class CafeForm(FlaskForm):
    cafe_name = StringField(
        "Cafe name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Cat & Coffee Cafe"}
    )

    cafe_location = StringField(
        "Cafe Location on Google Maps (URL)",
        validators=[DataRequired(), URL()],
        render_kw={"placeholder": "https://goo.gl/maps/cat_coffee_cafe"}
    )

    opening_time = StringField(
        "Opening Time",
        validators=[DataRequired()],
        render_kw={"placeholder": "11:00 AM"}
    )

    closing_time = StringField(
        "Closing Time (e.g., 11:01 AM)",
        validators=[DataRequired()],
        render_kw={"placeholder": "1:00 PM"}
    )

    coffee_rating = SelectField(
        "Coffee Rating",
        validators=[DataRequired()],
        choices=[("✘", "✘") if i == 0 else ("☕" * i, "☕" * i) for i in range(0,6)]
    )

    wifi_rating = SelectField(
        "Wi-Fi Rating",
        validators=[DataRequired()],
        choices=[("✘", "✘") if i == 0 else ("📶" * i, "📶" * i) for i in range(0,6)]
    )

    power_rating = SelectField(
        "Power Rating",
        validators=[DataRequired()],
        choices=[("✘", "✘") if i == 0 else ("🔌" * i, "🔌" * i) for i in range(0,6)]
    )

    submit = SubmitField(
        "Submit"
    )

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe_name = form.cafe_name.data
        cafe_location = form.cafe_location.data
        open_time = form.opening_time.data
        close_time = form.closing_time.data
        coffee_rating = form.coffee_rating.data
        wifi_rating = form.wifi_rating.data
        power_rating = form.power_rating.data

        cafe_data = [cafe_name, cafe_location, open_time, close_time, coffee_rating, wifi_rating, power_rating]

        with open("cafe-data.csv", mode="a", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(cafe_data)
        return redirect(url_for("home"))
    else:
        return render_template("add.html", form=form)


@app.route("/cafes")
def cafes():
    with open("cafe-data.csv", newline="", encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template("cafes.html", cafes=list_of_rows)


if __name__ == "__main__":
    app.run(debug=True)
