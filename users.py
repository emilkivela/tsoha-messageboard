from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

def get_users(user_id):
    sql = "SELECT username, id FROM users WHERE NOT id=:user_id"
    result = db.session.execute(sql, {"user_id" : user_id})
    return result.fetchall()

def signin(username, password):
    hash_value = generate_password_hash(password)
    sql = "SELECT id, password FROM Users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        sql = "INSERT INTO Users (username, password, admin) VALUES (:username, :password, :admin)"
        db.session.execute(sql, {"username":username, "password":hash_value, "admin":"FALSE"})
        db.session.commit()
        return True
    return False

def login(username, password):
    sql = "SELECT id, password FROM Users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["user_id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False
def logout():
    del session["user_id"]