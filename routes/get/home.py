from flask import Blueprint, render_template, url_for

application = Blueprint("challenge", __name__, url_prefix="/")

@application.route("/")
@application.route("/home")
def home():
    return render_template("home.html")