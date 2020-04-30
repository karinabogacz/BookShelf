import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for, json, jsonify
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

        #Make sure fields are not empty and username is not taken

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

        #Check if username and password are in the database

        if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount == 0:
            return render_template ("login.html", message = "Wrong username or password")
        else:
            session["user"] = username
            return redirect(url_for("search"))

    return render_template("login.html")

@app.route("/search", methods = ['GET', 'POST'])
def search():

    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        search_input = request.form.get("search")
        query = "%" + search_input + "%"

        search_input_lower = search_input.lower()
        query_lower = "%" + search_input_lower + "%"

        search_results = db.execute("SELECT * FROM books WHERE isbn LIKE :query OR title = :search_input OR LOWER(title) LIKE :query_lower OR LOWER(author) LIKE :query_lower",
        {"query": query, "search_input": search_input, "query_lower": query_lower})

        #Count the results
        
        row_count = search_results.rowcount

        if row_count == 0:
            return render_template ("search_results.html", message = "No results found :(")

        else:
            return render_template ("search_results.html", search_results = search_results, row_count = row_count)

    books = db.execute ("SELECT * FROM books WHERE year < 2000 LIMIT 50").fetchall()
    return render_template("search.html", user=session["user"], books = books)

@app.route ("/book/<string:isbn>", methods = ['GET', 'POST'])
def book(isbn):

    if "user" not in session:
        return redirect(url_for('login'))

    book_info = db.execute ("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()

    #Get data from goodreads

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "sFWzz4zaiCJ0jAqfXLMb5g", "isbns": isbn})

    if res.status_code == 200:
        data = res.json()
    else:
        raise Exception("Error: Api request unsuccesful")

    work_ratings_count = data["books"][0]["work_ratings_count"]
    average_rating = data["books"][0]["average_rating"]
    session['work_ratings_count'] = work_ratings_count
    session['average_rating'] = average_rating

    #GET BOOK ID and convert it to INT type

    book_id = db.execute("SELECT id FROM books WHERE isbn = :isbn", {"isbn": isbn})
    
    for result_proxy in book_id:
        book_id_dict = dict(result_proxy)
    book_id_int = book_id_dict["id"]

    #Get reviews and rates

    book_reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book_id_int})

    if request.method == "POST":

        #GET USER ID and convert it to INT type

        username = session.get('user', None)
        user_id = db.execute("SELECT id FROM users WHERE username = :username", {"username": username})
        
        for result_proxy in user_id:
            user_id_dict = dict(result_proxy)
        user_id_int = user_id_dict["id"]

        #Check if the user has already reviewed the book

        if db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id", {"user_id": user_id_int, "book_id": book_id_int}).rowcount != 0:
            return render_template ("book.html", book_info = book_info, book_reviews = book_reviews, work_ratings_count = work_ratings_count, average_rating = average_rating, message_error2 = "You have already reviewed this book!")

        review_content = request.form.get("review")
        review_rate = int(request.form.get("rate"))

        try:
            db.execute("INSERT INTO reviews (user_id, book_id, content, rate) VALUES (:user_id, :book_id, :content, :rate)",
            {"user_id": user_id_int, "book_id": book_id_int, "content": review_content, "rate": review_rate})
            db.commit()
            return render_template ("book.html", book_info = book_info, book_reviews = book_reviews, work_ratings_count = work_ratings_count, average_rating= average_rating, message = "Your review has been posted")
                
        except:
            return render_template ("book.html", book_info = book_info, book_reviews = book_reviews, work_ratings_count = work_ratings_count, average_rating = average_rating, message_error1 = "There was a problem in posting your review")

    return render_template ("book.html", book_info = book_info, book_reviews = book_reviews, work_ratings_count = work_ratings_count,  average_rating= average_rating)
    

@app.route ("/logout")
def logout():
    session.pop("user", None)
    return render_template ("login.html")

@app.route ("/api/<string:isbn>")
def book_api(isbn):

    #Make sure book exists
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return jsonify ({"error": "Invalid isbn"}), 404

    work_ratings_count = session.get('work_ratings_count', None)
    average_rating = session.get('average_rating', None)

    return jsonify ({
        "title": book[2],
        "author": book[3],
        "year": book[4],
        "isbn": book[1],
        "review_count": work_ratings_count,
        "average_score": average_rating
    })

  
if __name__ == "__main__":
    main()