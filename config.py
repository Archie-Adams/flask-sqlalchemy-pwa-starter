import os

# Cross-site request forgery protection ---------------------------------------
WTF_CSRF_ENABLED = True
SECRET_KEY = 'here-you-need-a-very-very-secret-key'

# Database config -------------------------------------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
