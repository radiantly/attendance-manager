from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "enterasecretkeyhere"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///data.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from attman import routes
