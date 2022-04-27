from pickle import TRUE
from flask import Flask, redirect, render_template, request, flash, session

from src.connection import Account
from src.connection import db
from src.repo import get_account_by_username, get_account_by_login, get_account_by_id

app = Flask(__name__)
app.secret_key = 'secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:NickyNicky@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
@app.get('/')
def index():
    if not 'user_id' in session:
        return redirect('/login')
    else:
        return redirect('/home')

@app.get('/home')
def home():
    if not 'user_id' in session:
        return redirect('/login')
    User = get_account_by_id(session['user_id'])
    return render_template("home.html", nav = get_nav_data(), usr = User)

@app.get('/create')
def create():
    if not 'user_id' in session:
        return redirect('/login')
    return render_template("create.html", nav = get_nav_data())

@app.get('/login')
def login():
    if 'user_id' in session:
        return redirect('/home')
    return render_template("login.html", nav = get_nav_data())

@app.get('/profile')
def profile():
    if not 'user_id' in session:
        return redirect('/login')
    return render_template("profile.html", nav = get_nav_data())

@app.get('/signup')
def signup():
    if 'user_id' in session:
        return redirect('/home')
    return render_template("signup.html", nav = get_nav_data())

@app.post('/signup')
def post_signup():
    if 'username' in request.form and 'password' in request.form:
        user = request.form.get('username')
        passwd = request.form.get('password')

        print(user)
        print(passwd)

        result = get_account_by_username(user)

        if result == None:

            #Created new user account
            new_account = Account(username=user, password=passwd)
            db.session.add(new_account)
            db.session.commit()

            #TODO: Show that account was created on HTML

            print("Created brand new user account")
        else:
            print("Could not create new user account because username is already taken")

    return render_template("signup.html", nav = get_nav_data())

@app.route('/login', methods=['GET', 'POST'])
def post_login():
    if 'username' in request.form and 'password' in request.form:
        user = request.form.get('username')
        passwd = request.form.get('password')

        result = get_account_by_login(user, passwd)
        if not result == None:
            session['user_id'] = result.id

            print("Successful login")
            return redirect('/home')
        else:
            #Invalid username or password
            #TODO: Show invalid username or password on HTML
            print("Invalid login - username or password is incorrect")
    return render_template("login.html", nav = get_nav_data())

@app.route('/logout')
def logout():
    session.pop('user_id')
    print('Logged out user')
    return redirect('/home')

def get_nav_data():
    nav_links = {}
    if not 'user_id' in session:
        nav_links['Login'] = 'login'
    else:
        nav_links['Home'] = 'home'
        nav_links['Create'] = 'create'
        nav_links['Profile'] = 'profile'
        nav_links['Logout'] = 'logout'
    return nav_links

