from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, FileField
from wtforms.validators import DataRequired, URL
from flask_wtf.file import FileAllowed


class ImageUploadField(FileField):
    def __init__(self, label=None, validators=None, **kwargs):
        if validators is None:
            validators = [FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')]
        else:
            validators.append(FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!'))
        super(ImageUploadField, self).__init__(label, validators, **kwargs)


class UploadForm(FlaskForm):
    image_url =URLField(label="Image Url")
    image = ImageUploadField('Image')
    submit = SubmitField("Check Now")