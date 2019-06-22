from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config.from_object("config")

from routes.get import application

app.register_blueprint(application)


if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0', port='5000')