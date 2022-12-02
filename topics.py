from db import db

def get_topics():
    sql = "SELECT name, creator, created_at, id FROM topics"
    result = db.session.execute(sql)
    return result

def get_name(id):
    sql = "SELECT name FROM topics WHERE topics.id=:id"
    result = db.session.execute(sql, {"id" : id})
    return result.fetchone()