import os
import csv

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

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

def main():
    
    db.execute('CREATE TABLE users(id SERIAL PRIMARY KEY, password character varying(20), username character varying(15) UNIQUE, gender text, email text UNIQUE, country text, booksreviewed jsonb[], profilepic_file text);')

    db.execute('CREATE TABLE reviews(bookisbn character varying UNIQUE, reviewsperid jsonb[], totalrates integer);')

    db.execute('CREATE TABLE books(isbn character varying UNIQUE,title character varying, author character varying, year integer);')


   
    f = open("books.csv")
    reader = csv.reader(f)
    index = False # just to skip the headers of the table columns.
    for isbn,title,author,year in reader:
        if index == True:
            db.execute("INSERT INTO Books(isbn,title,author,year) VALUES (:isbn,:title,:author,:year)",
            {"isbn": isbn, "title": title ,"author": author, "year": year})
        index = True
    db.commit()

if __name__== "__main__":
    main()         
