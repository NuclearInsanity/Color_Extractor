from extractor import Extractor
from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, FileField, MultipleFileField
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = "RBudY8Kem1lDlq9eTykb3kDQw7ge2wt1+tmrGpNdgYA"
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

extractor = Extractor()


class FileForm(FlaskForm):
    photo = FileField(label='Image File', validators=[FileAllowed(photos, u'Image only!'), FileRequired(u'File was empty!')])
    submit = SubmitField('Extract colors ⭐️')


@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = FileForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
        file_url = file_url[1:]
        plot = extractor.exact_color(file_url, extractor.resize_number, extractor.tolerance, extractor.zoom)
        return render_template('index.html', form=form, file_url=file_url)
    else:
        file_url = None
        return render_template('index.html', form=form, file_url=file_url)



if __name__ == "__main__":
    app.run(debug=True)




