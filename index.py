# /api/index.py
#flask --app index.py run

import pydot
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request
import VertexModel as VM
import EdgeModel as EM
import Independent as IS
import LPP as LP
import Coloring as CLR

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=['POST'])
@cross_origin()
def home():
    if request.method == 'POST':

        data = request.get_json()
        data = {'vertices': {'a': 0.4, 'b': 0.5, 'c': 0.8, 'd': 0.3, 'e': 0.7, 'f': 0.5, 'g': 0.8}, 'edges': [{'vertices': ['a', 'b'], 'value': 0.3}, {'vertices': ['a', 'f'], 'value': 0.3}, {'vertices': ['a', 'g'], 'value': 0.15}, {'vertices': ['b', 'c'], 'value': 0.3}, {'vertices': ['b', 'd'], 'value': 0.3}, {'vertices': ['e', 'd'], 'value': 0.25}, {'vertices': ['e', 'f'], 'value': 0.3}, {'vertices': ['b', 'g'], 'value': 0.2}, {'vertices': ['d', 'g'], 'value': 0.1}, {'vertices': ['e', 'g'], 'value': 0.3}]}
        vertices = VM.VertexModel(data["vertices"])
        edges = []
        for i in data["edges"]:
            edges.append(EM.EdgeModel(i))
        
        independent = IS.IndependentSet(vertices, edges)
        independent.findStrongEdges()
        independent.findIdependentSets()
        independentsets = independent.findAllMaximalSets()

        linearprog = LP.LinearProgram(independentsets)
        linearprog.createTablePhase1()
        while linearprog.williterate:
            linearprog.iterate(1)
        res = linearprog.createTablePhase2()
        if res == "no solution":
            return jsonify({"status": 422, "message": "Graph have no solution for coloring"}), 422 #422: “Unprocessable Entity.” The client request contains semantic errors, and the server can’t process it.
        while linearprog.williterate:
            linearprog.iterate(2)

        coloring = CLR.Coloring(vertices, edges, independentsets, linearprog)
        coloring.computeWeight()
        colors = coloring.createColorString()

        graph = pydot.Dot("my_graph", graph_type="graph", bgcolor="transparent")

        for vname, vvalue in data["vertices"].items():
            if ";" in colors[vertices.getIndexOf(vname)]:
                graph.add_node(pydot.Node(vname, shape="circle",style="wedged",fillcolor=f"{colors[vertices.getIndexOf(vname)]}", label="", xlabel=f"({vname}, {vvalue})"))
            else:
                graph.add_node(pydot.Node(vname, shape="circle",style="filled",fillcolor=f"{colors[vertices.getIndexOf(vname)]}", label="", xlabel=f"({vname}, {vvalue})"))

        for edge in data["edges"]:
            graph.add_edge(pydot.Edge(edge["vertices"][0], edge["vertices"][1], label=f"{edge["value"]}", color="blue"))

        output_graphviz_svg = graph.create_svg()
        return output_graphviz_svg, 200


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "Not Found"}), 404