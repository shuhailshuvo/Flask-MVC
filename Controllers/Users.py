from flask import request
from Models import Users
from Helpers import Response


def list():
    users, error = Users.list()
    if(error):
        return Response.send({}, "", error)
    return Response.send(users, "Successfully fetched")


def details(id):
    user, error = Users.details(id)
    if(error):
        return Response.send({}, "", error)
    return Response.send(user, "Successfully fetched")


def verify(user={}, token=""):
    return Response.send({"user": user, "token": token}, "Successfully Verified")


def post():
    userId, error = Users.create(request.json)
    if(userId):
        return Response.send({"userId": userId}, "Successfully created", 201)
    return Response.send({}, "Email already exists", error)


def update(id):
    user = Users.update(id, request.json)
    return Response.send(user, "Successfully updated")


def delete(id):
    user = Users.delete(id)
    return Response.send(user, "Successfully deleted", 202)
