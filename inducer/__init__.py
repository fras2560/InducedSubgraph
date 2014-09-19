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
from flask import Flask, g , request

# create the application
app = Flask(__name__)
app.config.from_object("config")
#load default config
app.config.update(dict(
                       DEBUG=True,
                       SECRET_KEY="development key",
                       USERNAME="admin",
                       PASSWORD="default"))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

from inducer import views

if __name__ == '__main__':
    app.run()