from search import *
from utils import *
import random
import threading
import time
TOTAL_PUZZLES = 10
class DuckPuzzle(Problem):
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)
        if index_blank_square in [0,2,6]:
            possible_actions.remove('LEFT')
        if index_blank_square in [0,1,4,5]:
            possible_actions.remove('UP')
        if (index_blank_square > 3 and index_blank_square % 3 == 2) or (index_blank_square == 1):
            possible_actions.remove('RIGHT')
        if index_blank_square == 2 or index_blank_square > 5:
            possible_actions.remove('DOWN')
            
        return possible_actions

    def result(self, state, action):
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        
        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank <= 3:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """
        # Check if small square has 1,2,3 and contains 1,2,3 in clockwise order
        def check_2x2_puzzle():
            one_square = state.index(1)

            nums = list(filter(lambda x: x not in [1,2,3], state[:4]))
            remaining_num = 0 # the remaining number in 4 numbers that is not 1, 2 or 3
            if len(nums) > 1:
                return False
            else:
                remaining_num = nums[0]
                if remaining_num != 0 and state[:3] != (1,2,3):
                    return False
            
            clockwise_order = []
            iter = one_square
            step = 0
            while step < 4:
                if state[iter] in [1,2,3]:
                    clockwise_order.append(state[iter])
                if iter == 0:
                    iter += 1
                elif iter == 1:
                    iter += 2
                elif iter == 2:
                    iter -= 2
                elif iter == 3:
                    iter -= 1
                step += 1
            return clockwise_order == [1,2,3]
        
        is_2x2_puzzle_solvable = check_2x2_puzzle()
        if not is_2x2_puzzle_solvable:
            return False

        remaining_num = 0
        for i in state[:4]:
            if i not in [1,2,3]:
                remaining_num = i
                break
        inversion = 0
        clone_state = list(state)
        clone_state[3] = remaining_num
        
        for i in range(3,len(clone_state)):
            for j in range(i + 1, len(clone_state)):
                if (clone_state[i] > clone_state[j] and
                    clone_state[i] != 0 and
                    clone_state[j] != 0):
                    inversion += 1
        return inversion % 2 == 0 
        

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        return sum(s != g for (s, g) in zip(node.state, self.goal))
        

def make_rand_puzzle(kind="EightPuzzle"):
    state  = (0,1,2,3,4,5,6,7,8)
    list_state = list(state) # random.shuffle needs list
    tmp = EightPuzzle(state) # to use check_solvability
    if kind == "DuckPuzzle":
        tmp = DuckPuzzle(state)
    while True:
        random.shuffle(list_state)
        if (tmp.check_solvability(list_state)):
            if kind == "EightPuzzle":
                return EightPuzzle(tuple(list_state))
            if kind == "DuckPuzzle":
                return DuckPuzzle(tuple(list_state))
            
def display(state, kind="EightPuzzle"):
    """Display puzzle state based of puzzle kind"""
    if kind == "EightPuzzle":
        for i in range(3):
            for j in range(3):
                print(state[i*3 + j], end=' ')
            print()
    elif kind == "DuckPuzzle":
        for i in range(2):
            for j in range(2):
                print(state[i*2+j], end-'')
            if i != 1:
                print()
        for i in range(1,3):
            for j in range(3):
                print(state[i*3+j], end='')
            print()

def get_state_string(state, kind="EightPuzzle"):
    state_string = ""
    if kind == "EightPuzzle":
        for i in range(3):
            for j in range(3):
                state_string += str(state[i*3+j]) + " "
            state_string += "\n"
    elif kind == "DuckPuzzle":
        for i in range(2):
            for j in range(2):
                if i == 1 and j == 1:
                    break
                state_string += str(state[i*2+j]) + " "
            if i != 1:
                state_string += "\n"
        for i in range(1,3):
            for j in range(3):
                state_string += str(state[i*3 + j]) + " "
            state_string += "\n  "
    return state_string
    
def generate_puzzles(n, kind="EightPuzzle"):
    return [make_rand_puzzle(kind) for _ in range(n)]


# This is a modified version of best_first_graph_seach provided in search.py
# This version is used to compute some benchmarks
def best_first_graph_search_custom(problem, f):
    start_time = time.time()
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
            elapsed_time = time.time() - start_time
            return node, num_of_removed_node, elapsed_time
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    elapsed_time = time.time() - start_time
    return None, num_of_removed_node, elapsed_time 


def manhattan_heuristic(node):
    res = 0
    for i in range(9):
        if node.state[i] != 0:
            res += abs(i % 3 - (node.state[i]-1)%3) + abs(i // 3 - (node.state[i]-1)//3)
    return res

def max_of_manhattan_and_misplaced(problem):
    def h(state):
        return max(manhattan_heuristic(state), problem.h(state))
    return h

# This is a modified version of astar_search_custom provided in search.py
# This version is used to compute some benchmarks
def astar_search_custom(problem, h=None):
    h = memoize(h or problem.h, 'h')
    return  best_first_graph_search_custom(problem, lambda n: n.path_cost + h(n))

def astar_search_using_manhattan(problem):
    return astar_search_custom(problem, manhattan_heuristic)

def astar_search_using_max_of_manhattan_and_misplaced(problem):
    return astar_search_custom(problem, max_of_manhattan_and_misplaced(problem))

test_puzzles = [EightPuzzle((1,6,2,3,4,5,7,8,0)),
                EightPuzzle((8,4,3,5,7,6,2,1,0)),
                EightPuzzle((6,2,3,4,5,0,8,7,1)),
                EightPuzzle((3,5,1,8,6,2,7,0,4)),
                EightPuzzle((4,7,3,8,0,1,2,5,6))]

def compare_search_algorithms(puzzles, kind="EightPuzzle"):
    searchers = [{"func": astar_search_custom,
                  "name": "astar search using misplaced heuristic"},
                 {"func": astar_search_using_manhattan,
                  "name": "astar search using manhattan heuristic"},
                 {"func": astar_search_using_max_of_manhattan_and_misplaced,
                  "name": "astar search using max of manhattan and misplaced"}]
    with open(kind+"_benchmarks.txt", 'w') as outfile:
        for puzzle in puzzles:
            outfile.write("\n==========================================\n")
            outfile.write("Puzzle:\n")
            #display(puzzle.initial, kind)
            outfile.write(get_state_string(puzzle.initial, kind))
            for searcher in searchers:
                outfile.write("\n--------------------------------------\n")
                outfile.write(searcher["name"].upper() + "\n")
                goal_state, num_of_removed_node,elapsed_time = searcher["func"](puzzle)
                if goal_state:
                    outfile.write("Running time (in seconds): "
                                  + str(elapsed_time) + "\n")
                    outfile.write("Length of solution: "
                                  + str(goal_state.depth) + "\n")
                    outfile.write("Total number of removed nodes: "
                                  + str(num_of_removed_node) + "\n")
        

def eight_puzzles_benchmarks():
    print("Benchmarking for EightPuzzle")
    start_time = time.time()
    eight_puzzles = generate_puzzles(TOTAL_PUZZLES, kind="EightPuzzle")
    #eight_puzzles = [EightPuzzle((8,7,6,4,0,3,5,2,1))]
    compare_search_algorithms(eight_puzzles)
    elapsed_time = time.time() - start_time
    print("Total running time(in seconds) for all puzzles:", elapsed_time)
    print("Check details for benchmarking in EightPuzzle_benchmark.txt")
    
def duck_puzzles_benchmarks():
    print("Benchmarking for DuckPuzzle")
    start_time = time.time()
    duck_puzzles = generate_puzzles(TOTAL_PUZZLES, kind="DuckPuzzle")
    #duck_puzzles = [DuckPuzzle((8,1,3,2,7,5,4,0,6))]
    compare_search_algorithms(duck_puzzles, kind="DuckPuzzle")
    elapsed_time = time.time() - start_time
    print("Total running time(in seconds) for all puzzles:", elapsed_time)
    print("Check details for benchmarking in DuckPuzzle_benchmark.txt")
    
if __name__ == "__main__":
    pass
    eight_puzzles_benchmarks()
    #duck_puzzles_benchmarks()
    #print(DuckPuzzle(()).check_solvability((8,1,3,2,7,5,4,0,6)))
