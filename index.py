"""
    Vstup požiadavkov na API a ich organizácia.
"""
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
cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=['POST'])
@cross_origin()
def home():
    try:
        if request.method == 'POST':
            # Spracovanie a uloženie požiadavku.
            data = request.get_json()
            vertices = VM.VertexModel(data["vertices"])
            edges = []
            for i in data["edges"]:
                edges.append(EM.EdgeModel(i))
            
            # Inicializácia výstupného grafu.
            graph = pydot.Dot("fuzzy_graf", graph_type="graph", bgcolor="transparent")
            independentsets = list()

            if len(edges) > 0: # Graf neobsahuje iba vrcholy.
                independent = IS.IndependentSet(vertices, edges)
                independent.findStrongEdges()
                independent.findIdependentSets()
                independentsets = independent.findAllMaximalSets()
            else: # Graf obsahuje iba vrcholy.
                for vname, vvalue in data["vertices"].items():
                    graph.add_node(pydot.Node(vname, shape="circle",style="filled",fillcolor="green", label="", xlabel=f"({vname}, {vvalue})"))
                output_graphviz_svg = graph.create_svg()
                return output_graphviz_svg, 200
            
            if len(independentsets) == 1 and frozenset() in independentsets: # Graf má iba slabo susediace vrcholy.
                for vname, vvalue in data["vertices"].items():
                    graph.add_node(pydot.Node(vname, shape="circle",style="filled",fillcolor="green", label="", xlabel=f"({vname}, {vvalue})"))

                for edge in data["edges"]:
                    graph.add_edge(pydot.Edge(edge["vertices"][0], edge["vertices"][1], label=f"{edge['value']}", color="black"))
                    
            else: # Graf obsahuje aj silne susediace vrcholy.
                # Inicializácia lineárneho programovania pre prvú fázu.
                linearprog = LP.LinearProgram(independentsets)
                linearprog.createTablePhase1()

                while linearprog.williterate: # Iterovanie v prvej fáze.
                    iter = linearprog.iterate(1)
                    if iter == 1:
                        return jsonify({"status": 422, "message": "Lineárne programovanie nemá riešenie."}), 422

                # Inicializácia lineárneho programovania pre druhú fázu.
                res = linearprog.createTablePhase2()
                if res == 2:
                    return jsonify({"status": 422, "message": "Graf nemá riešenie."}), 422
                
                while linearprog.williterate: # Iterovanie v druhej fáze.
                    iter = linearprog.iterate(2)
                    if iter == 1:
                        return jsonify({"status": 422, "message": "Lineárne programovanie nemá riešenie."}), 422

                # Inicializácia farieb a ich rozdelenie.
                coloring = CLR.Coloring(vertices, edges, independentsets, linearprog)
                coloring.computeWeight()
                colors = coloring.createColorString()

                # Vyfarbovanie grafu.
                for vname, vvalue in data["vertices"].items():
                    if not ";" in colors[vertices.getIndexOf(vname)] or ";1" in colors[vertices.getIndexOf(vname)]: # Vrchol je farbený jednou farbou.
                        graph.add_node(pydot.Node(vname, shape="circle",style="filled",fillcolor=f"{colors[vertices.getIndexOf(vname)]}", label="", xlabel=f"({vname}, {vvalue})"))
                    else: # Vrchol je farbený viacerými farbami.
                        graph.add_node(pydot.Node(vname, shape="circle",style="wedged",fillcolor=f"{colors[vertices.getIndexOf(vname)]}", label="", xlabel=f"({vname}, {vvalue})"))

                for edge in data["edges"]:
                    graph.add_edge(pydot.Edge(edge["vertices"][0], edge["vertices"][1], label=f"{edge['value']}", color="black"))

            output_graphviz_svg = graph.create_svg()
            return output_graphviz_svg, 200
    except:
        return jsonify({"status": 422, "message": "Nastala chyba na serveri."}) , 422


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "Not Found"}), 404