import unittest
from igraph import *
import algorithm as alg


class MyTestCase(unittest.TestCase):

    def test_checking_connectivity(self):

        g = Graph([(0, 1), (0, 2), (2, 1), (3, 4)])
        g.vs["name"] = ["a", "b", "c", "d", "e"]
        self.assertEqual(False, alg.is_connected(g))


if __name__ == '__main__':
    unittest.main()
