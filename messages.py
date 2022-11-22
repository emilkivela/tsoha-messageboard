from db import db

def get_list(thread_id):
    sql = "SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE M.author=U.id AND M.thread=:thread_id ORDER BY M.id"
    result = db.session.execute(sql, {"thread_id" : thread_id})
    return result.fetchall()

def direct_message(sender, to, content):
    sql = "INSERT INTO directs (content, author, receiver, sent_at) VALUES (:content, :author, :receiver, NOW())"
    db.session.execute(sql, {"content" : content, "author" : sender, "receiver": to})
    db.session.commit()

def get_directs(user_id):
    sql = "SELECT D.content, U.username, D.sent_at FROM directs D, users U WHERE D.receiver=:user_id AND U.id=D.author"
    result = db.session.execute(sql, {"user_id" : user_id})
    return result.fetchall()

def add_message(message, id, user_id):
    sql = "INSERT INTO messages (content, thread, author, sent_at) VALUES (:content, :thread, :author, NOW());"
    db.session.execute(sql, {"content" : message, "thread": id, "author" : user_id })
    db.session.commit()
