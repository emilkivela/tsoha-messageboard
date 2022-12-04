from db import db

def get_topics():
    sql = "SELECT topics.name, topics.id, (SELECT COUNT(id) FROM threads WHERE threads.topic=topics.id) FROM topics"
    result = db.session.execute(sql)
    return result

def get_name(id):
    sql = "SELECT name FROM topics WHERE topics.id=:id"
    result = db.session.execute(sql, {"id" : id})
    return result.fetchone()

def add_topic(thread_name, user_id):
    sql = "INSERT INTO topics (name, creator, created_at) VALUES (:thread_name, :user_id, NOW())"
    db.session.execute(sql, {"thread_name" : thread_name, "user_id" : user_id})
    db.session.commit()