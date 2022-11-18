from db import db

def get_list(thread_id):
    sql = "SELECT M.content, U.username FROM messages M, users U WHERE M.author=U.id AND M.thread=:thread_id"
    result = db.session.execute(sql, {"thread_id" : thread_id})
    return result.fetchall()
