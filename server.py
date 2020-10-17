import os
from argparse import ArgumentParser
import random

from flask import Flask, request, redirect, jsonify
from flask_cors import CORS

from werkzeug.utils import secure_filename

import pandas as pd
from fbprophet import Prophet

import logging
logging.getLogger('flask_cors').level = logging.DEBUG
logging.getLogger('fbprophet').setLevel(logging.ERROR)

import warnings
warnings.filterwarnings("ignore")

ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

DAYS_PARAM = 7    # default value for days hyper-param


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/v1/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        # flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    print(file.filename)
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['DATA_FOLDER'], filename))
        return jsonify('uploaded successfully!')

    return '''
    '''


@app.route("/api/v1/predict")
def predict():
    filename = request.args.get('filename')
    days_param = int(request.args.get('days')) if int(request.args.get('days')) else DAYS_PARAM
    df = pd.read_csv(app.config['DATA_FOLDER'] + '/' + filename)
    data = df.head(5).to_json()
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=days_param)
    forecast = m.predict(future)
    data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail().to_json()
    fig = m.plot(forecast)
    fig_fn = str(random.getrandbits(128)) + '.png'
    fig.savefig(os.path.join(app.config['MODEL_FOLDER'], fig_fn))
    data = {'url': 'figs/' + fig_fn}
    return jsonify(data)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-d", "--data", dest="DATA_FOLDER",
        help="specify the directory for uploading users data", required=True)
    parser.add_argument("-o", "--output", dest="MODEL_FOLDER",
        help="specify the directory for uploading forecat images", required=True)    
    args = parser.parse_args()
    app.config['DATA_FOLDER'] = args.DATA_FOLDER
    app.config['MODEL_FOLDER'] = args.MODEL_FOLDER
    app.run(host="0.0.0.0", port=5001, threaded=True, debug=True)	#set debug flag to False