from db import db

def get_list():
    sql = ("SELECT T.name, U.username FROM threads T, users U WHERE T.op = U.id")
    result = db.session.execute(sql)
    return result.fetchall()