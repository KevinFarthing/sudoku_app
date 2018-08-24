from app import app
from flask import render_template, redirect, url_for, request, session
# from flask.ext.uploads import Upload_Set, configure_uploads, IMAGES
from sudoku_solver import sudoku_solver
from clean_image import clean_image
from tess import img_to_sudoku
import cv2
import os

app.secret_key = b'?o\xe5\xc7\xd7\xd6\xea\xbbb\x94u\x1d\x03\xb8\tk'

easy_base = [[5,3,0,0,7,0,0,0,0],
              [6,0,0,1,9,5,0,0,0],
              [0,9,8,0,0,0,0,6,0],
              [8,0,0,0,6,0,0,0,3],
              [4,0,0,8,0,3,0,0,1],
              [7,0,0,0,2,0,0,0,6],
              [0,6,0,0,0,0,2,8,0],
              [0,0,0,4,1,9,0,0,5],
              [0,0,0,0,8,0,0,7,9]]

base_puzzle =[[0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0]] 

@app.route('/')
@app.route('/index')
def index():
    if 'sudoku' in session:
        return render_template('index.html', sudoku=session['sudoku'])
    return render_template('index.html', sudoku = easy_base)

@app.route('/', methods=["POST"])
@app.route('/index', methods=["POST"])
def index_post():
    load = request.form
    puzzle = []
    for i in range(9):
        row = []
        for j in range(9):
            c = load[f'row{i}col{j}']
            if c == '':
                row.append(0)
            else:
                row.append(int(c))
        puzzle.append(row)
    session['sudoku']=sudoku_solver(puzzle)
    # return render_template('index.html', sudoku = base_puzzle)
    # return render_template('index.html', sudoku=sudoku_solver(puzzle))
    return redirect(url_for('index'))
    # okay, if user changes input table, the change is NOT reflected when the solve function is called.
    # check that user inputs are handled by requests the same way as the values tag


# photos = Upload_Set('photos', IMAGES)
# app.config['UPLOADED_PHOTOS_DEST'] = 'static/images' #switch to os.join?
# configure_uploads(apps, photos)

UPLOAD_FOLDER = '/temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'temp')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=["GET", "POST"])
def upload():
    file = request.files['image']
    filename = file.filename
    # file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(full_filename)
    file.save(full_filename)
    # plus the add file stuff
    # redirect(url_for("index", sudoku=sudoku_shit))

    img = cv2.imread(full_filename,0)

    clean_image(img)
    session['sudoku'] = img_to_sudoku()

    # return render_template('index.html', sudoku = extracted)
    return redirect(url_for('index'))