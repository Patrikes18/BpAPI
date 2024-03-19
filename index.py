# /api/index.py
#flask --app index.py run

import pydot
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request
import LPP

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=['POST'])
@cross_origin()
def home():
    if request.method == 'POST':

        data = request.get_json()
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

        print(data["vertices"])
        # output_graphviz_svg = pydot.graph_from_dot_data(dot_string)
        # graph = output_graphviz_svg[0]
        output_graphviz_svg = graph.create_svg()
        return output_graphviz_svg, 200


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "Not Found"}), 404