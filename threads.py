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

def check_permission(user_id, thread_id):
    sql = "SELECT T.creator FROM threads T, users U WHERE T.creator=U.id AND T.id=:thread_id"
    result = db.session.execute(sql, {"thread_id" : thread_id})
    if user_id == result.fetchone()[0]:
        return True
    else:
        return False

def delete_thread(thread_id):
    sql = "DELETE FROM threads WHERE id=:thread_id"
    db.session.execute(sql, {"thread_id" : thread_id})
    db.session.commit()