import subprocess

from flask import Flask, render_template, redirect, jsonify
from . import app


@app.route('/')
def hello_world():
    title = "Home"
    return render_template('index.html', **locals())


@app.route('/stop/')
def stop():
    # subprocess.call("sudo shutdown -h now", shell=True)
    return jsonify(status="stop")


@app.route('/restart/')
def restart():
    # subprocess.call("sudo reboot", shell=True)
    return jsonify(status="reboot")
