import os

from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, exc

from models import DB_URL, ImageDB

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploaded')
ALLOWED_EXTENSIONS = set(['.jpg', '.jpeg', '.JPG', '.png', '.PNG'])


application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)


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


@application.route('/register_image', methods=['GET'])
def pre_upload():
    return render_template('file_upload.html', msg='Please select an image and upload.')


@application.route('/register_image', methods=['POST'])
def do_upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
        return render_template('specify_center.html', imgfile=filename)
    return render_template('file_upload.html',
                           msg='An error occurred when uploading file:{}'.format(file.filename))


@application.route('/store_center_pos', methods=['POST'])
def store_center_pos():
    filename = request.form['imgfile']
    posx = int(request.form['posx'])
    posy = int(request.form['posy'])
    session = Session()
    try:
        image = session.query(ImageDB).filter(ImageDB.image_file == filename).one()
        image.posx = posx
        image.posy = posy
    except exc.NoResultFound:
        image = ImageDB(image_file=filename, posx=posx, posy=posy)
        session.add(image)
    session.commit()
    return render_template('file_upload.html',
                           msg='Image file:{} successfully registered.'.format(filename))


@application.route('/test')
def test():
    return render_template('test.html')


@application.route('/imgs/<filename>')
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    application.debug = True
    application.run()
