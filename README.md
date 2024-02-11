# Web Programming with Python and JavaScript

## Description:
Project 1 is a web application developed for the Web Programming course, integrating Python and JavaScript technologies. The project focuses on creating a dynamic platform for book management and user interaction.

## Features:
- **Login and Registration:** Utilizing HTML forms, users can register or log in to access the system. Incorrect login attempts are handled gracefully with error messages.
- **User Dashboard:** Upon successful login, users are directed to their dashboard (index.html), where they can view selected books and search for additional titles.
- **Book Details:** Clicking on a book redirects users to a detailed book page (book.html), displaying information such as author, year, ISBN, along with ratings and reviews fetched from the Goodreads API.
- **Review System:** Users can leave reviews and ratings (up to 5 stars) for books. Each user can only submit one review per book.
- **Session Management:** Users can log out at any time, clearing their session and returning to the login page.

## Technologies Used:
- **Flask:** Used as the web framework to handle routing and requests.
- **Flask-Session:** For managing user sessions securely.
- **psycopg2-binary:** PostgreSQL adapter for Python, facilitating interaction with the database.
- **SQLAlchemy:** Used for database management and ORM functionalities.

## Files Structure:
- **application.py:** Main application file containing routing, database queries, and other functions.
- **import.py:** Script to import book data from books.csv into the database and create necessary tables.
- **requirements.txt:** List of dependencies required for the project.
- **templates:** Directory containing HTML templates for different pages.
- **static/stylesheet:** Directory containing CSS files for styling.
- **books.csv:** CSV file containing book data to be imported into the database.

## Requirements:
- Python
- Flask
- Flask-Session
- psycopg2-binary
- SQLAlchemy

## How to Run:
1. Ensure Python and required dependencies are installed.
2. Run `python import.py` to import book data and set up the database.
3. Run `python application.py` to start the Flask server.
4. Access the application via the provided URL.
