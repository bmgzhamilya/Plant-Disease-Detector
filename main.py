from flask import Flask,request,render_template,redirect
from werkzeug.utils import secure_filename
from NN.NN import get_image_disease
import os
import glob
app = Flask(__name__)


app.config["IMAGE_UPLOADS"] = "D:/site/static/Images"
#app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG","JPG","JPEG"]



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

		disease, description = get_image_disease(filename)

		return render_template("main.html",filename=filename, disease=disease, description = description)

	return render_template('main.html')

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static',filename = "/Images" + filename), code=301)


app.run(debug=True,port=2000)