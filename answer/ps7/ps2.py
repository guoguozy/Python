# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
import copy
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:The graph's nodes represent the buildings in this problem.
# The grapg's edges represent the road between two buildings. The distances
# represent the distance between the two buildings, one is total distance,
# the other one is distance that must be spent outdoors.
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    #print("Loading map from file...")
    campus_graph = Digraph()  # 实例化Digraph
    with open(map_filename) as file_object:
        lines = file_object.readlines()
    for line in lines:
        list = line.split()
        if not campus_graph.has_node(Node(list[0])):
            campus_graph.add_node(Node(list[0]))  # 若不在即加入
        if not campus_graph.has_node(Node(list[1])):
            campus_graph.add_node(Node(list[1]))
        campus_graph.add_edge(WeightedEdge(  # 将该边加入
            Node(list[0]), Node(list[1]), list[2], list[3]))
    return campus_graph


# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out

# test_graph = load_map('test_load_map.txt')
# print(test_graph.get_edges_for_node(Node('a')))
# print(test_graph.get_edges_for_node(Node('b')))
# print(test_graph.get_edges_for_node(Node('c')))
# print(test_graph.has_node(Node('a')))
# print(test_graph.has_node(Node('b')))
# print(test_graph.has_node(Node('c')))
# print(test_graph.has_node(Node('d')))
# print(str(test_graph))

#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer: The objective function for this problem is a function get_best_path
# which returns the shortest path between buildings subject to constraints.
# Constraints: minimize the distance traveled while not exceeding the maximum
# distance outdoors, each edge has its direction.
#

# Problem 3b: Implement get_best_path


def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):

    if (not digraph.has_node(Node(start))) or (not digraph.has_node(Node(end))):
        raise ValueError  # 起点终点存在不在图中的情况
    elif start == end:  # 找到比现有path更佳的path则更改best_path
        best_dist[0] = path[1]
        best_path.clear()
        for j in range(len(path[0])):
            best_path.append(path[0][j])
        best_path.append(start)
    else:
        for i in digraph.get_edges_for_node(Node(start)):
            if str(i.get_destination()) not in path[0]:  # 排除构成环的情况
                tmp_path = copy.deepcopy(path)  # 深拷贝path
                tmp_path[0].append(start)  # 将之加入path
                tmp_path[1] = path[1]+int(i.get_total_distance())
                tmp_path[2] = path[2]+int(i.get_outdoor_distance())
                if tmp_path[2] <= max_dist_outdoors and tmp_path[1] <= best_dist[0]:
                    get_best_path(digraph, str(i.get_destination()), end, tmp_path,
                                  max_dist_outdoors, best_dist, best_path)
    return (best_path, best_dist[0])

# Problem 3c: Implement directed_dfs


def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    
    # TODO
    path = [[], 0, 0]
    best_dist = [max_total_dist]  # 构造初始变量
    result = get_best_path(digraph, start, end, path,
                           max_dist_outdoors, best_dist, [])
    if not result[0]:
        raise ValueError  # 如果找不到path
    else:
        return result[0]

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================


class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end,
                               total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()
