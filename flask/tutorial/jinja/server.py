from flask import Flask, render_template
import datetime, random, requests

AGIFY_ENDPOINT = "https://api.agify.io"
GENDERIZE_ENDPOINT = "https://api.genderize.io"
NATIONALIZE_ENDPOINT = "https://api.nationalize.io"
RESTCOUNTRIES_ENDPOINT = "https://restcountries.com/v3.1/alpha/"
BLOG_ENDPOINT = "https://api.npoint.io/c790b4d5cab58020d391"

app = Flask(__name__)

@app.route("/")
def home():
    random_number = random.randint(0,9)
    current_year = datetime.datetime.today().year
    return render_template("index.html", num=random_number, current_year=current_year)

@app.route("/guess/<name>_<last_name>")
def guess_name(name: str, last_name: str):
    first_name_params = {
        "name": name.title()
    }

    last_name_params = {
        "name": last_name.title()
    }

    # AGIFY API - Guesses age given first name
    agify_response = requests.get(AGIFY_ENDPOINT, first_name_params)
    agify_response.raise_for_status()

    age = agify_response.json()["age"]

    # GENDERIZE API - Guesses gender given first name
    genderize_response = requests.get(GENDERIZE_ENDPOINT, first_name_params)
    genderize_response.raise_for_status()

    gender = genderize_response.json()["gender"]

    # NATIONALIZE API - Guesses nationality given last name
    nationalize_response = requests.get(NATIONALIZE_ENDPOINT, last_name_params)
    nationalize_response.raise_for_status()

    nationality = nationalize_response.json()["country"][0]["country_id"]

    # REST Countries API - Converts country code to full name
    rest_countries_response = requests.get(f"{RESTCOUNTRIES_ENDPOINT}{nationality}")
    rest_countries_response.raise_for_status()

    full_country = rest_countries_response.json()[0]["name"]["common"]

    return render_template("guess_name.html", name=name.title(), gender=gender, age=age, nationality=full_country)

@app.route("/blog")
def blog():
    response = requests.get(BLOG_ENDPOINT)
    response.raise_for_status()
    all_posts = response.json()
    return render_template("blog.html", posts=all_posts)

if __name__ == "__main__":
    app.run(debug=True)