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


full_adjacency_matrix_sample = np.array([
    [-1, 0, 1], # A
    [ 1,-1, 0], # B
    [ 0,-1,-1]  # C
])
labels_sample = ["A", "B", "C"]
weights_sample = [1, 2, 10]
# g = PartiallyDirectedGraph(full_adjacency_matrix_sample, labels_sample, weights_sample)
# g.plot()
# g1= G1(g)
# print(g1.have_euler_tour())
# g1.plot()

full_adjacency_matrix_sample1 = np.array([
    [ 1, 0,-1,  0],  # a
    [-1,-1, 0, -1],  # b
    [ 0,-1, 1,  0],  # c
    [ 0, 0, 0,  1]   # d
])
labels_sample = ["a", "b", "c", "d"]
weights_sample = [1, 4, 8, 6]
#g = PartiallyDirectedGraph(full_adjacency_matrix_sample1, labels_sample, weights_sample)
#g.plotGraph()
#g1= G1(g)
# print(g1.have_euler_tour())
#g1.plotGraph()

full_adjacency_matrix_sample2 = np.array([
    [-1, -1, 0, 0],  # a
    [-1, 0, -1, 0],  # b
    [0, -1, -1, 0],  # c
    [0, 0, 0, -1],  # d
    [0, 0, 0, -1]  # e
])
labels_sample = ["a", "b", "c", "d", "e"]
weights_sample = [1, 2, 10, 1]
# g = PartiallyDirectedGraph(full_adjacency_matrix_sample, labels_sample, weights_sample)
# g1= G1(g)
# print(g1.have_euler_tour())
# g1.plot()

# grpah G1 depicted on fig. 7 in documentation
full_adjacency_matrix_sample2 = np.array([
    [1,  1,-1, 0, 0, 0, 0, 0, 0, 0, 0],  # a
    [-1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # b
    [0, -1, 0, 0, 0, 1, 1,-1, 0, 0, 0],  # c
    [0,  0, 0, 0,-1, 0,-1, 0, 1,-1, 0],  # d
    [0,  0, 1,-1, 0,-1, 0, 0,-1, 0, 1],  # e
    [0,  0, 0, 0, 0, 0, 0,-1, 0,-1,-1]  # f
])

# grpah G1 depicted on fig. 7 in documentation
full_adjacency_matrix_sample = np.array([
    [1,  1,-1, 0, 0, 0, 0, 0, 0, 0, 0],  # a
    [-1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # b
    [0, -1, 0, 0, 0, 1, 1,-1, 0, 0, 0],  # c
    [0,  0, 0, 0,-1, 0,-1, 0, 1, 1, 0],  # d
    [0,  0, 1,-1, 0,-1, 0, 0,-1, 0, 1],  # e
    [0,  0, 0, 0, 0, 0, 0, 1, 0,-1,-1]  # f
])
labels_sample = ["a", "b", "c", "d", "e", "f"]
weights_sample = [10, 20, 12, 11, 12, 18, 20, 22, 5, 14, 3]
g = PartiallyDirectedGraph(full_adjacency_matrix_sample, labels_sample, weights_sample)
#g.plotGraph()
g1= G1(g)

#Correction for interpret d-f and c-f as undriected
g1.graph.es[9]["transformed"] = True
g1.graph.es[7]["transformed"] = True
#END Correction
#g1.plotGraph()
deg_list = [] # for storing vertices degrees(our degree = DegIn - degOut)

if not g1.have_euler_tour(deg_list):
    g1.graph.vs["deg"] = deg_list
    g2 = g1.add_penaltyTm_edges(3) #create G2 as mentioned in documentation
    gd, iNeg = g1.create_complete_bipart(deg_list, g2)
    if gd != None:
       ipenCnt =  g1.GraphBalancing(gd, g2)
       print("Number of penalty edges added: {}".format(ipenCnt))
       g1.FindEuler("a")
       #g1.plotGraph() # g1 after balancing
    #gd.plotGraph()
    #g2.plotGraph()
    #print(g1.graph.vs["deg"])
    #verL = g1.graph.vs.select(deg = -1)
    #for vert in verL: print(vert["label"])
    #g.plotGraph()
else:
    print("Graph already has Euler tour")
    g1.FindEuler("a")
print("END!")
