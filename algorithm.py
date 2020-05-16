from igraph import *
import numpy as np


class GenericGraph:
    """
    Generic class for graphs.
    """
    def __init__(self, graph: Graph):
        self.graph = graph

    def is_connected(self):
        return self.graph.is_connected()

    def plot(self, edge_label="directed", margin=100, bbox=(500, 500)):
        visual_style = {}
        visual_style["layout"] = self.graph.layout("kk")
        visual_style["bbox"] = bbox
        visual_style["margin"] = margin
        visual_style["vertex_label"] = self.graph.vs["label"]
        visual_style["edge_label"] = [edge_label if flag is True else ""
                                      for flag in self.graph.es[edge_label]]
        plot(self.graph, **visual_style)


class PartiallyDirectedGraph(GenericGraph):
    """
    Adapter for graph object from igraph library.
    Represents partially directed graph. Marked as graph of type G in the documentation.
    """
    def __init__(self, full_adjacency_matrix: np.ndarray, labels: list, weights: list):
        super(PartiallyDirectedGraph, self).__init__(self.get_graph_from_full_adj_mat(full_adjacency_matrix))
        self.graph.vs["label"] = labels
        self.graph.es["weight"] = weights

    @staticmethod
    def get_graph_from_full_adj_mat(full_adjacency_matrix: np.ndarray):
        """
        Gets directed graph based on given full adjacency matrix.
        Due to igraph limitations, representation of partially directed graph is in object of
        directed graph, but edges are flagged if these are directed or not.
        :param full_adjacency_matrix: (list of lists) full adjacency matrix
        :return: Directed graph with edges flagged if these are directed or not.
        """
        # safety check
        if full_adjacency_matrix.ndim != 2:
            return None

        # prepare graph g, at first without edges
        g = Graph(directed=True)
        vertex_count = full_adjacency_matrix.shape[0]
        edge_count = full_adjacency_matrix.shape[1]
        g.add_vertices(vertex_count)
        edges = np.empty((edge_count, 2), dtype=int)
        directed_flags = np.empty((edge_count, 1), dtype=bool)

        # iterate through the matrix & add edges to the graph
        end_flag = 'e'
        start_flag = 's'
        # for every edge...
        for edge_idx in range(edge_count):

            new_edge = []   # data structure for edge; consists of 2 tuples: (vertex id , end/start flag)
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
                edge_to_add = (new_edge[0][0], new_edge[1][0])
                directed_flags[edge_idx] = True
            elif new_edge[0][1] == end_flag and new_edge[1][1] == start_flag:
                edge_to_add = (new_edge[1][0], new_edge[0][0])
                directed_flags[edge_idx] = True
            elif new_edge[0][1] == end_flag and new_edge[1][1] == end_flag:
                edge_to_add = (new_edge[0][0], new_edge[1][0])
                directed_flags[edge_idx] = False
            else:
                raise RuntimeError("Incorrect structure of full_adjacency_matrix!")
            edges[edge_idx][0] = edge_to_add[0]
            edges[edge_idx][1] = edge_to_add[1]

        g.add_edges(list(map(tuple, edges)))
        g.es['directed'] = directed_flags.tolist()
        return g


class G1(GenericGraph):
    """
    Adapter for graph object from igraph library.
    Represents fully directed graph. Marked as graph of type G1 in the documentation.
    """
    def __init__(self, graph_G: PartiallyDirectedGraph):
        super(G1, self).__init__(self.transform_from_partially_directed(graph_G))

    @staticmethod
    def transform_from_partially_directed(graph_G: PartiallyDirectedGraph):
        """
        Transformation from graph G to G1 as in step 2 of the documentation.
        :return: graph G1 based on G.
        """
        g = graph_G.graph.copy()

        # count correction values because undirected edges are causing miscalculations of vertices' degrees
        correction_for_vs = defaultdict(int)    # default value is zero
        for edge in g.es:
            edge["transformed"] = False
            if edge["directed"] is False:
                correction_for_vs[edge.source] -= 1
                correction_for_vs[edge.target] += 1

        # greedy transformation of undirected edges
        for edge in g.es:
            if edge["directed"] is False:
                source_vertex_id = edge.source
                target_vertex_id = edge.target

                # degree = incoming - outgoing + correction
                source_vertex_degree = g.degree(source_vertex_id, type="in") - g.degree(source_vertex_id, type="out") \
                                       + correction_for_vs[source_vertex_id]
                if source_vertex_degree > 0:
                    # transform edge into outgoing
                    # in fact - reverse existing edge: delete current edge and add reversed one
                    g.delete_edges([(source_vertex_id, target_vertex_id)])
                    edge = g.add_edge(target_vertex_id, source_vertex_id)
                else:
                    # transform edge into incoming
                    # in fact - leave as it is, just flag it differently
                    pass
                edge["directed"] = True
                edge["transformed"] = True
                correction_for_vs[source_vertex_id] += 1
                correction_for_vs[target_vertex_id] -= 1

        return g
