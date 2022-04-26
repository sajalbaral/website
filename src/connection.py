from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'Account({self.id}, {self.username}, {self.password})'
    
class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, nullable=False)
    #TODO: add photo field, don't know how to do that yet :(
    caption = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)