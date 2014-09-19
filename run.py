"""
-------------------------------------------------------
runserver
starts the flask server for d3 G contains H
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-18
-------------------------------------------------------
"""
#!flask/bin/python
from inducer import app
if __name__ == "__main__":
    app.run(debug = True)