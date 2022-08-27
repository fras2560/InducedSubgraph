"""
-------------------------------------------------------
inducer
a flask app using d3 and networkx to helper find induced
subgraphs
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-11
-------------------------------------------------------
"""
from flask import Flask
import logging
# create the application
app = Flask(__name__)
app.config.from_object("config")
# load default config
app.config.update(dict(
    SECRET_KEY="development key",
    USERNAME="admin",
    PASSWORD="default"))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['UPLOAD_FOLDER'] = 'uploads'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

from inducer import views

if __name__ == '__main__':
    app.run()
