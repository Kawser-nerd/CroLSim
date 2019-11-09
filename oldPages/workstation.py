import os
from wtforms import Form, TextAreaField,  StringField, SelectField


upload_folder = '/home/kwnafi/PycharmProjects/MudaBlue/upload'
folders = os.listdir(upload_folder)


class WorkForm(Form):
    result = TextAreaField('Result')
    project = StringField('Enter Project Name')
    project_names = SelectField('Select Project', choices=[(x, x) for x in folders])
