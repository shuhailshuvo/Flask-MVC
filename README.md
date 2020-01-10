# Python MVC REST Framework (Flask)

DIY-1: Prepare MVC skeleton for REST API with MySQL & MongoDB implemented

## Folder Structure

|-> Controllers
|-> DB
|-> Helpers
|-> Models
|-> Routes
|-> App.py (Entry point)

## Application

Application needs to be registered with flask

```
from flask import Flask
app = Flask(__name__)
```

## Routes

Flask comes with a built-in route decorator, that can be used to register application routes.
First parameter to the `route()` is the url & second one is the request method
Matched request will be redirected to the function followed by the `@app.route()` decorator

```
from Controllers import Application

@app.route('/', methods=['GET'])
def default():
    # Forward request to
    return Application.index()

```

Here, we are forwarding the request to `index()` function of `Application` controller

## Controller

Controllers are responsible for receiving & validating inputs and filter them through business logics

```
from flask import request
from Models import Users
from Helpers import Response

def list():
    users, error = Users.list()
    if(error):
        return Response.send({}, "", error)
    return Response.send(users, "Successfully fetched")
```

The `request` object from flask contains all information about request. Like: `request.url`, `request.method`, `request.form`, `request.json` etc.

## Model

Models are used to separate the data layer from business logics.

```
def create(email, password):
    if alreadyExists(email):
        return False, 400

    hashedPass = hash(password)

    # mysql
    id = __create_in_mysql__(json, hashedPass)

    # mongo
    __create_in_mongo__(json, hashedPass, id)

    return id, False
```

## DB

DB files are simply database connectors.

```
import mysql.connector

def connect():
    connection = mysql.connector.connect(host='localhost', database='pydb', user='root', password='')
    return connection
```

Or, connecting MongoDB

```
from pymongo import MongoClient

def connect(table):
    client = MongoClient('mongodb://localhost:27017')
    return client.pydb[table]

```

## Helpers

Simple helper functions and decorators

```
from flask import request, jsonify

def send(data, message, status=200):
    return jsonify({"data": data, "message": message}), status
```
