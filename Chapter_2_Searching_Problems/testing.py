import unittest
from typing import List, Optional

from Searching_Generic.structures import Maze, MCState, Node, display_solution, MAX_NUM
from excersises import binary_contains, linear_contains, create_test_list, dfs, bfs, astar
from Searching_Generic.searching import manhattan_distance, node_to_path


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_performance(self):
        array = create_test_list()
        print("Testing linear_contains and binary_contains:")
        for test_value in [10, 100000, 500000, 999999, 1000000]:
            print(f"\nSearching for {test_value}:")
            linear_contains(array, test_value)
            binary_contains(array, test_value)

    def test_searching(self):
        """ We will test dfs, bfs and A* on 100 Mazes"""
        solutions_for_dfs: List[int] = []
        solutions_for_bfs: List[int] = []
        solutions_for_astar: List[int] = []
        for _ in range(100):
            maze: Maze = Maze()
            solution1 = dfs(maze.start, maze.goal_test, maze.successors)
            solutions_for_dfs.append(solution1[1] if solution1[0] else 0)
            solution2 = bfs(maze.start, maze.goal_test, maze.successors)
            solutions_for_bfs.append(solution2[1] if solution1[0] else 0)
            distance = manhattan_distance(maze.goal)
            solution3 = astar(maze.start, maze.goal_test, maze.successors, distance)
            solutions_for_astar.append(solution3[1] if solution3[0] else 0)
        print(sum(solutions_for_dfs), "DFS States touched")
        print(sum(solutions_for_bfs), "BFS States touched")
        print(sum(solutions_for_astar), "A* States touched")

    def test_missionaries(self):
        MAX_NUMBER = MAX_NUM  # MAX NUM can be changed for any number of people
        start: MCState = MCState(MAX_NUMBER, MAX_NUMBER, True)
        solution: Optional[Node[MCState]] = bfs(start, MCState.goal_test, MCState.successors)[0]
        if solution:
            path: List[MCState] = node_to_path(solution)
            display_solution(path)


if __name__ == '__main__':
    unittest.main()
