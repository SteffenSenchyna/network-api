import flask
from flask import request, Response
from app import interface, user

app = flask.Flask(__name__)

@app.route("/network/backup", methods=["POST"])
def get_int():
    res = interface.get_int(request)
    return res

@app.route("/switch/interfaces", methods=["POST"])
def create_int():
    res = interface.create_int(request)
    return res

@app.route("/switch/users", methods=["POST"])
def create_user():
    res = user.create_user(request)
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port =8081)