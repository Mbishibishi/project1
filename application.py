from xml.etree import ElementTree as ET
import os, json, requests, datetime, re
from flask import Flask, session, request, render_template, redirect, url_for, abort, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps
from sqlalchemy.sql import text
from wtforms.validators import ValidationError
from PIL import Image
import forms
from forms import RegistrationForm, SearchBook, CommentBox, Sign_in, Update
from book import Book
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = 'cs50w'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
Session(app)



# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

""" takes in a country's code(string) and returns its full text. """
def country_by_code(code):
    dict_countries = {"BD": "Bangladesh", "BE": "Belgium", "BF": "Burkina Faso", "BG": "Bulgaria", "BA": "Bosnia and Herzegovina", "BB": "Barbados", "WF": "Wallis and Futuna", "BL": "Saint Barthelemy", "BM": "Bermuda", "BN": "Brunei", "BO": "Bolivia", "BH": "Bahrain", "BI": "Burundi", "BJ": "Benin", "BT": "Bhutan", "JM": "Jamaica", "BV": "Bouvet Island", "BW": "Botswana", "WS": "Samoa", "BQ": "Bonaire, Saint Eustatius and Saba ", "BR": "Brazil", "BS": "Bahamas", "JE": "Jersey", "BY": "Belarus", "BZ": "Belize", "RU": "Russia", "RW": "Rwanda", "RS": "Serbia", "TL": "East Timor", "RE": "Reunion", "TM": "Turkmenistan", "TJ": "Tajikistan", "RO": "Romania", "TK": "Tokelau", "GW": "Guinea-Bissau", "GU": "Guam", "GT": "Guatemala", "GS": "South Georgia and the South Sandwich Islands", "GR": "Greece", "GQ": "Equatorial Guinea", "GP": "Guadeloupe", "JP": "Japan", "GY": "Guyana", "GG": "Guernsey", "GF": "French Guiana", "GE": "Georgia", "GD": "Grenada", "GB": "United Kingdom", "GA": "Gabon", "SV": "El Salvador", "GN": "Guinea", "GM": "Gambia", "GL": "Greenland", "GI": "Gibraltar", "GH": "Ghana", "OM": "Oman", "TN": "Tunisia", "JO": "Jordan", "HR": "Croatia", "HT": "Haiti", "HU": "Hungary", "HK": "Hong Kong", "HN": "Honduras", "HM": "Heard Island and McDonald Islands", "VE": "Venezuela", "PR": "Puerto Rico", "PS": "Palestinian Territory", "PW": "Palau", "PT": "Portugal", "SJ": "Svalbard and Jan Mayen", "PY": "Paraguay", "IQ": "Iraq", "PA": "Panama", "PF": "French Polynesia", "PG": "Papua New Guinea", "PE": "Peru", "PK": "Pakistan", "PH": "Philippines", "PN": "Pitcairn", "PL": "Poland", "PM": "Saint Pierre and Miquelon", "ZM": "Zambia", "EH": "Western Sahara", "EE": "Estonia", "EG": "Egypt", "ZA": "South Africa", "EC": "Ecuador", "IT": "Italy", "VN": "Vietnam", "SB": "Solomon Islands", "ET": "Ethiopia", "SO": "Somalia", "ZW": "Zimbabwe", "SA": "Saudi Arabia", "ES": "Spain", "ER": "Eritrea", "ME": "Montenegro", "MD": "Moldova", "MG": "Madagascar", "MF": "Saint Martin", "MA": "Morocco", "MC": "Monaco", "UZ": "Uzbekistan", "MM": "Myanmar", "ML": "Mali", "MO": "Macao", "MN": "Mongolia", "MH": "Marshall Islands", "MK": "Macedonia", "MU": "Mauritius", "MT": "Malta", "MW": "Malawi", "MV": "Maldives", "MQ": "Martinique", "MP": "Northern Mariana Islands", "MS": "Montserrat", "MR": "Mauritania", "IM": "Isle of Man", "UG": "Uganda", "TZ": "Tanzania", "MY": "Malaysia", "MX": "Mexico", "IL": "Israel", "FR": "France", "IO": "British Indian Ocean Territory", "SH": "Saint Helena", "FI": "Finland", "FJ": "Fiji", "FK": "Falkland Islands", "FM": "Micronesia", "FO": "Faroe Islands", "NI": "Nicaragua", "NL": "Netherlands", "NO": "Norway", "NA": "Namibia", "VU": "Vanuatu", "NC": "New Caledonia", "NE": "Niger", "NF": "Norfolk Island", "NG": "Nigeria", "NZ": "New Zealand", "NP": "Nepal", "NR": "Nauru", "NU": "Niue", "CK": "Cook Islands", "XK": "Kosovo", "CI": "Ivory Coast", "CH": "Switzerland", "CO": "Colombia", "CN": "China", "CM": "Cameroon", "CL": "Chile", "CC": "Cocos Islands", "CA": "Canada", "CG": "Republic of the Congo", "CF": "Central African Republic", "CD": "Democratic Republic of the Congo", "CZ": "Czech Republic", "CY": "Cyprus", "CX": "Christmas Island", "CR": "Costa Rica", "CW": "Curacao", "CV": "Cape Verde", "CU": "Cuba", "SZ": "Swaziland", "SY": "Syria", "SX": "Sint Maarten", "KG": "Kyrgyzstan", "KE": "Kenya", "SS": "South Sudan", "SR": "Suriname", "KI": "Kiribati", "KH": "Cambodia", "KN": "Saint Kitts and Nevis", "KM": "Comoros", "ST": "Sao Tome and Principe", "SK": "Slovakia", "KR": "South Korea", "SI": "Slovenia", "KP": "North Korea", "KW": "Kuwait", "SN": "Senegal", "SM": "San Marino", "SL": "Sierra Leone", "SC": "Seychelles", "KZ": "Kazakhstan", "KY": "Cayman Islands", "SG": "Singapore", "SE": "Sweden", "SD": "Sudan", "DO": "Dominican Republic", "DM": "Dominica", "DJ": "Djibouti", "DK": "Denmark", "VG": "British Virgin Islands", "DE": "Germany", "YE": "Yemen", "DZ": "Algeria", "US": "United States", "UY": "Uruguay", "YT": "Mayotte", "UM": "United States Minor Outlying Islands", "LB": "Lebanon", "LC": "Saint Lucia", "LA": "Laos", "TV": "Tuvalu", "TW": "Taiwan", "TT": "Trinidad and Tobago", "TR": "Turkey", "LK": "Sri Lanka", "LI": "Liechtenstein", "LV": "Latvia", "TO": "Tonga", "LT": "Lithuania", "LU": "Luxembourg", "LR": "Liberia", "LS": "Lesotho", "TH": "Thailand", "TF": "French Southern Territories", "TG": "Togo", "TD": "Chad", "TC": "Turks and Caicos Islands", "LY": "Libya", "VA": "Vatican", "VC": "Saint Vincent and the Grenadines", "AE": "United Arab Emirates", "AD": "Andorra", "AG": "Antigua and Barbuda", "AF": "Afghanistan", "AI": "Anguilla", "VI": "U.S. Virgin Islands", "IS": "Iceland", "IR": "Iran", "AM": "Armenia", "AL": "Albania", "AO": "Angola", "AQ": "Antarctica", "AS": "American Samoa", "AR": "Argentina", "AU": "Australia", "AT": "Austria", "AW": "Aruba", "IN": "India", "AX": "Aland Islands", "AZ": "Azerbaijan", "IE": "Ireland", "ID": "Indonesia", "UA": "Ukraine", "QA": "Qatar", "MZ": "Mozambique"}
    return dict_countries[code]


