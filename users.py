from db import db

def get_users(user_id):
    sql = "SELECT username, id FROM users WHERE NOT id=:user_id"
    result = db.session.execute(sql, {"user_id" : user_id})
    return result.fetchall()