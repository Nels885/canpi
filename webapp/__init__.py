from flask import Flask


# Initialisze l'application Flask
app = Flask( __name__ )


from . import views
