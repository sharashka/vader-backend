import initdb
import schemas

def test():
    return {"status": "test ok"}

def test2():
    return {"status": "test2 ok"}

def testdb():
    return initdb.users

def getUserEmail(username: str):
    initdb.cursor.execute("select email from users where username=:who", {"who": username})
    return initdb.cursor.fetchone()

def register_new_user(user: schemas.User):
    initdb.cursor.execute("select username from users where username=:who", {"who": user.username})
    user_record= initdb.cursor.fetchone()
    if user_record is None:
        userdict = user.dict()
        userdict['created_date'] = userdict['created_date'].strftime('%Y-%m-%d')
        _query_keys = ','.join([ f'{key}' for key in userdict])
        _query_values = ','.join([ f'?' for key in userdict])
        query = f"insert into users ({_query_keys}) values ({_query_values})"
        print(query)
        response = initdb.cursor.execute(query, userdict.values())
    return response