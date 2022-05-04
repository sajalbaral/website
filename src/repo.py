from src.connection import Account, Post

def get_account_by_login(username, password):
    result = Account.query.filter(Account.username == username, Account.password == password).first()
    return result

def get_account_by_username(username):
    result = Account.query.filter(Account.username == username).first()
    return result

def get_account_by_id(id):
    result = Account.query.filter(Account.id == id).first()
    return result

def get_post_by_account():
    return

def create_post():
    
    return

def remove_post():
    return