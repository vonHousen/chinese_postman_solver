from igraph import *


class PartiallyDirectedGraph:
    """
    Adapter for graph object from igraph library. Represents partially directed graph.
    """

    def __init__(self, full_adjacency_matrix: list, labels: list, weights: list):
        self.graph = self.get_graph_from_full_adj_mat(full_adjacency_matrix)
        self.graph.vs["label"] = labels
        self.graph.es["weight"] = weights

    @staticmethod
    def get_graph_from_full_adj_mat(full_adjacency_matrix: list):
        """
        Gets directed graph based on given full adjacency matrix.
        Due to igraph limitations, representation of partially directed graph is in object of
        directed graph, but edges are flagged if these are directed or not.
        :param full_adjacency_matrix: (list of lists) full adjacency matrix
        :return: Directed graph with edges flagged if these are directed or not.
        """
        # safety check
        if full_adjacency_matrix is None \
                or len(full_adjacency_matrix) == 0\
                or len(full_adjacency_matrix[0]) == 0:
            return None

        # prepare graph g, at first without edges
        g = Graph(directed=True)
        vertex_count = len(full_adjacency_matrix)
        edge_count = len(full_adjacency_matrix[0])
        g.add_vertices(vertex_count)
        edges = []
        directed_flags = []

        # iterate through the matrix & add edges to the graph
        end_flag = 'e'
        start_flag = 's'
        # for every edge...
        for edge_idx in range(edge_count):

            new_edge = []
            # find vertices incident to the edge
            for vertex_idx in range(vertex_count):
                edge_flag = full_adjacency_matrix[vertex_idx][edge_idx]
                if edge_flag == -1:
                    new_edge.append((vertex_idx, end_flag))
                elif edge_flag == 1:
                    new_edge.append((vertex_idx, start_flag))
                else:
                    continue
                # check if new_edge already consists of 2 vertices
                if len(new_edge) == 2:
                    break

            # having obtained new edge, decide if it is directed or undirected
            if new_edge[0][1] == start_flag and new_edge[1][1] == end_flag:
                edges.append((new_edge[0][0], new_edge[1][0]))
                directed_flags.append(True)
            elif new_edge[0][1] == end_flag and new_edge[1][1] == start_flag:
                edges.append((new_edge[1][0], new_edge[0][0]))
                directed_flags.append(True)
            elif new_edge[0][1] == end_flag and new_edge[1][1] == end_flag:
                edges.append((new_edge[0][0], new_edge[1][0]))
                directed_flags.append(False)
            else:
                raise RuntimeError("Incorrect structure of full_adjacency_matrix!")

        g.add_edges(edges)
        g.es['directed'] = directed_flags
        return g


def is_connected(adjacency_matrix: list):
    return Graph.Adjacency(adjacency_matrix).is_connected()


def transform_g_to_g1(adjacency_matrix: list):
    return Graph.Adjacency(adjacency_matrix)
