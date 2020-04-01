import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = "key"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template ("index.html")

@app.route("/sign_up", methods=['GET','POST'])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = str(request.form.get("password"))

        if username == "" or email == "" or password == "":
            return render_template ("sign_up.html", message = "You need to fill in all fields")
        try:
            db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)", {"username": username, "email": email, "password": password})
            db.commit()
            session["user"] = username
            return redirect(url_for('search'))
        except:
            return render_template("sign_up.html", message = "Username taken")
    return render_template("sign_up.html")

@app.route("/login", methods=['GET','POST'])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount == 0:
            return render_template ("login.html", message = "Wrong username or password")
        else:
            session["user"] = username
            return redirect(url_for("search"))

    return render_template("login.html")

@app.route("/search")
def search():
    if "user" in session:
        return render_template("search.html", user=session["user"] ) 
    else:
        return redirect(url_for("login"))

@app.route ("/logout")
def logout():
    session.pop("user", None)
    return render_template ("login.html")