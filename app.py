from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
import os


app = Flask(__name__)
Bootstrap(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


current_image_index = 0
images = []

from flask import send_from_directory

@app.route('/download_log')
def download_log():
    # Assuming log.txt is in the same directory as your app.py
    return send_from_directory(directory='.', path='log.txt', as_attachment=True)


@app.route('/next_image', methods=['POST'])
def next_image():
    global current_image_index
    current_image_index = (current_image_index + 1) % len(images)
    return jsonify({"image": images[current_image_index]})

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')

@app.route('/previous_image', methods=['POST'])
def previous_image():
    global current_image_index
    current_image_index = (current_image_index - 1) % len(images)
    return jsonify({"image": images[current_image_index]})

@app.route('/record_click/<int:x>/<int:y>', methods=['POST'])
def record_click(x, y):
    return jsonify({"x": x, "y": y})



@app.route('/log_clicks', methods=['POST'])
def log_clicks():
    data = request.json
    with open('log.txt', 'a') as f:
        f.write(data['log'] + '\n')
    return jsonify({"status": "success"})

images_uploaded = False


if __name__ == "__main__":
    app.run(debug=True)
