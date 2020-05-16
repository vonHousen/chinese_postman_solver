from igraph import *
from algorithm import *

# g = Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
#
# g.vs["name"] = ["Alice", "Bob", "Claire", "Dennis", "Esther", "Frank", "George"]
# g.vs["age"] = [25, 31, 18, 47, 22, 23, 50]
# g.vs["gender"] = ["f", "m", "f", "m", "f", "m", "m"]
# g.es["is_formal"] = [False, False, True, True, True, False, True, False, False]
#
# layout = g.layout("kk")
# color_dict = {"m": "blue", "f": "pink"}
# visual_style = {}
# visual_style["vertex_size"] = 20
# visual_style["vertex_color"] = [color_dict[gender] for gender in g.vs["gender"]]
# visual_style["vertex_label"] = g.vs["name"]
# visual_style["edge_width"] = [1 + 2 * int(is_formal) for is_formal in g.es["is_formal"]]
# visual_style["layout"] = layout
# visual_style["bbox"] = (300, 300)
# visual_style["margin"] = 20
# plot(g, **visual_style)

# g = Graph([(0, 1), (0, 2), (2, 1), (3, 4)])
# g.vs["name"] = ["a", "b", "c", "d", "e"]
# visual_style = {}
# visual_style["layout"] = g.layout("kk")
# visual_style["bbox"] = (300, 300)
# visual_style["margin"] = 20
# visual_style["vertex_label"] = g.vs["name"]
# visual_style["vertex_color"] = ["green"] * len(g.vs["name"])
# #plot(g, **visual_style)
# g.get_adjacency()


full_adjacency_matrix_sample = [
    [-1, 0, 1], # A
    [ 1,-1, 0], # B
    [ 0,-1,-1]  # C
]
labels_sample = ["A", "B", "C"]
weights_sample = [1, 2, 10]
full_adjacency_matrix_sample = [
    [-1, -1, 0, 0],  # a
    [-1, 0, -1, 0],  # b
    [0, -1, -1, 0],  # c
    [0, 0, 0, -1],  # d
    [0, 0, 0, -1]  # e
]
labels_sample = ["a", "b", "c", "d", "e"]
weights_sample = [1, 2, 10, 1]

g = PartiallyDirectedGraph(full_adjacency_matrix_sample, labels_sample, weights_sample)
g.plot()