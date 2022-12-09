from flask import Flask,request,render_template,redirect
from werkzeug.utils import secure_filename
from NN import get_image_disease
import os
import glob
app = Flask(__name__)


app.config["IMAGE_UPLOADS"] = "/opt/Plant-Disease-Detector/static/Images"
#app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG","JPG","JPEG"]

@app.route("/")
def index():
            return "<h1>Hello!</h1>"

@app.route('/home',methods = ["GET","POST"])
def upload_image():
	if request.method == "POST":
		image = request.files['file']

		if image.filename == '':
			print("Image must have a file name")
			return redirect(request.url)

		basedir = os.path.abspath(os.path.dirname(__file__))

		files = glob.glob(app.config["IMAGE_UPLOADS"] + '/*')
		print(files)
		for f in files:
			os.remove(f)

		filename = secure_filename(image.filename)
		image.save(os.path.join(basedir,app.config["IMAGE_UPLOADS"],filename))

		disease = get_image_disease(filename)

		return render_template("main.html",filename=filename, disease=disease)

	return render_template('main.html')

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static',filename = "/Images" + filename), code=301)

if __name__ == "__main__":
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)
