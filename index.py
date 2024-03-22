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
        print(independent.findAllMaximalSets())

        graph = pydot.Dot("my_graph", graph_type="graph", bgcolor="transparent", splines="line")

        for vname, vvalue in data["vertices"].items():
            graph.add_node(pydot.Node(vname, shape="circle", label="", xlabel=f"({vname}, {vvalue})"))

        for edge in data["edges"]:
            graph.add_edge(pydot.Edge(edge["vertices"][0], edge["vertices"][1], label=f"{edge["value"]}", color="blue"))
            
        # Add nodes
        # my_node = pydot.Node("a", label="Foo")
        # graph.add_node(my_node)
        # Or, without using an intermediate variable:
        # graph.add_node(pydot.Node("b", shape="circle"))

        # Add edges
        # my_edge = pydot.Edge("a", "b", color="blue")
        # graph.add_edge(my_edge)
        # Or, without using an intermediate variable:
        # graph.add_edge(pydot.Edge("b", "c", color="blue"))
    #     dot_string = """graph G{
    #     bgcolor="transparent"
    #     1--2;
    #     2--3;
    #     1--3;
    #     4--5;
    #     4--1;
    #     1[shape=circle,style=wedged,fillcolor="blue;0.1:green;0.1:black;0.1:red;0.1:white:cyan;0.4",label="",xlabel="Hello"];
    #     2[shape=circle,style=wedged,fillcolor="blue;0.1:green;0.1:black;0.1:red:white;0.4",label="",xlabel="Hello"];
    #     3[shape=circle,style=wedged,fillcolor="blue;0.1:green;0.1:black;0.1:red:white;0.4",label="",xlabel="Hello"];
    #     4[shape=circle,style=wedged,fillcolor="blue;0.1:green;0.1:black;0.1:red:white;0.4",label="",xlabel="Hello"];
    #     5[shape=circle,style=wedged,fillcolor="blue;0.1:green;0.1:black;0.1:red:white;0.4",label="",xlabel="Hello"];
    #     6[shape=circle,style=wedged,fillcolor="blue;0.1:green;0.1:black;0.1:red:white;0.4",label="",xlabel="Hello"];
    # }"""

        # print(data)
        # output_graphviz_svg = pydot.graph_from_dot_data(dot_string)
        # graph = output_graphviz_svg[0]
        output_graphviz_svg = graph.create_svg()
        return output_graphviz_svg, 200


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "Not Found"}), 404