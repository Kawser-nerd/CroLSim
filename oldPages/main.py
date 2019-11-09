from flask import Flask, render_template, request, flash
import pandas as pd
from Tkinter import *
from werkzeug.utils import *
import tkFileDialog
from workstation import WorkForm
from mudablue import *
import numpy
from vector import *
import lda_2_vec_imple


upload_folder = '/home/kwnafi/PycharmProjects/MudaBlue/upload'
result_folder = '/home/kwnafi/PycharmProjects/MudaBlue/Results'


app = Flask(__name__)
app.config['upload_folder'] = upload_folder
app.secret_key = 'practicedocument'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = WorkForm()
    if request.method == 'POST':
        #  File Upload mechanism #
        if request.form['button'] == "Upload":
            if request.form['project'] == '':
                flash('Enter Project Name')
                return render_template("workstation.html", form=form)
            else:
                files = request.files.getlist("file[]")   # Requested files to upload
                project = request.form['project']
                project_folder = os.path.join(upload_folder, project)
                try:
                    os.makedirs(project_folder)
                except OSError:
                    print "Folder is already there"
                for f in files:
                    filename = secure_filename(f.filename)     # Files Upload
                    f.save(os.path.join(project_folder, filename))
                    flash('Upload Done')
                return render_template("workstation.html", form=form)
        elif request.form['button'] == 'MudaJoin':
            root = Tk()
            directory = tkFileDialog.askdirectory()
            root.destroy()
            files = os.listdir(directory)
            with open(os.path.join(directory, 'Source_Join.txt'), 'w') as outfile:   # Open & Write file
                for f in files:
                    if f.endswith('.py'):
                        with open(os.path.join(directory, f), 'r') as f_r:
                            for line in f_r:
                                outfile.write(line)
            flash('Source Code are joined')
            with open(os.path.join(directory, 'Doc_Join.txt'), 'w') as outfile:     # Open & Write file
                for f in files:
                    if f.endswith('.md'):
                        with open(os.path.join(directory, f), 'r') as f_r:
                            for line in f_r:
                                outfile.write(line)
            return render_template("workstation.html", form=form)
        elif request.form['button'] == 'MudaTDM':
            projects = os.listdir(upload_folder)
            name = 'Source_Join.txt'
            for f in projects:
                files = os.listdir(os.path.join(upload_folder, f))
                if name in files:
                    term_document_matrix(os.path.join(upload_folder, f, 'Source_Join.txt'))
            tdm.write_csv(os.path.join(result_folder, 'matrix.csv'), cutoff=1)
            #  Transpose Matrix from Term-Document to Document-Term
            pd.read_csv(os.path.join(result_folder, 'matrix.csv')).T.\
                to_csv(os.path.join(result_folder, 'Read_matrix.csv'), header=False)
            with open(os.path.join(result_folder, 'Read_matrix.csv')) as f_csv:
                form.result.data = f_csv.readlines()
            return render_template("workstation.html", form=form)
        elif request.form['button'] == 'MudaLSA':
            # matrix = csv_file_to_matrix(os.path.join(result_folder, 'matrix.csv'))
            df = pd.read_csv(os.path.join(result_folder, 'matrix.csv'))
            matrix = df.as_matrix()
            matrix_tfidf = tfidfTransform(matrix)
            numpy.savetxt(os.path.join(result_folder, 'TfIDf_matrix.csv'), matrix_tfidf, delimiter=",")
            df = pd.read_csv(os.path.join(result_folder, 'TfIDf_matrix.csv'), header=None)
            matrix = df.as_matrix()
            matrix_lsa = lsa(matrix)
            form.result.data = matrix_lsa
            numpy.savetxt(os.path.join(result_folder, 'LSA_matrix.csv'), matrix_lsa, delimiter=",")
            pd.read_csv(os.path.join(result_folder, 'LSA_matrix.csv')).T. \
                to_csv(os.path.join(result_folder, 'T_LSA_matrix.csv'), header=False)
            return render_template("workstation.html", form=form)
        elif request.form['button'] == 'MudaCosineSimilarity':
            df = pd.read_csv(os.path.join(result_folder, 'LSA_matrix.csv'), header=None)
            matrix = df.as_matrix()
            matrix_cosine = cosine_similar(matrix)
            print(matrix_cosine)
            form.result.data = matrix_cosine
            numpy.savetxt(os.path.join(result_folder, 'Cosine_matrix.csv'), matrix_cosine, delimiter=",")
            return render_template("workstation.html", form=form)
        elif request.form['button'] == 'MudaVectorAnalysis':
            projects = os.listdir(upload_folder)
            name = 'Source_Join.txt'
            for f in projects:
                files = os.listdir(os.path.join(upload_folder, f))
                if name in files:
                    vector_document_mapping(os.path.join(upload_folder, f, 'Source_Join.txt'))
            v = VectorSpaceCreate()
            vectorSpace = v.vector_space_mapping()
            form.result.data = vectorSpace
            cosine_score = cosine_similar(vectorSpace)
            form.result.data = cosine_score
            return render_template("workstation.html", form=form)
        elif request.form['button'] == 'MudaLDA':
            return render_template("workstation.html", form=form)
        elif request.form['button'] == 'Lda2vec':
            return render_template("workstation.html", form=form)

        # CroPSim Implementation with Lda2Vec

        elif request.form['button'] == 'CropSim_data':
            projects = os.listdir(upload_folder)
            name = 'Source_Join.txt'
            count = 1
            for f in projects:
                files = os.listdir(os.path.join(upload_folder, f))
                if name in files:
                    reading = open(os.path.join(upload_folder, f, 'Source_Join.txt'), 'r')
                    text_doc = reading.readlines()
                    lda_2_vec_imple.text_prep(text_doc, count)
                    count += 1
            return render_template("workstation.html", form=form)
    return render_template("workstation.html", form=form)


if __name__ == '__main__':
    app.debug = True
    app.run()
