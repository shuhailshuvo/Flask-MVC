from flask import current_app as app
from DB import MySQL, Mongo
from Helpers.Authentication import hash

db = MySQL.connect()
cursor = db.cursor()

mdb = Mongo.connect("users")


def list():
    cursor.execute("select id, name, email, phone from users")
    result = __format__(cursor)
    if(result == None or len(result) < 1):
        return False, 204
    return result, False


def details(id):
    cursor.execute(
        "select id, name, email, phone from users where id="+str(id))
    record = cursor.fetchone()
    if(record == None or len(record) < 1):
        return False, 204
    return record, False


def alreadyExists(email):
    cursor.execute("select id from users where email='"+email+"'")
    record = cursor.fetchone()
    if record:
        return True
    return False


def verify(email, password):
    hashedPass = hash(password)
    print(hashedPass, password)
    cursor.execute("select id, name, email, phone from users where email='" +
                   email+"' and password='"+hashedPass+"'")
    record = cursor.fetchone()
    if(record == None or len(record) < 1):
        return False, 404

    return record, False


def create(json):
    if alreadyExists(json['email']):
        return False, 400
    hashedPass = hash(json['password'])
    # mysql
    id = __create_in_mysql__(json, hashedPass)
    # mongo
    __create_in_mongo__(json, hashedPass, id)

    return id, False


def update(id, data):
    __update_in_mysql__(data, id)
    __update_in_mongo__(data, id)
    return True


def delete(id):
    cursor.execute("delete from users where id="+id)
    db.commit()
    mdb.delete_one({'id': int(id)})
    return True


def __format__(cursor):
    fields = map(lambda x: x[0], cursor.description)
    return [dict(zip(fields, row)) for row in cursor.fetchall()]


def __create_in_mysql__(json, hashedPass):
    query = "insert into users(name, email, phone, password) VALUES ('" +\
        json["name"]+"', '"+json["email"]+"','" +\
        json["phone"]+"','"+hashedPass+"')"

    cursor.execute(query)
    db.commit()

    return __get_last_id__()


def __update_in_mysql__(data, id):
    query = "update users"
    if data.get("name"):
        query += " set name='"+data["name"]+"'"
    if data.get("email"):
        query += " set email='"+data["email"]+"'"
    if data.get("phone"):
        query += " set phone='"+data["phone"]+"'"
    query += " where id="+id
    cursor.execute(query)
    db.commit()


def __get_last_id__():
    cursor.execute("select id from users order by id desc")
    record = cursor.fetchone()
    return record[0]


def __create_in_mongo__(json, hashedPass, id):
    mdb.insert_one({
        'id': id,
        'name': json["name"],
        'email': json["email"],
        'phone': json["phone"],
        'password': hashedPass
    })


def __update_in_mongo__(data, id):
    mdb.update_one({'id': int(id)}, {"$set": data})
