import os

from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploaded')
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'JPG', 'png', 'PNG'])


application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    ret = False
    _, ext = os.path.splitext(filename)
    if ext in ALLOWED_EXTENSIONS:
        ret = True
    return ret


def saveFile(file):
    ret = False
    filename = None
    if fileAllowed(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        ret = True
    return ret, filename


@application.route("/")
def index():
    return "not yet ready"


@application.route("/test")
def test():
    return render_template("test.html")


@application.route('/imgs/<filename>')
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    application.debug = True
    application.run()
