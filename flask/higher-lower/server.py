from flask import Flask
import random

app = Flask(__name__)
random_number = random.randint(0, 9)

RANDOM_GIF = "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHowZTh6djZjbDA3dDlpb3R4cDRlemp6eGkzaGFmZGc1ZXJ5cm9jZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/glJdAXojfP3wPEg84a/giphy.gif"
LOW_CAT_GIF = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmlhbTVtaDdqdWltbnp0MnE0cmRycmxibW1kNDBub2d3emFyYTBlcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jJcPUoQkI68bC/giphy.gif"
HIGH_CAT_GIF = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnVtNjBwNWZqdXdhYWcxejF5aHQ1amdlZTh3NW83cHJmM2YxcmM0diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/s0FHfz2O4yaJ2/giphy.gif"
JUST_RIGHT_CAT_GIF = "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWlzcTdqa3I0OXlyM2dtNjNwa3ZneG5kazQzeHhwaHBjMm14M3JnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/lOlPYr2w94s02P8Q9V/giphy.gif"


def make_bold_decorator(function):
    def wrapper(*args, **kwargs):
        return f"<b>{function(*args, **kwargs)}</b>"
    return wrapper

def colour_hint_decorator(function):
    def color_wrapper(*args, **kwargs):
        number = kwargs.get("number")

        if number > random_number:
            html = function(*args, **kwargs)
            return html.replace("<h1 style='", "<h1 style='color: blue; ")
        elif number < random_number:
            html = function(*args, **kwargs)
            return html.replace("<h1 style='", "<h1 style='color: red; ")
        else:
            html = function(*args, **kwargs)
            return html.replace("<h1 style='", "<h1 style='color: green; ")
    return color_wrapper

@app.route("/")
@make_bold_decorator
def guess_homepage():
    return (f"<h1 style='text-align: center'>Guess a number between 0 and 9"
            f"<br/> <img src={RANDOM_GIF}> </h1>")

@app.route("/<int:number>")
@colour_hint_decorator
def user_guess(number):
    if number > random_number:
        msg = "Too high, try again!"
        gif = HIGH_CAT_GIF
    elif number < random_number:
        msg = "Too low, try again!"
        gif = LOW_CAT_GIF
    else:
        msg = "You found me!"
        gif = JUST_RIGHT_CAT_GIF

    return (f"<h1 style='text-align: center'>{msg}"
            f"<br/> <img src={gif}> </h1>")

if __name__ == "__main__":
    app.run(debug=True)