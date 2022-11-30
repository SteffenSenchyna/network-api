import flask
from flask import request, Response
from app import interface

app = flask.Flask(__name__)

@app.route("/switch/interfaces", methods=["GET"])
def get_int():
    res = interface.get_int(request)
    return res

@app.route("/switch/interfaces", methods=["POST"])
def create_int():
    res = interface.create_int(request)
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port =8081)