from flask import Flask, render_template, request
from Tkinter import *
import tkFileDialog
import os
from API_Extraction import API_Extraction, Comment_Extraction, ReadMe_Extraction

app = Flask(__name__)
app.secret_key = 'practicedocument'


directory = "select directory"


@app.route('/', methods=['GET', 'POST'])
def index():
    global directory
    if request.method == 'POST':
        if request.form['button'] == 'browse':
            root = Tk()
            directory = tkFileDialog.askdirectory()
            root.destroy()
            return render_template("FrontEnd.html", dir=directory)
        elif request.form['button'] == 'start':
            listofprojects = os.listdir(directory)
            for project in listofprojects:
                if os.path.isdir(os.path.join(directory, project)):
                    ReadMe_Extraction(project, directory)
                    for path, subdirs, files in os.walk(os.path.join(directory, project)):
                        for f in files:
                            if f.endswith('.py'):
                                projectPath = os.path.join(path, f)
                                API_Extraction(project, projectPath, directory)
                                Comment_Extraction(project, projectPath, directory)
            return render_template("FrontEnd.html", dir=directory)
    return render_template("FrontEnd.html", dir=directory)


if __name__ == "__main__":
    app.run()

