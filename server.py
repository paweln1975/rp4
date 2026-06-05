import os
from flask import Flask, render_template, send_from_directory


CAMERA_FOLDER_PATH = '/home/pi/Pictures'

app = Flask(__name__, static_folder=CAMERA_FOLDER_PATH)


@app.route("/")
def index():
    return send_from_directory(CAMERA_FOLDER_PATH, 'index.html', mimetype='text/html')


@app.route("/<path:filename>")
def serve_file(filename):
    return send_from_directory(CAMERA_FOLDER_PATH, filename)


app.run(host="0.0.0.0", port=8080)
