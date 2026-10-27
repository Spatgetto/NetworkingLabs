from graphviz import Digraph

my_graph = Digraph(comment = "10-23")

my_graph.node("ext-conn-1")
my_graph.node("SW1")
my_graph.node("SW2")
my_graph.node("R1")
my_graph.node("R2")

my_graph.edge("ext-conn-1", "SW1")
my_graph.edge("SW1", "SW2")
my_graph.edge("SW1", "R1")
my_graph.edge("SW2", "R2")
my_graph.edge("R1", "R2")

print(my_graph.source)

my_graph.render("graph2.gv")