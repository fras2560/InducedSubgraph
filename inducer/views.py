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
from inducer.container import induced_subgraph
from pprint import PrettyPrinter
from inducer.helper import convert_to_networkx
from inducer.helper import convert_to_d3
pp = PrettyPrinter(indent=5)
@app.route("/")
def index():
    return render_template('new_finder.html')

@app.route("/contains" , methods=["POST"])
def contains():
    graphs = json.loads(request.data)
    g = convert_to_networkx(graphs['G'])
    h = convert_to_networkx(graphs['H'])
    subgraph = induced_subgraph(g, h)
    if subgraph is None:
        subgraph = {'success': False}
    else:
        subgraph = convert_to_d3(subgraph)
        subgraph['success'] = True
    pp.pprint(graphs['H'])
    pp.pprint(graphs['G'])
    return json.dumps(subgraph)