import pydot

dot_string = """graph my_graph {
    bgcolor="yellow";
    a [label="Foo"];
    b [shape=circle];
    a -- b -- c [color=blue];
}"""

graphs = pydot.graph_from_dot_data(dot_string)
graph = graphs[0]

output_graphviz_svg = graph.create_svg()
print(output_graphviz_svg)