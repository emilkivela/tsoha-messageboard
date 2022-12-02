from db import db

def get_list(id):
    sql = ("SELECT T.name, U.username, T.id, (SELECT COUNT(content) FROM messages WHERE messages.thread=T.id) FROM threads T, users U WHERE T.topic=:id AND T.creator=U.id")
    result = db.session.execute(sql, {"id" : id})
    return result.fetchall()

def get_name(id):
    sql = ("SELECT name, id FROM threads WHERE id=:id")
    result = db.session.execute(sql, {"id" : id})
    return result.fetchone()

def add_thread(name, creator, topic):
    sql = "INSERT INTO threads (name, creator, topic, created_at) values (:name, :creator, :topic, NOW())"
    db.session.execute(sql, {"name": name, "creator" : creator, "topic" : topic})
    db.session.commit() 