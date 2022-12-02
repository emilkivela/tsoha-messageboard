from db import db

def get_topics():
    sql = "SELECT name, creator, created_at, id FROM topics"
    result = db.session.execute(sql)
    return result