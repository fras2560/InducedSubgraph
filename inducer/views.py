"""
-------------------------------------------------------
views
holds all the views
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-18
-------------------------------------------------------
"""
from flask import render_template
from inducer import app
from flask import json, request
from inducer.container import contains
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=5)
@app.route("/")
def index():
    return render_template('new_finder.html')

@app.route("/contains" , methods=["POST"])
def contains():
    pp.pprint(request.data)
    return json.dumps(True)