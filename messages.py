from db import db

def get_list(thread_id):
    sql = "SELECT M.content, U.username, M.sent_at, M.id FROM messages M, users U WHERE M.author=U.id AND M.thread=:thread_id ORDER BY M.id"
    result = db.session.execute(sql, {"thread_id" : thread_id})
    return result.fetchall()

def direct_message(sender, to, content):
    sql = "INSERT INTO directs (content, author, receiver, sent_at) VALUES (:content, :author, :receiver, NOW())"
    db.session.execute(sql, {"content" : content, "author" : sender, "receiver": to})
    db.session.commit()

def get_directs(user_id):
    sql = "SELECT D.content, U.username, D.sent_at FROM directs D, users U WHERE D.receiver=:user_id AND U.id=D.author"
    result = db.session.execute(sql, {"user_id" : user_id})
    received = result.fetchall()
    sql = "SELECT D.content, U.username, D.sent_at FROM directs D, users U WHERE D.author=:user_id AND U.id=D.receiver"
    result = db.session.execute(sql,{"user_id" : user_id})
    sent = result.fetchall()
    return received, sent

def add_message(message, id, user_id):
    sql = "INSERT INTO messages (content, thread, author, sent_at) VALUES (:content, :thread, :author, NOW());"
    db.session.execute(sql, {"content" : message, "thread": id, "author" : user_id })
    db.session.commit()

def find_message(thread_id, query):
    sql = "SELECT DISTINCT   M.content, U.username, M.sent_at FROM messages M, users U, threads T WHERE M.thread=:thread_id AND M.author=U.id AND content LIKE :query"
    result = db.session.execute(sql, {"thread_id" : thread_id, "query" : "%"+query+"%"})
    return result.fetchall()

def check_permission(user_id, message_id):
    sql = "SELECT M.author FROM messages M, users U WHERE M.author=U.id AND M.id=:message_id"
    result = db.session.execute(sql, {"message_id" : message_id})
    if user_id == result.fetchone()[0]:
        return True
    else:
        return False

def delete_message(message_id):
    sql = "DELETE FROM messages WHERE id=:message_id"
    db.session.execute(sql, {"message_id" : message_id})
    db.session.commit()