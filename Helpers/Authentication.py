from flask import request, current_app as app
from jwt import encode, decode
from hashlib import sha224 # could be md5 or others
from Helpers import Response
from Models import Users
secret = "VerySecretKey"


def Authenticated(func):
    def validateToken(*args, **kwargs):
        token = request.headers.get("token")
        if token == None:
            return Response.send({}, "Missing Authentication token", 401)

        try:
            request.user = decode(token, secret)
        except:
            return Response.send({}, "Invalid Authentication token", 401)

        return func(*args, **kwargs)

    return validateToken


def Verify(func):
    def JWT(*args, **kwargs):
        email = request.json.get("email")
        password = request.json.get("password")
        user, error = Users.verify(email, password)
        if(error):
            return Response.send({}, "Invalid Credentials", error)
        token = encode(
            {"id": user[0], "email": user[1], "phone": user[2]}, secret).decode('UTF-8')
        print(type(token))
        return func(user, token)

    return JWT


def hash(password):
    passwd = password.encode('utf-8')
    hashedPass = sha224(passwd).hexdigest()
    print("\n=======\n", password, hashedPass)
    return hashedPass
