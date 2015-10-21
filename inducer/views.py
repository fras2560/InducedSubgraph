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
from flask import render_template, json, request, make_response
from inducer import app, logger
from inducer.container import induced_subgraph, k_vertex
from pprint import PrettyPrinter
from inducer.helper import convert_to_networkx, convert_to_d3, text_to_d3
from inducer.helper import complement, join, d3_to_text
from inducer.dcolor import Dcolor 
from inducer.colorable import coloring
from inducer.EvenHoleFree import even_hole_free
from os.path import join as filepath
from os import getcwd
from inducer.clique_cutset import clique_cutset

pp = PrettyPrinter(indent=5)
ALLOWED_EXTENSIONS = set(['txt'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template('new_finder.html')


@app.route("/clique_cutset", methods=["POST"])
def cutset():
    graph = json.loads(request.data)
    g = convert_to_networkx(graph)
    subgraph = clique_cutset(g)
    if subgraph is None:
        subgraph = {'success': False}
    else:
        subgraph = convert_to_d3(subgraph)
        subgraph['success'] = True
    return json.dumps(subgraph)

@app.route("/evenholefree", methods=["POST"])
def ehf():
    graph = json.loads(request.data)
    g = convert_to_networkx(graph['G'])
    subgraph = even_hole_free(g)
    if subgraph is None:
        subgraph = {'success': False}
    else:
        subgraph = convert_to_d3(subgraph)
        subgraph['success'] = True
    return json.dumps(subgraph)

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

@app.route("/complement", methods=["POST"])
def complement_graph():
    graph = json.loads(request.data)
    g = convert_to_networkx(graph)
    co_g = complement(g)
    co_g = convert_to_d3(co_g)
    return json.dumps(co_g)

@app.route("/k_vertex", methods=["POST"])
def k():
    graphs = json.loads(request.data)
    g = convert_to_networkx(graphs['G'])
    subgraphs = []
    for subgraph in graphs['subgraphs']:
        subgraphs.append(convert_to_networkx(subgraph))
    k_vertexes = k_vertex(g, subgraphs)
    return json.dumps(k_vertexes)

@app.route("/join", methods=["POST"])
def join_graphs():
    graphs = json.loads(request.data)
    g = convert_to_networkx(graphs["G"])
    h = convert_to_networkx(graphs["H"])
    f = join(g, h)
    f = convert_to_d3(f)
    return json.dumps(f)

@app.route("/save_file", methods=["POST"])
def save_graph():
    graph = json.loads(request.data)
    graph = d3_to_text(graph)
    fp = filepath(getcwd(), app.config['UPLOAD_FOLDER'], "graph.txt")
    print(fp)
    with open(fp, 'w') as f:
        for line in graph:
            f.write(line + "\n")
            print(line)
    return json.dumps("graph.txt")

@app.route("/<file_name>")
def getFile(file_name):
    fp = filepath(getcwd(), app.config['UPLOAD_FOLDER'],file_name)
    result = ""
    with open (fp, "r") as f:
        for line in f:
            result += line
    print(result)
    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=outbound.txt"
    return response

@app.route("/coloring", methods=["POST"])
def find_coloring():
    print(request.data)
    graph = json.loads(request.data)
    graph = convert_to_networkx(graph)
    colored = coloring(graph, logger=logger)
    return json.dumps(colored) 

@app.route("/dcoloring", methods=["POST"])
def find_dcoloring():
    print(request.data)
    graph = json.loads(request.data)
    graph = convert_to_networkx(graph)
    colored = Dcolor(graph).color()
    return json.dumps(colored)