""" a helper function, takes the user id(int) and query the database(user table)
and returns a tuple containing the user's details(number of reviews submitted,
profile picture file name, username, email, country, and a list of books the user
reviewed in form of dictionary with isbn and date as keys, an example -> [{isbn1:value, date1:value},
{isbn2:value, date2:value}])."""

def basic_info(id):
    data_row = db.execute(\
            "SELECT username, email, country, booksreviewed, profilepic_file FROM users\
                WHERE id=:user_id", {"user_id": id}).fetchone()
    name =  (data_row.username).capitalize()
    if len(name) > 20:
        name = name[:17] + '...'
    email, country = data_row.email, data_row.country                               
    country = country_by_code(str(data_row.country))        
    booksreviewed = data_row.booksreviewed
    numreviews = 0
    profilePic_file = data_row.profilepic_file
    if booksreviewed == None:
        booksreviewed = []
    else:
        booksreviewed = list(booksreviewed)
        numreviews = len(booksreviewed)    
    return (numreviews, profilePic_file, name, email, country, booksreviewed)


""" A helper function, takes in the index(int when used by delete_review and delete_account functions) of a review in
 the reviewsperid column of the reviews table in the database, index = '-1' when the addAndEdit_review is deleting the
previous review in order to add a new one, and the isbn of the book, then performs a deletionof that review and update 
the row in which it was located in the database. This include the total number of rates and deleting the row if there
 are no more review left. It is used in the addAndEdit_review, delete_account and delete_review functions."""

