"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.

"""
from flask import Flask

app = Flask(__name__)
UPLOAD_FOLDER = r'tmp/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
STATIC_FOLDER = r'static'
app.config['STATIC_FOLDER'] = STATIC_FOLDER

# routes.py after app is created, circular references
from routes import *
from globes import *
global_init()

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# launch server
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    local_only = True
    if local_only:
        app.run(HOST, PORT)
    else:
        accept_remote_host = "0.0.0.0"
        app.run(accept_remote_host, PORT)

