from pickle import TRUE
from src.dummy import DummyPost
from flask import Flask, redirect, render_template, request, flash, session
import datetime
from src.connection import Account, Post
from src.connection import db
from src.repo import get_account_by_username, get_account_by_login, get_account_by_id, get_all_posts, get_post_by_account, get_post_by_id
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('CLEARDB_DATABASE_URL')
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

    posts = get_all_posts()
    dummy_posts = []
    for post in posts:
        dummy = DummyPost(post.post_id, get_account_by_id(post.account_id), post.photo_link, post.caption, post.date_posted)
        dummy_posts.append(dummy)

    return render_template("home.html", nav = get_nav_data(), usr = User, posts = dummy_posts)

@app.get('/create')
def create():
    if not 'user_id' in session:
        return redirect('/login')
    return render_template("create.html", nav = get_nav_data())

@app.post('/post')
def post():
    if not 'user_id' in session:
        return redirect('/login')

    if 'Photo' in request.form and 'caption' in request.form:
        Photo = request.form.get('Photo')
        caption = request.form.get('caption')
        x = datetime.now()
        print(Photo)
        print(caption)
        new_post = Post( photo_link=Photo, account_id=session['user_id'], caption=caption, date_posted=x.strftime("%B %d, %Y"))
        db.session.add(new_post)
        db.session.commit()
        return redirect('/post/' + str(new_post.post_id))
    return None

@app.get('/login')
def login():
    if 'user_id' in session:
        return redirect('/home')
    return render_template("login.html", nav = get_nav_data())

@app.get('/profile')
def profile():
    if not 'user_id' in session:
        return redirect('/login')

    all_posts = get_post_by_account(session['user_id'])
    all_posts.reverse()
    return render_template("profile.html", nav = get_nav_data(), posts = all_posts)

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

    return render_template("login.html", nav = get_nav_data())

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


@app.route('/post/<id>')
def post_page(id):
    if not 'user_id' in session:
        return redirect('/login')
    
    post = get_post_by_id(id)
    dummy = DummyPost(post.post_id, get_account_by_id(post.account_id), post.photo_link, post.caption, post.date_posted)
    return render_template("post.html", nav = get_nav_data(), post = dummy)

@app.route('/edit/<id>')
def edit_page(id):
    if not 'user_id' in session:
        return redirect('/login')
    
    post = get_post_by_id(id)
    dummy = DummyPost(post.post_id, get_account_by_id(post.account_id), post.photo_link, post.caption, post.date_posted)

    if not post.account_id == int(session['user_id']):
        print("Can't edit")
        #Not allowed to edit this post because it's not the same user who posted it
        return redirect('../post/' + str(post.post_id))
    
    return render_template("edit.html", nav = get_nav_data(), post = dummy)

@app.post('/edit/<id>')
def submit_edit(id):
    if not 'user_id' in session:
        return redirect('/login')
    
    if 'Photo' in request.form and 'caption' in request.form:
        post = get_post_by_id(id)
        Photo = request.form.get('Photo')
        caption = request.form.get('caption')

        post.photo_link = Photo
        post.caption = caption
        db.session.commit()
        return redirect('/post/' + str(id))

@app.post('/delete/<id>')
def delete(id):
    if not 'user_id' in session:
        return redirect('/login')
    
    post = get_post_by_id(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/profile')

@app.route('/logout')
def logout():
    session.pop('user_id')
    print('Logged out user')
    return redirect('/home')

def get_nav_data():
    nav_links = {}
    if not 'user_id' in session:
        nav_links['Login'] = '../login'
    else:
        nav_links['Home'] = '../home'
        nav_links['Create'] = '../create'
        nav_links['Profile'] = '../profile'
        nav_links['Logout'] = '../logout'
    return nav_links

