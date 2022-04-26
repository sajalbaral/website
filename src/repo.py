from src.connection import Account

def get_account_by_login(username, password):
    result = Account.query.filter(Account.username == username, Account.password == password).first()
    return result

def get_account_by_username(username):
    result = Account.query.filter(Account.username == username, Account.password == password).first()
    return result

def get_account_by_id(id):
    result = Account.query.filter(Account.id == id).first()
    return result