from db import db

def get_list(thread_id):
    sql = "SELECT M.content, U.username, M.created_at FROM messages M, users U WHERE M.author=U.id AND M.thread=:thread_id ORDER BY M.id"
    result = db.session.execute(sql, {"thread_id" : thread_id})
    return result.fetchall()
