import os
from flask import request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

import cv2

from models import application, db, ImageDB
from config import Config

if not os.path.exists(application.config['UPLOAD_FOLDER']):
    os.makedirs(application.config['UPLOAD_FOLDER'])

if not os.path.exists(application.config['DB_FILE']):
    db.create_all()


def allowed_file(filename):
    ret = False
    _, ext = os.path.splitext(filename)
    if ext in Config.ALLOWED_EXTENSIONS:
        ret = True
    return ret


@application.route('/')
def index():
    all_data = ImageDB.query.all()
    file_list = [d.image_file for d in all_data]
    return render_template('start.html', file_list=file_list)


@application.route('/show/<filename>')
def show_zoom(filename):
    ret = 'Unknown error occurred.'
    dat = db.session.query(ImageDB).filter_by(image_file=filename).first()
    if dat is None:
        ret = render_template('notify.html',
                              title="ERROR!!",
                              msg="Cannot find image:{}.".format(filename),
                              target="/")
    else:
        ret = render_template('zoom.html',
                              image=dat.image_file, posx=dat.posx, posy=dat.posy)
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
        if Config.MAX_IMAGE_WIDTH < width:
            img_small = cv2.resize(img, (Config.MAX_IMAGE_WIDTH, Config.MAX_IMAGE_WIDTH * height // width))
            cv2.imwrite(filepath, img_small)

        return render_template('specify_center.html', imgfile=filename)
    return render_template('file_upload.html',
                           msg='An <b>error</b> occurred when uploading file.')


@application.route('/store_center_pos', methods=['POST'])
def store_center_pos():
    filename = request.form['imgfile']
    posx = int(request.form['posx'])
    posy = int(request.form['posy'])

    image = db.session.query(ImageDB).filter_by(image_file=filename).first()
    if image is None:
        image = ImageDB(image_file=filename, posx=posx, posy=posy)
        db.session.add(image)
    else:
        image.posx = posx
        image.posy = posy
    db.session.commit()
    return redirect(url_for('register_success'))


@application.route('/success')
def register_success():
    return render_template('notify.html',
                           title="SUCCESS!!",
                           msg="Please press the right button to register another image",
                           target="/register_image")


@application.route('/imgs/<filename>')
def get_image(filename):
    return send_from_directory(application.config['UPLOAD_FOLDER'], filename)


@application.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    application.debug = True
    application.run()
