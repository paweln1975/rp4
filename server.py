from flask import Flask, render_template
import blink_led as blink
import gradient_led as gradient
import led_on_off as led_op

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


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


app.run(host="0.0.0.0", port=8080)
