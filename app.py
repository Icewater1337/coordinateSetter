from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
Bootstrap(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

current_image_index = 0
images = []

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
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        handle_uploaded_files(uploaded_files)
        return redirect(url_for('index'))

    return render_template('index.html', image=images[current_image_index] if images else None)


@app.route('/previous_image', methods=['POST'])
def previous_image():
    global current_image_index
    current_image_index = (current_image_index - 1) % len(images)
    return jsonify({"image": images[current_image_index]})

@app.route('/record_click/<int:x>/<int:y>', methods=['POST'])
def record_click(x, y):
    return jsonify({"x": x, "y": y})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/log_clicks', methods=['POST'])
def log_clicks():
    data = request.json
    with open('log.txt', 'a') as f:
        f.write(data['log'] + '\n')
    return jsonify({"status": "success"})


def handle_uploaded_files(uploaded_files):
    global images, current_image_index

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filenames = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            filenames.append(filepath.replace("\\", "/"))

    images = filenames
    current_image_index = 0


if __name__ == "__main__":
    app.run(debug=True)
