from flask import Flask, render_template, request, flash
import tkFileDialog


upload_folder = '/home/sr-p2irc-big14/Dropbox/CroLSim/toolUpload'
result_folder = '/home/sr-p2irc-big14/Dropbox/CroLSim/templates/interResults'


app = Flask(__name__)
app.config['upload_folder'] = upload_folder
app.secret_key = 'demowork'


directory = "NotSelected"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['button'] == "Search":
            file = request.files['file']
            if file.filename =='':
                flash('No project selected')
                return render_template("index.html", directory=directory)
    return render_template("index.html", directory=directory)


if __name__== '__main__':
    app.debug = True
    app.run()