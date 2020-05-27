import unittest
from algorithm import *


class MyTestCase(unittest.TestCase):

    def test_checking_connectivity(self):
        # test as described in documentation
        # graph depicted on fig. 6 in documentation
        full_adjacency_matrix_sample = np.array([
            [-1,-1, 0, 0],  # a
            [-1, 0,-1, 0],  # b
            [ 0,-1,-1, 0],  # c
            [ 0, 0, 0,-1],  # d
            [ 0, 0, 0,-1]   # e
        ])
        labels = ["a", "b", "c", "d", "e"]
        weights = [1, 1, 1, 1, 1]
        graph = PartiallyDirectedGraph(full_adjacency_matrix_sample, labels, weights)
        # graph.plot()
        self.assertEqual(False, graph.is_connected())

    def test_transforming_g_to_g1(self):
        # graph depicted on fig. 2 in documentation
        full_adjacency_matrix_sample = np.array([
            [ 1, 0,-1],  # a
            [-1,-1, 0],  # b
            [ 0,-1, 1]   # c
        ])
        labels = ["a", "b", "c"]
        weights = [1, 1, 1]
        g = PartiallyDirectedGraph(full_adjacency_matrix_sample, labels, weights)
        # g.plotLabel(edge_label="directed")
        g1 = G1(g)
        # g1.plotLabel(edge_label="transformed")
        # g1.plotLabel(edge_label="directed")
        # g1.plotGraph()
        g1_expected = Graph([(0,1), (1,2), (2,0)], directed=True)
        g1_expected.vs["label"] = labels
        g1_expected.es["weight"] = weights
        self.assertEqual(g1_expected.get_adjacency(), g1.graph.get_adjacency())

    def test_doc_fig7(self):
        # graph G1 depicted on fig. 7 in documentation (edges d->f & f->c are undirected)
        full_adjacency_matrix = np.array([
            [ 1, 1,-1, 0, 0, 0, 0, 0, 0, 0, 0],  # a
            [-1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # b
            [ 0,-1, 0, 0, 0, 1, 1,-1, 0, 0, 0],  # c
            [ 0, 0, 0, 0,-1, 0,-1, 0, 1,-1, 0],  # d
            [ 0, 0, 1,-1, 0,-1, 0, 0,-1, 0, 1],  # e
            [ 0, 0, 0, 0, 0, 0, 0,-1, 0,-1,-1]   # f
        ])
        labels = ["a", "b", "c", "d", "e", "f"]
        weights = [10, 20, 12, 11, 12, 18, 20, 22, 5, 14, 3]
        g = PartiallyDirectedGraph(full_adjacency_matrix, labels, weights)
        g1 = G1(g)
        # g1.plotLabel(edge_label="transformed")
        self.assertTrue(g1.graph.es[g1.graph.get_eid(3, 5)]["transformed"])     # d->f
        self.assertTrue(g1.graph.es[g1.graph.get_eid(5, 2)]["transformed"])     # f->c

        cost, tour = g1.get_postman_tour(penalty=3, starting_vertex_label='a')

        #                 a -> b -> d -> e -> a -> b -> e -> a -> c -> e -> f -> c -> d -> f -> d -> e -> a
        tour_expected = ['a', 'b', 'd', 'e', 'a', 'b', 'e', 'a', 'c', 'e', 'f', 'c', 'd', 'f', 'd', 'e', 'a']
        cost_expected = 200
        self.assertEqual(cost_expected, cost)
        # self.assertEqual(tour_expected, tour)

    def test_transforming_from_adj_mat(self):

        adj_mat = np.array([
            [ 0, 1, 1],
            [ 1, 0, 0],
            [ 0, 1, 0],
        ])
        full_adj_mat = PartiallyDirectedGraph.transform_adj_mat_to_full(adj_mat)

        expected_full_adj_mat = np.array([
            [-1, 0, 1, 1],  # a
            [ 1,-1, 0,-1],  # b
            [ 0, 1,-1, 0]   # c
        ])
        self.assertTrue(PartiallyDirectedGraph.are_full_adj_mat_equal(expected_full_adj_mat, full_adj_mat))


if __name__ == '__main__':
    unittest.main()
