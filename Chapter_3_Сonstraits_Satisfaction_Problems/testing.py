import unittest
from random import choice
from typing import List, Dict, Optional

from Chapter_3_Сonstraits_Satisfaction_Problems.theory import CSP, MapColoringConstraint, QueensConstraint, Grid, \
    generate_grid, GridLocation, generate_domain, WordSearchConstraint, display_grid, SendMoreMoneyConstraint


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_Australia(self):
        variables: List[str] = ["Western Australia", "Northern Territory", "South Australia", "Queensland",
                                "New South Wales", "Victoria", "Tasmania"]
        domains: Dict[str, List[str]] = {}
        for variable in variables:
            domains[variable] = ["red", "green", "blue"]
        csp: CSP[str, str] = CSP(variables, domains)
        csp.add_constraint(MapColoringConstraint("Western Australia", "Northern Territory"))
        csp.add_constraint(MapColoringConstraint("Western Australia", "South Australia"))
        csp.add_constraint(MapColoringConstraint("South Australia", "Northern Territory"))
        csp.add_constraint(MapColoringConstraint("Queensland", "Northern Territory"))
        csp.add_constraint(MapColoringConstraint("Queensland", "South Australia"))
        csp.add_constraint(MapColoringConstraint("Queensland", "New South Wales"))
        csp.add_constraint(MapColoringConstraint("New South Wales", "South Australia"))
        csp.add_constraint(MapColoringConstraint("Victoria", "South Australia"))
        csp.add_constraint(MapColoringConstraint("Victoria", "New South Wales"))
        csp.add_constraint(MapColoringConstraint("Victoria", "Tasmania"))
        solution: Optional[Dict[str, str]] = csp.backtracking_search()
        if solution is None:
            print("No solution yet")
        else:
            print(solution)

    def test_8Queen(self):
        columns: List[int] = [1, 2, 3, 4, 5, 6, 7, 8]
        rows: Dict[int, List[int]] = {}
        for column in columns:
            rows[column] = [1, 2, 3, 4, 5, 6, 7, 8]
        csp: CSP[int, int] = CSP(columns, rows)
        csp.add_constraint(QueensConstraint(columns))
        solution: Optional[Dict[int, int]] = csp.backtracking_search()
        if solution:
            print(solution)

    def test_word_search(self):
        grid: Grid = generate_grid(9, 9)
        words: List[str] = ["MATTHEW", "JOE", "MARY", "SARAH", "SALLY"]
        locations: Dict[str, List[List[GridLocation]]] = {}
        for word in words:
            locations[word] = generate_domain(word, grid)
        csp: CSP[str, List[GridLocation]] = CSP(words, locations)
        csp.add_constraint(WordSearchConstraint(words))
        solution: Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()
        if solution:
            for word, grid_locations in solution.items():
                if choice([True, False]):
                    grid_locations.reverse()
                for index, letter in enumerate(word):
                    (row, col) = (grid_locations[index].row, grid_locations[index].column)
                    grid[row][col] = letter
            display_grid(grid)

    def test_sendmoremoney(self):
        letters: List[str] = ["S", "E", "N", "D", "M", "O", "R", "Y"]
        possible_digits: Dict[str, List[int]] = {}
        for letter in letters:
            possible_digits[letter] = [0,1,2,3,4,5,6,7,8,9]
        possible_digits["M"] = [1]
        csp: CSP[str, int] = CSP(letters, possible_digits)
        csp.add_constraint(SendMoreMoneyConstraint(letters))
        solution: Optional[Dict[str, int]] = csp.backtracking_search()
        if solution:
            print(solution)


if __name__ == '__main__':
    unittest.main()
