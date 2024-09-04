import time
from typing import Callable, List, Tuple, Optional, Set, Dict
from Searching_Generic.structures import Maze, MazeLocation, Node, T, Stack, Queue, PriorityQueue


# Number 1: Show the performance advantage of binary search over linear search by creat
# ing a list of one million numbers and timing how long it takes the linear_
#  contains() and binary_contains() functions defined in this chapter to find
#  various numbers in the list.

def timer_decorator(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> int:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function {func.__name__} executed in {end - start:.6f} seconds")
        return result

    return wrapper


def create_test_list() -> List[int]:
    array: List[int] = []
    for i in range(10000000):
        array.append(i)
    return array


@timer_decorator
def linear_contains(array: List[int], element: int) -> int:
    """Takes array and an element as input and outputs index of an element
    For our task we suppose that there always will be element"""
    for index, item in enumerate(array):
        if element == item:
            return index
    return -1


@timer_decorator
def binary_contains(array: List[int], element: int) -> int:
    low = 0
    high = len(array)
    while low <= high:
        mid = (low + high) // 2
        if mid == element:
            return mid
        elif element > mid:
            low = mid + 1
        else:
            high = mid - 1
    return -1


# Number 2:  Add a counter to dfs(), bfs(), and astar() to see how many states each
#  searches through for the same maze. Find the counts for 100 different mazes to
#  get statistically significant results.


def dfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Tuple[
    Optional[Node[T]], int]:
    """We rewrite dfs so it will return Tuple"""
    counter: int = 0
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    explored: Set[T] = {initial}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        if goal_test(current_state):
            return current_node, counter
        for child in successors(current_state):
            counter += 1
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None, counter


def bfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Tuple[
    Optional[Node[T]], int]:
    frontier: Queue[Node[T]] = Queue[Node[T]]()
    frontier.push(Node(initial, None))
    explored: Set[T] = {initial}
    counter: int = 0

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        if goal_test(current_state):
            return current_node, counter
        for child in successors(current_state):
            counter += 1
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None, counter


def astar(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]],
          heuristic: Callable[[T], float]) -> Tuple[Optional[Node[T]], int]:
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    explored: Dict[T, float] = {initial: 0.0}
    counter: int = 0

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        if goal_test(current_state):
            return current_node, counter
        for child in successors(current_state):
            counter += 1
            new_cost: float = current_node.cost + 1
            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
    return None, counter


# Number 3:  Find a solution to the missionaries-and-cannibals problem for a different num
# ber of starting missionaries and cannibals. Hint: you may need to add overrides
#  of the __eq__() and __hash__() methods to MCState.

def s():
    """I implemented 3rd ex in structures.py"""
    pass