def review_helper(index, isbn):
            
    review = {'id':None}
    if index == '-1':
        row = db.execute("SELECT reviewsperid AS reviews, totalrates FROM reviews WHERE bookisbn = :token", {"token": f'{isbn}'}).fetchone() 
        if row is None:
            return
        for elt in row.reviews:
            if elt['id'] == session['user_id']:
                review = elt
                break
                    
    elif index != '-1':
        row = db.execute("SELECT reviewsperid[:index] AS review, totalrates FROM reviews WHERE bookisbn = :token", { "index": int(index) + 1, "token": f'{isbn}'}).fetchone()#adding 1 on the index because json indices begin from 1 not 0      
        review = row.review
    totalrates = row.totalrates
        
    if review['id'] == session['user_id']:
        ID = review['id']
        body = review['body']
        new = '' #this will replace the body(review text) after the for loop which escapes characters that may cause trouble.
        for char in range(len(body)):
            if body[char] in ['"','\\']:
                new += f'\\{body[char]}'
            elif body[char] == "'":
                new += "'" + body[char]          
                
            else:
                new += body[char]
        rate = review['rate']
        date = review['date'] 
        name = review['name']
        profilePic_file = review['profilepic_file']
        newtotal = totalrates
        if totalrates != 'null' and rate != 'null':
            newtotal = int(totalrates) - int(rate)   
        db.get_bind().execute(text(f'UPDATE reviews SET totalrates={newtotal}, reviewsperid = array_remove(reviewsperid, \'{{"id": {ID},"body": "{new}", "date" : "{date}", "name": "{name}", "rate": "{rate}", "profilepic_file": "{profilePic_file}"}}\'::jsonb) WHERE bookisbn = \'{isbn}\''))
        db.get_bind().execute(text(f'UPDATE users SET booksreviewed = array_remove(booksreviewed, \'{{"date": "{date}","isbn": "{isbn}"}}\'::jsonb) WHERE id = {ID}'))
        ar = db.execute(f"SELECT reviewsperid FROM reviews WHERE bookisbn = '{isbn}'").fetchone() 
        if len(ar.reviewsperid) == 0:
            db.execute(f"DELETE FROM reviews WHERE bookisbn = '{isbn}'") 
        db.commit()            


""" The home page, takes the user to a page where the can choose to register
or login if they are not logged in yet, and takes them to their dashboard if they
have logged in already. """

@app.route("/", methods = ['POST', 'GET'])
def index():
    login_form = Sign_in()
    if 'user_id' in session and request.method == 'GET':
        return redirect(url_for('dashboard'))

    elif request.method == 'POST' and login_form.validate_on_submit():
        session.clear()
        email = request.form.get('email')
        password = request.form.get('password')
        userId = db.execute('SELECT id FROM users WHERE email = :email AND password = :password', {'email' : email, 'password': password}).fetchone()
        if userId is not None:
            session['user_id'] = userId[0]   
            return redirect(url_for('dashboard'))
        elif userId is None:
            flash('No matching account has been found, try again.', 'danger')
                
    return render_template("index.html", topTitle='Home')  



""" wrapper function to check whether a user is logged in before accessing certain routes."""
def logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' in session:
            return f(*args, **kwargs)
        else:            
            flash('Sorry, you should login first!', 'danger')                      
            return redirect(url_for('login')) 
    return wrap        



""" login page checks whether the input credentials(email and password) are valid,
if valid, redirects to the index function, otherwise return the login form again."""
@app.route("/login", methods = ['POST', 'GET'])
def login():
    login_form = Sign_in()
    if request.method == 'POST' and login_form.validate_on_submit():
        session.clear()
        email = request.form.get('email')
        password = request.form.get('password')
        userId = db.execute('SELECT id FROM users WHERE email = :email AND password = :password', {'email' : email, 'password': password}).fetchone()
        if userId is not None:
            session['user_id'] = int(userId[0])
            return redirect(url_for("index"))
        elif userId is None:
            flash('No matching account has been found, try again.', 'danger')
            return redirect(url_for("login"))
    return render_template('login.html', login_form = login_form)




