from flask import request
from Controllers import Users
from Helpers.Authentication import Authenticated, Verify


def register(app):

    @app.route('/', methods=['POST'])
    @Verify
    def getToken(user, token):
        return Users.verify(user, str(token))

    @app.route('/users', methods=['GET'])
    @Authenticated
    def list():
        return Users.list()

    @app.route('/users/<id>', methods=['GET'])
    def details(id):
        return Users.details(id)

    @app.route('/users', methods=['POST'])
    def post():
        return Users.post()

    @app.route('/users/<id>', methods=['PUT'])
    def update(id):
        return Users.update(id)

    @app.route('/users/<id>', methods=['DELETE'])
    def delete(id):
        return Users.delete(id)
