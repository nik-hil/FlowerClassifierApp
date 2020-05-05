
import os
import base64
from io import BytesIO
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {  'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from fastai2.vision.all import *
from fastai2.vision.widgets import *
fname= "./export.pkl"
learn_inf = load_learner(fname, cpu=True)

TEMPLATE = '''
    <!doctype html>
    <title>FLower Classifier</title>
    <h1>Classify Flower images</h1>
    <p>
    Do you need to identify the flower. Just upload it.
    And this will classify the flower image. 
    This only handles chamomile, tulip, rose, sunflower, dandelion flowers</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img = PILImage.create( UPLOAD_FOLDER + '/' + filename)
            
            # import pdb; pdb.set_trace()
            pred,pred_idx,probs  = learn_inf.predict(img)
            value = f'Prediction: {pred}; Probability: {probs[pred_idx]:.04f}'
            himg = img.to_thumb(128,128)
            buffered = BytesIO()
            himg.save(buffered, format="JPEG")
            buffered.seek(0)
            img_str = base64.b64encode(buffered.read()).decode('ascii')

            return TEMPLATE + f'''
                <br>
                <img src="data:image/png;base64,{img_str}">
                <pre>{value}</pre>
                </form>
                '''
    return TEMPLATE



if __name__ == "__main__":
    #app.run("0.0.0.0", port=80)
    app.run(debug=True, host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
