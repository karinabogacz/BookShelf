# Project 1 for Web Programming with Python and JavaScript

In templates directory there are all html files. login.html file extends layout_home.html. Threre are two forms in login page, one for registering a second for logging in. Both of them extend layout_enter.html. Succesfully registered user can try log in, in case of incorrect data message shows. Once logged in username displays next to log out button.

User is redirected to index.html after logged in. If index is requested by GET, some chosen books will be displayed and users will be able search more books in database. If index is requested by POST (searching for books) list of books shows. Clicking one of the positions takes redirects to book.html (bookpage), which extends layout_home.html

On bookpage author, year and isbn are loaded as well as rating count and average rate from goodread.com API. Also all reviews received from users along with ratings are loaded. There is also a plece where user can leave their review and rating of max 5 stars. User can only leave 1 review for each book.

Clicking Log out button session is cleared and users is logging out, login.html page is loaded after.

application.py is a main app file. Contains routing to all html files , queries to database and all other functions.
import.py take books from books.csv file and import them into database, as well as creates all needed tables.
