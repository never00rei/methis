from flask import Blueprint, render_template, url_for, current_app
from time import gmtime, strftime
import logging

logger = logging.getLogger('__name__')

application = Blueprint("challenge", __name__, url_prefix="/")

@application.route("/")
@application.route("/home")
def home():
    print("Request to / or /home.")
    hour = str(strftime('%H', gmtime()))
    print(f"Hour is: {hour}")
    config = current_app.config['DATA_SOURCE']
    checksum = config[hour]['checksum']
    payload = config[hour]['payload']

    return render_template("home.html", checksum=checksum, payload=payload)