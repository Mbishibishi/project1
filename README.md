# Project 1

Web Programming with Python and JavaScript

About the files:

1) application.py contains the routes, imports and configurations and a few helper functions. There are docstrings above every function in this file which explains what the function does.

2.1) forms.py is where all forms are defined as all forms in the app are wtf forms.

2.2) book.py contains a Book class which is used in the routes to create a book instances according to its details(author, isbn, etc) before rendering them to the templates in order to avoid having a very long return statement with many variables in it which may look messy.

2.3) import.py contains the code that uploads books from books.csv to the database.


3) the hmtl pages are the templates, each according to its name. 
for example: dashboard.hmtl being th dashboard page, etc.


4) The static folder:
4.1) profile_photos contains the profile pictures of the users in addition to the male and female avatar which becomes the user's default profile picture.
4.2) styles.css contains the styles of the pages, however there are a few styles in the html files also.
4.3) styles2.css contains the styles for registration.hmtl and login.hmtl only because they are slitly different from the rest of the files as they do not inherit from layout.hmtl.


In addition:

1) The reviewsperid column in the reviews table of the database is
a jsonb array which contains the reviewer id, review text, the date the review was submitted on and rate in jsonb format. For example 

[{id:id1, body:text, date:date, name:username, rate:rate, profilepic_file:value},{id:id2, body:review_text, date:date, name:username, rate:rate, profilepic_file:value},{id: id3, body:review_text, date:date, name:username, rate:rate, profilepic_file:value}] 


2) The booksreviewed column in the users table of the database is a jsonb array which contains the reviewed book isbns and dates of reviews in jsonb format. for example

[{isbn1:value, date:value},{isbn2:value, date:date}]

Initial it is [] when the user has not reviewed any book yet.

3) Whenever there is a variable 'name', it refers to the username.

4) The dates are stored in the database and displayed in the templates as strings.

5) The app also uses goodreads api to get the description and cover image of the books through an xml response. I was only able to do it by following the instructions in the goodreads api page.

6) In the video I uploaded the app seems to be so slow because 1) the video  recorder is heavy and my computer has a small processor, 2) there is also the effect of the vpn I use to access Goodreads api because currently Goodreads is blocked in china, where I am now.