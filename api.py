import flask
from flask import request, Response
from app import backup

app = flask.Flask(__name__)

@app.route("/network/backup", methods=["POST"])
def post_backup():
    res = backup.postBackup(request)
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
