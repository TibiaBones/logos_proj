import os
from datetime import datetime
import base64
from tabnanny import check
from click import DateTime
from flask import Flask, flash, render_template, request, escape
from werkzeug.utils import secure_filename
from DBcm import UseDatabase


UPLOAD_FOLDER = 'static/images'


app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': '4pu_user',
                          'password': '4pu_passwd',
                          'database': 'sportlogodb', }


@app.route('/')
@app.route('/index')
def entry_page() -> 'html':    
    return render_template('index.html')    


if __name__ == '__main__':
    app.run(debug=True)