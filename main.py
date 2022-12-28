from flask import Flask,request,render_template,redirect
from werkzeug.utils import secure_filename
from config import *
from NN.NN import *
from NN.NN_info import *
import os
import glob
app = Flask(__name__)


app.config["IMAGE_UPLOADS"] = path_to_directory + "static/Images/Uploads"
app.config["VIDEO_UPLOADS"] = path_to_directory + "static/Videos"
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

		if ".JPG" in image.filename.upper() or ".PNG" in image.filename.upper():
			print('log: this is image')
			basedir = os.path.abspath(os.path.dirname(__file__))

			files = glob.glob(app.config["IMAGE_UPLOADS"] + '/*')
			print(files)
			for f in files:
				os.remove(f)

			filename = secure_filename(image.filename)
			image.save(os.path.join(basedir,app.config["IMAGE_UPLOADS"],filename))

			response = get_image_disease(filename)

			return render_template("main.html",filename=filename, response=response)
		elif ".MOV" in image.filename.upper() or ".MP4" in image.filename.upper():
			print('log: this is video')
			basedir = os.path.abspath(os.path.dirname(__file__))
			
			files = glob.glob(app.config["IMAGE_UPLOADS"] + '/*')
   
			for f in files:
				os.remove(f)

			files = glob.glob(app.config["VIDEO_UPLOADS"] + '/*')
   
			for f in files:
				os.remove(f)

			filename = secure_filename(image.filename)
			image.save(os.path.join(basedir,app.config["VIDEO_UPLOADS"],filename))

			response = get_video_disease(filename)

			return render_template("main.html",filename=filename, response=response)
		return

	return render_template('main.html')

if __name__ == "__main__":
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)
