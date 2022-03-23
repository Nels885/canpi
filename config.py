import os

# To generate a new secret key:
# >>> import random, string
# >>> "".join([random.choice(string.printable) for _ in range(32)])
SECRET_KEY = 'e|r!qqw0wo!Jf-:phn#JQ\x0c(Q9xJI&ZW_'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False
