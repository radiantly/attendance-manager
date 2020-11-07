from flask import render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user
from flask_uploads import UploadNotAllowed

import hashlib
from pathlib import Path

# from flask_uploads import file_allowed
from attman import app, db, bcrypt, csvfiles
from attman.forms import RegistrationForm, LoginForm, UploadForm
from attman.models import User, AttnFile
from attman.csvparse import parseAttendanceCSV, getMeetingDate


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        form = UploadForm()
        if form.validate_on_submit():
            try:
                filename = csvfiles.save(form.csvfile.data)
                parseAttendanceCSV(filename)
                filePath = filePath = Path.cwd() / "uploads" / filename
                fileHash = hashlib.md5(filePath.read_bytes()).hexdigest()
                fileDate = getMeetingDate(filename)
                if not fileDate:
                    flash("Error parsing file.", "danger")
                elif AttnFile.query.filter_by(
                    filehash=fileHash, user_id=current_user.id
                ).first():
                    flash("This file already exists in the database.", "danger")
                else:
                    attnFile = AttnFile(
                        filename=filename,
                        filehash=fileHash,
                        date=fileDate,
                        user_id=current_user.id,
                    )
                    db.session.add(attnFile)
                    db.session.commit()
                    flash(f"Your file has been successfully uploaded.", "success")
            except UploadNotAllowed:
                flash("Invalid upload", "danger")
        return render_template("start.html", form=form)
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            f"Your account has been successfully created. You may login now.", "success"
        )
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("home"))
        flash("Login Unsuccessful. Please check your email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("You have been successfully logged out", "success")
    return redirect(url_for("home"))