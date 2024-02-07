import os
import platform
import blink_led as blink
import gradient_led as gradient
import led_on_off as led_op

from flask import Flask, render_template

PATH_SEP = '\\' if platform.system() == "Windows" else '/'
CAMERA_FOLDER_PATH = os.getcwd() + PATH_SEP + 'camera'

app = Flask(__name__, static_folder=CAMERA_FOLDER_PATH)


class Image:
    def __init__(self, name, url, path):
        self.name = name
        self.url = url
        self.path = path


@app.route("/")
def index():
    dir_list = []
    try:
        for entry in os.scandir(path=CAMERA_FOLDER_PATH):
            if entry.is_dir():
                dir_list.append(entry.name)
    except FileNotFoundError as e:
        print(f"Error occurred: {e}")
    return render_template('index.html', dir_list=dir_list)


@app.route("/led/<op_type>")
def led(op_type: str):
    print(op_type)
    if op_type == "blink":
        blink.run()
    elif op_type == "gradient":
        gradient.run()
    else:
        print("Unsupported operation")
    return render_template('index.html')


@app.route("/led/<pin>/<on_off>")
def led_on_off(pin, on_off):
    try:
        led_nr = int(pin)
        state = int(on_off)
    except ValueError:
        print("Unsupported values in URL path")
        return render_template('index.html')

    led_op.run(led_nr, state)
    return render_template('index.html', pin=pin, state=state)


@app.route("/movement/<folder_name>")
def list_photos(folder_name: str):
    with open(CAMERA_FOLDER_PATH + PATH_SEP + folder_name + PATH_SEP + 'photo_logs.txt', 'r') as f:
        photos = [Image(name=line.rstrip(),
                        url=folder_name + PATH_SEP + line.rstrip(),
                        path=CAMERA_FOLDER_PATH + PATH_SEP + folder_name + PATH_SEP + line.rstrip()
                        )
                  for line in f]
    return render_template('photos.html', photos=photos)


app.run(host="0.0.0.0", port=8080)
