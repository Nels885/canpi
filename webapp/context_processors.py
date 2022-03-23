import datetime

from . import app


@app.context_processor
def get_today_date():
    return dict(now=datetime.datetime.now())
