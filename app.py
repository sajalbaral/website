from flask import Flask, render_template, request 

from src.connection import Account
from src.connection import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

@app.get('/home')
def home():
    Account.query.all()
    return render_template("home.html")

@app.get('/create')
def create():
    return render_template("create.html")

@app.get('/login')
def login():
    return render_template("login.html")

@app.get('/profile')
def profile():
    return render_template("profile.html")

@app.get('/signup')
def signup():
    return render_template("signup.html")

@app.post('/signup')
def post_signup():
    if 'username' in request.form and 'password' in request.form:
        user = request.form.get('username')
        passwd = request.form.get('password')

        print(user)
        print(passwd)

        result = Account.query.filter(Account.username == user).first() 

        if result == None:

            #Created new user account
            new_account = Account(username=user, password=passwd)
            db.session.add(new_account)
            db.session.commit()

            #TODO: Show that account was created on HTML

            print("Created brand new user account")
        else:
            print("Could not create new user account because username is already taken")

    return render_template("signup.html")

@app.post('/login')
def post_login():
    if 'username' in request.form and 'password' in request.form:
        user = request.form.get('username')
        passwd = request.form.get('password')

        result = Account.query.filter(Account.username == user, Account.password == passwd).first()
        if not result == None:
            #Successful login
            #TODO: Save session in browser

            print("Successful login")
        else:
            #Invalid username or password
            #TODO: Show invalid username or password on HTML
            print("Invalid login - username or password is incorrect")

    return render_template("login.html")
