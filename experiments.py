from algorithm import *
import random

vertex_count = 5
edge_count = int(vertex_count * 1.5)
undirected_count = int(0.5*edge_count)

# draw a random, fully connected graph
is_connected = False
while not is_connected:
    g = Graph.Erdos_Renyi(n=vertex_count, m=edge_count, directed=True, loops=False)
    is_connected = g.is_connected()

# assign random weights to it
weights = [random.randint(1, 10) for _ in range(vertex_count)]
vertex_labels = list(ascii_lowercase[:edge_count])
g.es["weights"] = weights
g.es["label"] = weights
g.vs["label"] = vertex_labels
# plot(g)

# manipulate adjacency matrix
# WARNING: weights sequence is not preserved
full_adjacency_matrix = PartiallyDirectedGraph.transform_adj_mat_to_full(g.get_adjacency())
for _ in range(undirected_count):   # set random edges as undirected
    edge_idx = random.randint(0, edge_count-1)
    full_adjacency_matrix[:, edge_idx] = -1*abs(full_adjacency_matrix[:, edge_idx])
g = PartiallyDirectedGraph(full_adjacency_matrix, weights, vertex_labels)
g.plotGraph()
g1 = G1(g)
# g1.plotGraph()
g1.get_postman_tour(100, 'a')
