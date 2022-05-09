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

def get_all_posts():
    all_posts = Post.query.all()
    all_posts.reverse()
    return all_posts

def get_post_by_account(id):
    all_posts = Post.query.filter(Post.account_id == id).all()
    return all_posts

def get_post_by_id(id):
    post = Post.query.filter(Post.post_id == id).first()
    return post

def create_post():
    
    return

def remove_post():
    return