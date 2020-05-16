from search import *
from utils import *
import random
import threading
import time

def make_rand_8puzzle():
    state  = (0,1,2,3,4,5,6,7,8)
    list_state = list(state) # random.shuffle needs list
    tmp = EightPuzzle(state) # to use check_solvability
    while True:
        random.shuffle(list_state)
        if (tmp.check_solvability(list_state)):
            return EightPuzzle(tuple(list_state))

def display(state):
    for i in range(3):
        for j in range(3):
            print(state[i*3 + j], end=' ')
        print()

def generate_puzzles(n, kind="8puzzle"):
    if kind == "8puzzle":
        return [make_rand_8puzzle() for _ in range(n)]
    if kind == "duck":
        return None


# This is a modified version of best_first_graph_seach provided in search.py
# This version is used to compute some benchmarks
def best_first_graph_search_custom(problem, f):
    f = memoize(f, 'f')
    num_of_removed_node = 0
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        num_of_removed_node += 1
        if problem.goal_test(node.state):
            return node, num_of_removed_node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, num_of_removed_node

# This is a modified version of astar_search_custom provided in search.py
# This version is used to compute some benchmarks
def astar_search_custom(problem, h=None):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search_custom(problem, lambda n: n.path_cost + h(n))

def manhattan_heuristic(node):
    res = 0
    for i in range(9):
        if node.state[i] != 0:
            res += abs(i % 3 - (node.state[i]-1)%3) + abs(i // 3 - (node.state[i]-1)//3)
    return res

def max_of_manhattan_and_misplaced(problem):
    def func(state):
        return max(manhattan_heuristic(state), problem.h(state))
    return func

def astar_search_using_manhattan(problem):
    return astar_search_custom(problem, manhattan_heuristic)

def astar_search_using_max_of_manhattan_and_misplaced(problem):
    return astar_search_custom(problem, max_of_manhattan_and_misplaced(problem))

def compare_search_algorithms():
    puzzles = generate_puzzles(10)
    searchers = [{"func": astar_search_custom,
                  "name": "astar search using misplaced"},
                 {"func": astar_search_using_manhattan,
                  "name": "astar search using manhattan"},
                 {"func": astar_search_using_max_of_manhattan_and_misplaced,
                  "name": "astar search using max of manhattan and misplaced"}]
    for puzzle in puzzles:
        print("==========================================")
        print("Puzzle:")
        display(puzzle.initial)
        for searcher in searchers:
            print("--------------------------------------")
            print(searcher["name"].upper())
            goal_state, num_of_removed_node = searcher["func"](puzzle)
            if goal_state:
#                print("Solved for puzzle: ", puzzle.initial, len(goal_state.solution()))
                print("Running time: ", "")
                print("Length of solution: ", len(goal_state.solution()))
                print("Total number of removed nodes: ", num_of_removed_node)
#            print("--------------------------------------")
        print("===========================================")
            
trivial_problem = EightPuzzle((2,1,3,5,4,0,6,7,8))
trivial_2 = EightPuzzle((1,2,3,4,5,6,0,7,8))
if __name__ == "__main__":
    compare_search_algorithms()
