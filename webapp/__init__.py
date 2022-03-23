from flask import Flask


# Initialisze l'application Flask
app = Flask( __name__ )

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

from .context_processors import *
from . import views
from . import models


# Connect sqlalchemy to app
models.db.init_app(app)


@app.cli.command()
def init_db():
    models.init_db()
