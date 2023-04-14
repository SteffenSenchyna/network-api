import flask
from flask import request, Response
from app import backup, scan

app = flask.Flask(__name__)


@app.route("/health", methods=["GET"])
def health_check():
    return Response("Alive", status=200)


@app.route("/network/backup", methods=["POST"])
def post_backup():
    res = backup.postBackup(request)
    return res


@app.route("/network/scan", methods=["GET"])
def get_scan():
    res = scan.getScan()
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
