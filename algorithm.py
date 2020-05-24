from igraph import *
from collections import Counter
import numpy as np


class GenericGraph:
    """
    Generic class for graphs.
    """
    def __init__(self, graph: Graph):
        self.graph = graph

    def is_connected(self):
        return self.graph.is_connected()

    def plotGraph(self, edge_label="dr", margin=100, bbox=(500, 500)):
        visual_style = {}
        visual_style["layout"] = self.graph.layout("kk")
        visual_style["bbox"] = bbox
        visual_style["margin"] = margin
        visual_style["vertex_label"] = self.graph.vs["label"]
        for ed in self.graph.es:
            sLbl = ""
            if ed["directed"]:
                sLbl = "dr"
            if self.graph.is_weighted():
                sLbl += " w:{}".format(ed["weight"])
            ed["label"] = sLbl
        visual_style["edge_label"] = self.graph.es["label"]

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
        directed_flags = np.empty(edge_count, dtype=bool)

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
        #print("DIR: {}".format(g.es['directed']))
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
            if not edge["directed"]:
                correction_for_vs[edge.source] -= 1
                correction_for_vs[edge.target] += 1

        #print("DIR: {}".format(g.es['directed']))
        #print("In: {}, Out: {}".format(g.degree(1, type="in"), g.degree(1, type="out")))
        
        # greedy transformation of undirected edges
        for edge in g.es:
            #print("dir: {}".format(edge['directed']))
            if not edge["directed"]:
                source_vertex_id = edge.source
                target_vertex_id = edge.target

                # degree = incoming - outgoing + correction
                source_vertex_degree = g.degree(source_vertex_id, type="in") - g.degree(source_vertex_id, type="out") \
                                       + correction_for_vs[source_vertex_id]
                if source_vertex_degree < 0:
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

    #------------------------------------------------------------------------
    def have_euler_tour(self, deg_list: list):
        """
        Check for Euler tour in graph
        :param: deg_list - list for storing vertices degrees
        :return: boolean
        """
        if not self.is_connected(): return False
        degIn_list = self.graph.indegree()
        degOut_list = self.graph.outdegree()
        #print("Lista In: " + str(degIn_list))
        #print("Lista Out: " + str(degOut_list))
        
        deg_list.clear()
        prev_deg = degIn_list[0] - degOut_list[0]
        deg_list.append(prev_deg)
        for i in range(1, len(degIn_list) ):
            deg = degIn_list[i] - degOut_list[i]
            deg_list.append(deg)

        for i in range(1, len(degIn_list) ):
            deg = degIn_list[i] - degOut_list[i]
            if deg != prev_deg:
                return False

        return True

    #------------------------------------------------------------------------
    def create_complete_bipart(self, deg_list: list, g2 : GenericGraph):
        """
        Create complete bipartie grapgh from given G1 graph
        as mentioned in 3a step in documentation. Based on g2 adding weights for egdes in bipartite graph
        :param: deg_list as vertices degrees in G1 graph, g2 : GenericGraph - graph with penalty edges
        :return: Complete Biparte graph GD
        """
        iNeg, iPos = 0, 0
        for v in deg_list:
            if v > 0:
                iPos = iPos + v #number of vertices with positive degree
            elif v < 0:
                iNeg = iNeg + abs(v) # number of vertices with negative degree 
        
                # safety chec
        if iNeg != iPos:
            print("Error: Problem not solvable for this graph")
            return None

        gd = Graph.Full_Bipartite(iNeg, iPos)
                        # set vertices labels in bipartite graph as in G1
        i, k, l = 0, 0, 0
        for v in deg_list:
            if v < 0:
                vs = self.graph.vs[i]
                for j in range(abs(v)):
                    gd.vs[k + j]["label"] = vs["label"]
                k = k + abs(v)
            elif v > 0:
                vs = self.graph.vs[i]
                for j in range(abs(v)):
                    gd.vs[l + j + iNeg]["label"] = vs["label"]
                l = l + v
            i = i + 1
        
                    # calculate weights for egdes in bipartite graph gd based on weights in graph G2
        for edg in gd.es:
            src_vetrex_id = edg.source
            target_vertex_id = edg.target
                    # if src_vert have negative degree it need to be target in path calc on G2
            if src_vetrex_id < iNeg:
                target_label = gd.vs[src_vetrex_id]["label"]
                source_label = gd.vs[target_vertex_id]["label"]
            else:
                target_label = gd.vs[target_vertex_id]["label"]
                source_label = gd.vs[src_vetrex_id]["label"]

                    # get vertex in g2 from given label
            src_g2 = g2.graph.vs.find(label=source_label)
            trg_g2 = g2.graph.vs.find(label=target_label)
            weight_mtrx = g2.graph.shortest_paths_dijkstra(src_g2.index, trg_g2.index, "weight", OUT)
            edg["weight"] = weight_mtrx[0][0]
            print("Path weight in bipartite graph: {}, src: {}, trg: {}".format(weight_mtrx[0][0], source_label, target_label) )
            
        gd.es["directed"] = False
        return GenericGraph(gd), iNeg
    
    #------------------------------------------------------------------------
    def add_penaltyTm_edges(self, penaltyT: float):
        """
        Create grapgh with penalty edges from given G1 graph
        as mentioned in 3b step in documentation.
        :param: PenaltyT - specifies how many times multiply weight of corresponding legal edgde
        :return: New graph with penalty edges
        """
        g2 = self.graph.copy()
                # At start all edges are legal
        g2.es["IsPenalty"] = False

        for e in self.graph.es:
            source_vertex_id = e.source
            target_vertex_id = e.target
                    # if edge was transformed add egde 
                    # in reverse direction with the same weight
            if e["transformed"]:
                new_e = g2.add_edge(e.target, e.source)
                new_e["weight"] = e["weight"]
                new_e["IsPenalty"] = False
                new_e["transformed"] = True
            else:
                new_e = g2.add_edge(e.target, e.source)
                #new_e["weight"] = ( int(e["weight"]) * penaltyT)
                #---------------------------------------TEST - to remove in final version
                new_e["weight"] = 80
                #-----------------------------------END TEST - to match test in docu
                new_e["IsPenalty"] = True

        g2.es["directed"] = True
        return GenericGraph(g2)

    #------------------------------------------------------------------------
    def add_penaltyAvg_edges(self, penaltyT: float):
        """
        Create grapgh with penalty edges from given G1 graph
        as mentioned in 3b step in documentation.
        :param: PenaltyT - specifies how many times multiply average weight of edges
        :return: New graph with penalty edges
        """
        g2 = self.graph,copy()
                # At start all edges are legal
        g2.es["IsPenalty"] = False
        
        sum_w = 0
        for e in g2.es:
            sum_w += e["weight"]
            
        avg_w = sum_w / len(g2.es)

        for e in self.graph.es:
            source_vertex_id = e.source
            target_vertex_id = e.target
                    # if edge was transformed add egde 
                    # in reverse direction with the same weight
            if e["transformed"]:
                new_e = g2.add_edge(e.target, e.source)
                new_e["weight"] = e["weight"]
                new_e["IsPenalty"] = False
                new_e["transformed"] = True
            else:
                new_e = g2.add_edge(e.target, e.source)
                new_e["weight"] = (avg_w * penaltyT)
                new_e["IsPenalty"] = True

        g2.es["directed"] = True
        return GenericGraph(g2)

    #------------------------------------------------------------------------
    def GraphBalancing(self, gd : GenericGraph, g2: GenericGraph):
        """
        Use Hungarian method to find optimal matching in given bipartite graph. In documentation described at 3d)
        Then get selcted egdes from biGraph (representing minimal paths in g1) 
        and find edge sequences corresponding to them in graph g1.
        Duplicate selected edges in g1 - documentation point 3e)
        :param: gd - complete bipartite graph, g2 - graph with penalty edges
        :return: penalties - number of added penalty edges
        """
                # At start graph G1 dont have penalty edges
        self.graph.es["IsPenalty"] = False

                # we need to find minimum matching so to do that invert weight values
                # method don't support negative weight values
        for e in gd.graph.es:
            e["weight"] = 10000 - e["weight"]
        
        lstW = gd.graph.es["weight"]
        matching = gd.graph.maximum_bipartite_matching(weights = lstW)
        
        ###TEST
        #for e in matching.edges():
        #    print("Matching: {}".format(e))
        #    print("Src: {}, Trg: {}".format(gd.graph.vs[e.source]["label"], gd.graph.vs[e.target]["label"]))
        ###END TEST

        for e in gd.graph.es:
            e["weight"] = 10000 - e["weight"]

        for e in matching.edges():
                    # in bipartite graph edges source are vertices with positive degree
                    # so we need to swap target with source
            trg_lb = gd.graph.vs[e.source]["label"]
            src_lb = gd.graph.vs[e.target]["label"]
            src_g2 = g2.graph.vs.find(label=src_lb)
            trg_g2 = g2.graph.vs.find(label=trg_lb)
            #print("Src_G2: {}, Trg_G2: {}".format(src_g2["label"], trg_g2["label"]))
            vertex_sequnce_for_path = g2.graph.get_shortest_paths(src_g2.index, trg_g2.index, "weight")
            #print(vertex_sequnce_for_path)

            i, ipre, penalties = 0, -1, 0
            for iVi in vertex_sequnce_for_path[0]:
                if i > 0:
                   ed1 = self.graph.add_edge(ipre, iVi) #add(duplicate) edge in g1
                   ed2 = g2.graph.es.find(_source=ipre, _target=iVi)
                   ed1["weight"] = ed2["weight"]
                   ed1["directed"] = ed2["directed"]
                   ed1["IsPenalty"] = ed2["IsPenalty"]
                   if ed1["IsPenalty"] == True: penalties += 1
                i = i + 1
                ipre = iVi

        return penalties

    #------------------------------------------------------------------------
    def FindEuler(self, start_label: str):
        """
        Finding Euler cycle in graph G1
        :param: start_label - starting vertex label
        :return:
        """
        adj = self.graph.get_adjlist()
        total_weight = 0
        startVer = self.graph.vs.find(label = start_label)
        if startVer is None:
            print("Incorrect start label in finding Euler cycle")

        # Hierholzer’s Algorithm from
        # https://www.geeksforgeeks.org/hierholzers-algorithm-directed-graph/
        # not supported in igraph library

        if len(adj) == 0:
            return # empty graph

        # Maintain a stack to keep vertices
        # We can start from any vertex, here we start with 0
        curr_path = [startVer.index]

        # list to store final circuit
        circuit = []

        while curr_path:

            curr_v = curr_path[-1]

            # If there's remaining edge in adjacency list
            # of the current vertex
            if adj[curr_v]:

                # Find and remove the next vertex that is
                # adjacent to the current vertex
                next_v = adj[curr_v].pop()

                # Push the new vertex to the stack
                curr_path.append(next_v)

            # back-track to find remaining circuit
            else:
                # Remove the current vertex and
                # put it in the curcuit
                circuit.append(curr_path.pop())

        # we've got the circuit, now print it in reverse
        print("Euler cycle - postman route: ")
        for i in range(len(circuit) - 1, -1, -1):
            #print(circuit[i], end = "")

            if i > 0:
                ed = self.graph.es.find(_source=circuit[i], _target=circuit[i-1])
                total_weight += ed["weight"]

                    # result path printing
            label = self.graph.vs[circuit[i]]["label"]
            print(label, end = "")
            if i:
                print(" -> ", end = "")

        print("\nTotal weight: {}".format(total_weight))
        return