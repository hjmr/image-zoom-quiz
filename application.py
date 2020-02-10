import os

from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, exc

import cv2

import models
from models import ImageDB

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploaded')
DB_FOLDER = os.path.abspath(os.path.dirname(__file__))

ALLOWED_EXTENSIONS = set(['.jpg', '.jpeg', '.JPG'])
MAX_IMAGE_WIDTH = 1280
DB_FILE = 'image_db.sqlite3'

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

DB_URL = 'sqlite:///{}'.format(DB_FILE)
db_exists = os.path.exists(os.path.join(DB_FOLDER, DB_FILE))

engine = create_engine(DB_URL)
if not db_exists:
    models.Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def allowed_file(filename):
    ret = False
    _, ext = os.path.splitext(filename)
    if ext in ALLOWED_EXTENSIONS:
        ret = True
    return ret


@application.route('/')
def index():
    session = Session()
    all_data = session.query(ImageDB).all()
    file_list = [d.image_file for d in all_data]
    session.close()
    return render_template('start.html', file_list=file_list)


@application.route('/show/<filename>')
def show_zoom(filename):
    session = Session()
    ret = 'Unknown error occurred.'
    try:
        dat = session.query(ImageDB).filter(ImageDB.image_file == filename).one()
        ret = render_template('zoom.html',
                              image=dat.image_file, posx=dat.posx, posy=dat.posy)
    except exc.NoResultFound:
        ret = render_template('notify.html',
                              title="ERROR!!",
                              msg="Cannot find image:{}.".format(filename),
                              target="/")
    return ret


@application.route('/register_image', methods=['GET'])
def pre_upload():
    return render_template('file_upload.html', msg='Please select an image and upload.')


@application.route('/register_image', methods=['POST'])
def do_upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(application.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        img = cv2.imread(filepath)
        height, width, _ = img.shape[:3]
        if MAX_IMAGE_WIDTH < width:
            img_small = cv2.resize(img, (MAX_IMAGE_WIDTH, MAX_IMAGE_WIDTH * height // width))
            cv2.imwrite(filepath, img_small)

        return render_template('specify_center.html', imgfile=filename)
    return render_template('file_upload.html',
                           msg='An <b>error</b> occurred when uploading file.')


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
    session.close()
    return redirect(url_for('register_success'))


@application.route('/success')
def register_success():
    return render_template('notify.html',
                           title="SUCCESS!!",
                           msg="Please press the right button to register another image",
                           target="/register_image")


@application.route('/test')
def test():
    return render_template('test.html')


@application.route('/imgs/<filename>')
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    application.debug = True
    application.run()
