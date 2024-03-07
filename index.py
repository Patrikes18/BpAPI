# /api/index.py

import pydot
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():

    dot_string = """graph G{
    1--2;
    2--3;
    1--3;
    4--5;
    4--1;
    1[shape=circle,style=wedged,fillcolor="blue;0.1:green;0.1:black;0.1:red;0.1:white:cyan;0.4",label="",xlabel="Hello"];
    2[shape=circle,style=wedged,fillcolor="blue;0.1:green;0.1:black;0.1:red:white;0.4",label="",xlabel="Hello"];
    3[shape=circle,style=wedged,fillcolor="blue;0.1:green;0.1:black;0.1:red:white;0.4",label="",xlabel="Hello"];
    4[shape=circle,style=wedged,fillcolor="blue;0.1:green;0.1:black;0.1:red:white;0.4",label="",xlabel="Hello"];
    5[shape=circle,style=wedged,fillcolor="blue;0.1:green;0.1:black;0.1:red:white;0.4",label="",xlabel="Hello"];
    6[shape=circle,style=wedged,fillcolor="blue;0.1:green;0.1:black;0.1:red:white;0.4",label="",xlabel="Hello"];
}"""

    graphs = pydot.graph_from_dot_data(dot_string)
    graph = graphs[0]

    output_graphviz_svg = graph.create_svg()
    return output_graphviz_svg, 200


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "Not Found"}), 404