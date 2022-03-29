from flask import Flask, render_template, request 
app = Flask(__name__)

@app.get('/home')
def home():
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