""" helper function takes the username(string), submitted file(or picture's path in the satic folder),
and it converts the picture into jpg, adjust the size, and changes its filename to be the username
to avoid duplicate name since usernames are unique, saves it in the static folder in the profile_photos folder,
and returns the new pictures filename. It is used to update the user's profile picture in the dashbord function."""

def profile_picture(username, data):
    profilePic_file = username +  '.jpg'
    pic_path = os.path.join(app.root_path, 'static/profile_photos', profilePic_file)
    output_size = (498, 499)
    i = Image.open(data)
    i.thumbnail(output_size)
    converted = i.convert('RGB')
    converted.save(pic_path)
    return profilePic_file
    


""" Uses flask's wtform to register users and create accounts in the database.
email and username are unique, and it assigns a default profile picture to the user depending
on their gender. It also initializes the booksreviewed column of the database's users table
to an empty jsonb array. All fields are required. After successfully creating the account, the user is redirected 
to the index function with a success message."""


@app.route("/registration", methods= ['POST', 'GET'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        username = (form.username.data).lower()
        exists = db.execute("SELECT id FROM users WHERE email = :token", {"token": f'{email}'}).fetchone() is not None 
        if exists:
            form.email.errors.append(ValidationError(f'Looks like account with the email you input is already exists.'))
        exists = db.execute("SELECT id FROM users WHERE username = :token", {"token": f'{username}'}).fetchone() is not None 
        if exists:
            form.username.errors.append(ValidationError(f'Username taken! Pick another username.'))        
        else:
            password = form.password.data
            country = form.country.data
            gender = form.gender.data
            filename = gender + '.png'            
            data = os.path.join(app.root_path, 'static/profile_photos/', filename)            
            profilePic_file = profile_picture(username, data)
            db.execute(f'INSERT INTO users (email, password, country, username, gender, profilepic_file , booksreviewed)\
                 VALUES (:email, :password, :country, :username, :gender, :profilepic_file, \'{{}}\'::jsonb[])',\
                     {"email": email, "password": password, "country": country, "username": username, "gender": gender, "profilepic_file": profilePic_file })    
            db.commit()
            flash(f'Congratulations {username.capitalize()}! your account has been successfully created. You can now login with your credentials.', 'success')            
            return redirect(url_for('index'))    
    return render_template('registration.html', form = form)

    

""" logs out the user and redirects them to the home page(index function)."""        
@app.route("/logout", methods = ['POST', 'GET'])
@logged_in
def logout():   
    session.pop('user_id')
    return redirect(url_for('index'))


""" Takes a string book token(isbn), get book's details(cover picture, official review,
average rates) by Goodreads api, and the book's author, title, year of release form the app's database,
then returns them to the book template."""
@app.route("/books/<string:book_token>" , methods = ['POST', 'GET'])
@logged_in
def chosen_book(book_token):

    if request.method == 'GET' or request.method == 'POST':
    
        if book_token:
            bookName, bookAuthor, bookIsbn, releaseYear = db.execute(\
                "SELECT title, author, isbn, year FROM books\
                  WHERE isbn = :token", {"token": book_token}).fetchone()               
            key = "Lt8awOLNA0pbVyGOwn3e1Q"
            resXml = requests.get(f"https://www.goodreads.com/book/isbn/{bookIsbn}?format=xml", params={"key": key})        
            desXml = ET.fromstring(resXml.content)
            description = (desXml.find('book/description')).text
            imageUrl = (desXml.find('book/image_url')).text
            resJson = (requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": bookIsbn})).json()
            rating_counts, avg_rating = resJson['books'][0]['work_ratings_count'], resJson['books'][0]['average_rating']
            allreviews = db.execute(f"SELECT reviewsperid, totalrates FROM reviews WHERE bookisbn = '{bookIsbn}'").fetchone() 
            reviews = []
            totalrates = 0
            if allreviews != None:
                reviews = allreviews.reviewsperid
                totalrates = allreviews.totalrates                         
            basic_infor = basic_info(int(session['user_id']))
            name = basic_infor[2]
            isReviewed = False
            for elt in basic_infor[5]:
                if elt['isbn'] == book_token:
                    isReviewed = True
                    break
            book = Book(bookName, bookAuthor, bookIsbn, releaseYear, bookImage=imageUrl, bookDescription=description, rating_counts=rating_counts, avg_rating=rating_counts)             
            return render_template('book.html', totalrates = totalrates, owner_id = session['user_id'], isReviewed = isReviewed, lgComment= reviews, form = SearchBook(), comment = CommentBox(),\
                book = book, name = name, topTitle=book.getBookName())
        
""" gets the user's input query in the search engine, and queries the database to find
possible matches, returns a list of the found matches, if any, to the template. Otherwise returns an empty list to the template."""        


@app.route("/search/book-matches", methods = ['POST', 'GET']) # I should be back to customise the url so that it contains individual token that can help in case some one copies the url and pastes it somewhere else.
@logged_in
def matching_books():
    
    if request.method == 'GET':    
        book_token = str(request.args.get('books'))        
        if book_token:
            rows = db.execute(\
                "SELECT title, author, isbn, year FROM books\
                    WHERE title LIKE :token OR author LIKE :token OR isbn LIKE :token", {"token": f'%{book_token}%'}).fetchall()               
            
            matching_books = []
            for row in rows:
                bookName, bookAuthor, bookIsbn, releaseYear = row.title, row.author, row.isbn, row.year
                matching_books.append(Book(bookName, bookAuthor, bookIsbn, releaseYear))        
            
            basic_infor = basic_info(int(session['user_id']))    
            name = basic_infor[2]
            email, country = basic_infor[3], basic_infor[4]                             
            numreviews = basic_infor[0]       
            profilePic_file = url_for('static', filename='profile_photos/' + basic_infor[1])
            
            return render_template('like_books.html', books = matching_books, form= SearchBook(), search_query= f'<{book_token}>',numreviews = numreviews, profilePic_file = profilePic_file, name = name, email = email, country = country, topTitle='Search results' )
            
""" Takes the username(string), book'isbn(string) and a boolean isReviewed, which is True when the user
has already reviewed the book, and False otherwise. Then makes sure that the previous review, if any, is deleted,
then update the reviews table and the user's review history in the database. Finale redirect to the book's page. """

@app.route("/add_and_edit/<string:name>/<string:isbn>/<string:isReviewed>", methods = ['POST'])
@logged_in
def addAndEdit_review(name, isbn, isReviewed):
    # db.begin(subtransactions=True)
    user_detail = db.execute(\
            "SELECT profilepic_file FROM users\
                WHERE id=:user_id", {"user_id": session['user_id']}).fetchone()
    profilePic_file = user_detail.profilepic_file
    if isReviewed:        
        review_helper('-1', isbn)       
    for book in basic_info(session['user_id'])[5]:
        if str(book['isbn']) == isbn:
            return redirect(url_for('chosen_book', book_token=isbn))
    
    rate = request.form.get('rate')
    if rate == 'null':
        rate = 0
    else:
        rate = int(rate)

                    
    comment = request.form.get('comment')
    comment = re.sub(r"\s+", " ", comment)
    date = datetime.datetime.now().strftime('%Y/%m/%d')
    ID = session['user_id']
    exists = db.execute("SELECT bookisbn, totalrates FROM reviews WHERE bookisbn = :token", {"token": f'{isbn}'}).fetchone() is not None               
    if len(comment) > 0:
        new = ''
        for char in range(len(comment)):
            if comment[char] in ['"','\\']:
                new += f'\\{comment[char]}'
            elif comment[char] == "'":
                new += "'" + comment[char]          
                
            else:
                new += comment[char]
               
        if exists:
            db.get_bind().execute(text(f'UPDATE reviews \
            SET totalrates = totalrates + {rate}, reviewsperid = reviewsperid || \'{{"id": {ID},"body": "{new}", "date" : "{date}", "name": "{name}", "rate": "{rate}", "profilepic_file": "{profilePic_file}"}}\'::jsonb WHERE bookisbn = \'{isbn}\''))
            
        elif not exists:            
            db.get_bind().execute(text(f'INSERT INTO reviews (bookisbn, totalrates, reviewsperid)\
            VALUES (\'{isbn}\', {rate}, array[\'{{"id": {ID},"body": "{new}", "date" : "{date}", "name": "{name}", "rate": "{rate}", "profilepic_file": "{profilePic_file}"}}\']::jsonb[])'))
            
        db.get_bind().execute(text(f'UPDATE users SET booksreviewed = booksreviewed || \'{{"date": "{date}","isbn": "{isbn}"}}\'::jsonb WHERE id = {ID}'))
    db.commit()  
    return redirect(url_for('chosen_book', book_token=isbn))


"""Takes in the index(int) of a review in the reviewsperid column
of the reviews table in the database, and the isbn(string) of the book, then performs a deletion
of that review and update the row in which it was located in the database. And redirects to the book's page. """
@app.route("/delete_review/<string:index>/<string:isbn>", methods = ['POST', 'GET'])
@logged_in
def delete_review(index, isbn):
    review_helper(index, isbn)
    return redirect(url_for('chosen_book', book_token=isbn))

    

""" Dashboard retuens to the template the review history(books s/he reviewed by date) of the user
and basic information about them such as country, username, email address and also their profile picture.
Also uses the profile_picture function to update the user's profile picture in the database if the user submits it."""


@app.route("/dashboard", methods = ['POST', 'GET'])
@logged_in
def dashboard():
    update = Update()
    if update.validate_on_submit():
        if update.profile_picture.data:
            usernameAndProfilePic = db.execute(f'SELECT username, profilepic_file FROM users WHERE id={session["user_id"]}').fetchone()
            data = update.profile_picture.data
            oldPic = usernameAndProfilePic.profilepic_file
            username = usernameAndProfilePic.username            
            profilePic_file = profile_picture(username, data)
            db.execute(f'UPDATE users SET profilepic_file = \'{profilePic_file}\'WHERE id={session["user_id"]}')
            db.commit()
            flash('Profile picture successfully updated! you may need to reload the page in order to see it.', 'success')
            return redirect(url_for('dashboard')) 

    basic_infor = basic_info(int(session['user_id']))    
    name = basic_infor[2]
    email, country = basic_infor[3], basic_infor[4]                             
    numreviews = basic_infor[0]        
    booksreviewed = basic_infor[5]
    history = []
    profilePic_file = url_for('static', filename='profile_photos/' + basic_infor[1])
    if len(booksreviewed) > 0:
        for book in booksreviewed:            
            date = str(book['date'])
            book_isbn = str(book['isbn'])            
            temp = db.execute("SELECT title, author, year FROM books WHERE isbn = :book", {"book": book_isbn}).fetchone()               
            
            history.append((temp.title, temp.author, book_isbn, temp.year, date))

    
    return render_template('dashboard.html', form=SearchBook(), update=Update(), history= history,numreviews = numreviews, name = name, email = email, country = country, profilePic_file=profilePic_file, topTitle=f'Dashboard/{name}' )

""" deletes the user's row in the users table in the database and all their activities in the reviews table of the database, it uses
the review_helper function to delete the the reviews. It also deletes the profile picture in the static folder in the profile_photos file."""


@app.route("/about", methods = ['POST', 'GET'])
def about():
    return render_template('about.html', topTitle= 'About-Contact')


@app.route("/delete_account", methods = ['POST', 'GET'])
@logged_in
def delete_account():
    profilePic = db.execute(\
            "SELECT profilepic_file FROM users\
                WHERE id=:user_id", {"user_id": session['user_id']}).fetchone()
    pic = profilePic.profilepic_file
       
    isbns_column = db.execute("SELECT bookisbn FROM reviews").fetchall()
    isbns = isbns_column[0]
    for isbn in isbns:
        isbn_row = db.execute(\
            f"SELECT reviewsperid FROM reviews WHERE bookisbn=\'{isbn}\'").fetchone()
        index = len(isbn_row.reviewsperid)-1 
        while index > -1:
            review_helper(index, isbn)
            index -= 1       
    os.remove('static/profile_photos/' + pic)        
    db.execute(f"DELETE FROM users WHERE id = {session['user_id']}")
    db.commit()
    return redirect(url_for('logout'))        
           


""" takes in a book's isbn, checks whether it is in the database, if not, it aborts a 404 error, if yes,
returns a json response containing the book's title, author, publication year, isbn, total number of reviews and average rate"""

@app.route("/api/<string:isbn>", methods = ['POST', 'GET'])
@logged_in
def book_api(isbn):
    book = db.execute(\
                "SELECT title, author, isbn, year FROM books\
                  WHERE isbn = :isbn", {"isbn": str(isbn)}).fetchone()
    if book is None:
        abort(404)
    else:
        bookName, bookAuthor, bookIsbn, releaseYear = book.title, book.author, book.isbn, book.year
    reviews =  db.execute(\
            f"SELECT reviewsperid, totalrates FROM reviews WHERE bookisbn= :isbn", {"isbn": str(isbn)}).fetchone()
    review_count = int(len(reviews.reviewsperid))
    avg_rating = float(reviews.totalrates)/review_count
    
    result = {
    "title": bookName,
    "author": bookAuthor,
    "year": releaseYear,
    "isbn": bookIsbn,
    "review_count": review_count,
    "average_score": round(avg_rating, 2) 
    }
    return json.dumps(result)

                                       


if __name__ == "__main__":
    main()    
