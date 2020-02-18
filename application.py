import os
from flask import request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

from PIL import Image

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
    file_list = [{'file': d.image_file, 'title': d.title} for d in all_data]
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
                              image=dat.image_file,
                              posx=dat.posx,
                              posy=dat.posy,
                              duration_in_sec=10,
                              zoom_ratio=50)
    return ret


@application.route('/register_image', methods=['GET'])
def pre_upload():
    return render_template('file_upload.html',
                           msg='Please choose an image (JPG or PNG) and upload.')


@application.route('/register_image', methods=['POST'])
def do_upload():
    file = request.files['file']
    title = request.form['title']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(application.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        img = Image.open(filepath)
        height, width = img.size
        if Config.MAX_IMAGE_WIDTH < width:
            img.thumbnail((Config.MAX_IMAGE_WIDTH, Config.MAX_IMAGE_WIDTH * height // width))
            img.save(filepath)

        if len(title) == 0:
            title = filename
        return render_template('specify_center.html', title=title, imgfile=filename)
    return render_template('file_upload.html',
                           msg='An error occurred when uploading file.')


@application.route('/store_center_pos', methods=['POST'])
def store_center_pos():
    filename = request.form['imgfile']
    title = request.form['title']
    posx = int(request.form['posx'])
    posy = int(request.form['posy'])

    image = db.session.query(ImageDB).filter_by(image_file=filename).first()
    if image is None:
        image = ImageDB(image_file=filename, title=title, posx=posx, posy=posy)
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
