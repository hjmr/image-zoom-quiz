import os

from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploaded')
ALLOWED_EXTENSIONS = set(['.jpg', '.jpeg', '.JPG', '.png', '.PNG'])


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
    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(application.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        ret = True
    return ret, filename


@application.route('/')
def index():
    return 'not yet ready'


@application.route('/upload_image', methods=['GET'])
def pre_upload():
    return render_template('file_upload.html', msg='Please select an image and upload.')


@application.route('/upload_image', methods=['POST'])
def do_upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
        return render_template('specify_center.html', imgfile=filename)
    return render_template('file_upload.html',
                           msg='An error occurred when uploading file:{}'.format(file.filename))


@application.route('/test')
def test():
    return render_template('test.html')


@application.route('/imgs/<filename>')
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    application.debug = True
    application.run()
