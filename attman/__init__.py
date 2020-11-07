from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads

app = Flask(__name__)
app.config["SECRET_KEY"] = "enterasecretkeyhere"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///data.db"
app.config["UPLOADED_CSVFILES_DEST"] = "uploads"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
csvfiles = UploadSet("csvfiles", extensions=("csv"))
configure_uploads(app, csvfiles)

from attman import routes
