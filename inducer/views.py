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
from flask import render_template, json, request
from inducer import app
from inducer.container import induced_subgraph
from pprint import PrettyPrinter
from inducer.helper import convert_to_networkx, convert_to_d3, text_to_d3
import sys
pp = PrettyPrinter(indent=5)
ALLOWED_EXTENSIONS = set(['txt'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template('new_finder.html')

@app.route("/contains" , methods=["POST"])
def contains():
    print(request.data)
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
    print("Done")
    return json.dumps(subgraph)

@app.route("/loadGraph", methods=["POST"])
def load_graph():
    file = request.files['file']
    result = {'graph': None, 'success':False}
    if file and allowed_file(file.filename):
        content = (file.read()).decode("UTF-8")
        print(content)
        lines = content.replace("\r", "")
        lines = lines.split("\n")
        print(lines)
        result['graph'] = text_to_d3(lines)
        if result['graph'] is not None:
            result['success'] = True
        return json.dumps(result)
