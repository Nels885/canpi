import logging as lg

from flask_sqlalchemy import SQLAlchemy
from . import app


db = SQLAlchemy(app)


class Fmux(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(200), nullable=False)
    product = db.Column(db.String(200), nullable=False)
    arbitration_id = db.Column(db.Integer(), nullable=False)
    data = db.Column(db.String(200), nullable=False)

    # def __init__(self, name, brand, product, arbitration_id, data):
    #     self.name = name
    #     self.brand = brand
    #     self.product = product
    #     self.arbitration_id = arbitration_id
    #     self.data = data


def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    lg.warning('Database initialized!')