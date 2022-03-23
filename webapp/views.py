import subprocess

from flask import Flask, render_template, redirect, jsonify, request
from . import app

from .models import db, Fmux
from .forms import FmuxForm


@app.route('/')
def hello_world():
    title = "Home"
    return render_template('index.html', **locals())


@app.route('/stop/')
def stop():
    subprocess.call("sudo shutdown -h now", shell=True)
    return jsonify(status="stop")


@app.route('/restart/')
def restart():
    subprocess.call("sudo reboot", shell=True)
    return jsonify(status="reboot")


@app.route("/create/", methods=["GET", "POST"])
def create_fmux():
    title = "Create FMUX"
    fmux = Fmux()
    success = False

    if request.method == "POST":
        form = FmuxForm(request.form, obj=fmux)
        if form.validate():
            form.populate_obj(fmux)
            db.session.add(fmux)
            db.session.commit()
            success = True
    else:
        form = FmuxForm(obj=fmux)

    return render_template("create.html", **locals())