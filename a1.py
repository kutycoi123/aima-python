from search import *
from utils import *
import random
import threading
import time

TOTAL_PUZZLES = 10
EIGHT_PUZZLE = "EightPuzzle"
DUCK_PUZZLE = "DuckPuzzle"

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
    
    def random_moves(self, state, moves=500):
        res = state
        for i in range(moves):
            child_states = res.expand(self)
            index = random.randint(0,len(child_states)-1)
            res = child_states[index]
        return res
    
    def result(self, state, action):
        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        
        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        if blank < 3:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """
        """ Goal state look like this:
        1 2
        3 4 5 6
          7 8 *
        Strategy: Split puzzle into two sub puzzles: 2x2([[1,2],[3,4]]) and 2x3([[4,5,6],[7,8,*]])
                  The puzzle is solvable if these two sub puzzles are solvable
        """
        # Check if 2x2 sub puzzle is solvable
        def check_2x2_puzzle():
            """ For 2x2 puzzle to be solvable, it needs to contain [1,2,3] in clockwise order
                For example:
                    - * 1
                      3 2 is solvable
                    - * 1
                      2 3 is not solvable
            """
            one_square = state.index(1)
            nums = list(filter(lambda x: x not in [1,2,3], state[:4]))
            if len(nums) > 1:
                return False

            clockwise_order = []
            next = one_square
            step = 0
            while step < 4:
                if state[next] in [1,2,3]:
                    clockwise_order.append(state[next])
                if next  == 0:
                    next  += 1
                elif next  == 1:
                    next  += 2
                elif next  == 2:
                    next -= 2
                elif next == 3:
                    next -= 1
                step += 1
            if clockwise_order == [1,2,3]:
                remaining_num = nums[0]
                """In case there is a remaining number that is not 0, 1, 2 or 3
                   this number must sit at the bottom right corner of 2x2 puzzle 
                   For example:
                   3 1
                   2 8 5 4
                     0 7 6 
                   is solvable because 8 is sitting at the bottom right corner
                   1 2
                   8 3 5 4
                     0 7 6
                   is not solvable because we can't move 8 out of 2x2 puzzle
                """
                if remaining_num != 0:
                    return state.index(remaining_num) == 3
                return True
            else:
                return False
        
        is_2x2_puzzle_solvable = check_2x2_puzzle()
        if not is_2x2_puzzle_solvable:
            return False

        remaining_num = list(filter(lambda x: x not in [1,2,3], state[:4]))[0]
        inversion = 0
        clone_state = list(state)
        clone_state[3] = remaining_num

        # Check if the remaining 2x3 puzzle solvable
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
        misplaced = sum(s != g  for (s, g) in zip(node.state, self.goal))
        if node.state.index(0) != self.goal.index(0):
            return misplaced - 1
        return misplaced


def make_rand_8puzzle():
    state  = (0,1,2,3,4,5,6,7,8)
    list_state = list(state) # random.shuffle needs list
    dummy = EightPuzzle(state) # to use check_solvability
    while True:
        random.shuffle(list_state)
        if (dummy.check_solvability(list_state)):
            return EightPuzzle(tuple(list_state))
        
def make_rand_duckpuzzle():
    """Return a random duckpuzzle"""
    dummy = DuckPuzzle(())
    rand_node = dummy.random_moves(Node((1,2,3,4,5,6,7,8,0)))
    return DuckPuzzle(rand_node.state)
            
def generate_puzzles(n, kind=EIGHT_PUZZLE):
    """Generate n number of puzzles"""
    if kind == DUCK_PUZZLE:
        return [make_rand_duckpuzzle() for _ in range(n)]
    return [make_rand_8puzzle() for _ in range(n)]
            


def display(state, kind=EIGHT_PUZZLE):
    """Display 8puzzle(default) and duckpuzzle state based on passed value of "kind" parameter"""
    if kind == EIGHT_PUZZLE:
        for i in range(3):
            for j in range(3):
                print(state[i*3 + j], end=' ')
            print()
    elif kind == DUCK_PUZZLE:
        for i in range(2):
            for j in range(2):
                print(state[i*2+j], end-'')
            if i != 1:
                print()
        for i in range(1,3):
            for j in range(3):
                print(state[i*3+j], end='')
            print()
            
def get_state_string(state, kind=EIGHT_PUZZLE):
    """Return string representation for a given state"""
    state_string = ""
    if kind == EIGHT_PUZZLE:
        for i in range(3):
            for j in range(3):
                state_string += str(state[i*3+j]) + " "
            state_string += "\n"
    elif kind == DUCK_PUZZLE:
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

def misplaced(problem):
    def h(node):
        """Compute misplaced heuristic excluding empty tile"""
        misplaced_num = sum(s != g for (s,g) in zip(node.state, problem.goal))
        if node.state.index(0) != problem.goal.index(0):
            return misplaced_num - 1
        return misplaced_num
    return h

def manhattan_duckpuzzle(node):
    res = 0
    # Node state (2,3,1,8,4,7,5,0,6)
    # 2 3
    # 1 8 4 7
    #   5 0 6

    # tmp_state: (2,3,0,0,1,8,4,7,0,5,0,6)
    # 2 3 0 0
    # 1 8 4 7
    # 0 5 0 6
    tmp_state = list(node.state)
    tmp_state.insert(2,0)
    tmp_state.insert(3,0)
    tmp_state.insert(8,0)
    coord_map = {1:(0,0),2:(0,1),3:(1,0),4:(1,1),5:(1,2),6:(1,3),7:(2,1),8:(2,2)}
    for i in range(12):
        if tmp_state[i] != 0:
            res += abs(i % 4 - coord_map[tmp_state[i]][1]) + abs(i // 4 - coord_map[tmp_state[i]][0])
    return res


def manhattan_8puzzle(node):
    res = 0
    for i in range(9):
        if node.state[i] != 0:
            res += abs(i % 3 - (node.state[i]-1)%3) + abs(i // 3 - (node.state[i]-1)//3)
    return res

def max_of_manhattan_and_misplaced(problem,kind=EIGHT_PUZZLE):
    def h(state):
        if kind == DUCK_PUZZLE:
            return max(manhattan_duckpuzzle(state), problem.h(state))
        return max(manhattan_8puzzle(state), misplaced(problem)(state))
    return h


# This is a modified version of astar_search provided in search.py
# This version is used to compute some benchmarks
def my_astar_search(problem, h=None):
    h = memoize(h or problem.h, 'h')
    return  best_first_graph_search_custom(problem, lambda n: n.path_cost + h(n))

def astar_search_using_misplaced(problem, kind=None):
    h = misplaced(problem)
    return my_astar_search(problem, h)

def astar_search_using_manhattan(problem, kind=EIGHT_PUZZLE):
    if kind == DUCK_PUZZLE:
        return my_astar_search(problem, manhattan_duckpuzzle)
    return my_astar_search(problem, manhattan_8puzzle)

def astar_search_using_max_of_manhattan_and_misplaced(problem, kind=EIGHT_PUZZLE):
    return my_astar_search(problem, max_of_manhattan_and_misplaced(problem,kind))


def compare_search_algorithms(puzzles, kind=EIGHT_PUZZLE, path=None):
    searchers = [{"func": astar_search_using_misplaced,
                  "name": "astar search using misplaced heuristic"},
                 {"func": astar_search_using_manhattan,
                  "name": "astar search using manhattan heuristic"},
                 {"func": astar_search_using_max_of_manhattan_and_misplaced,
                 "name": "astar search using max of manhattan and misplaced"}]
    file_path = path or kind+"_benchmarks.txt"
    with open(file_path, 'w') as outfile:
        for puzzle in puzzles:
            outfile.write("\n==========================================\n")
            outfile.write("Puzzle:\n")
            outfile.write(get_state_string(puzzle.initial, kind))
            for searcher in searchers:
                outfile.write("\n--------------------------------------\n")
                outfile.write(searcher["name"].upper() + "\n")
                goal_state, num_of_removed_node,elapsed_time = searcher["func"](puzzle,kind)
                if goal_state:
                    outfile.write("Running time (in seconds): "
                                  + str(elapsed_time) + "\n")
                    outfile.write("Length of solution: "
                                  + str(goal_state.depth) + "\n")
                    outfile.write("Total number of removed nodes: "
                                  + str(num_of_removed_node) + "\n")

def puzzle_benchmark(kind):
    """Calculate benchmarks for solving puzzles"""
    puzzles = generate_puzzles(TOTAL_PUZZLES, kind=kind)
    #puzzles = [EightPuzzle((7,3,4,1,0,8,2,6,5)),
    #           EightPuzzle((4,6,7,5,0,2,3,1,8)),
    #           EightPuzzle((6,2,5,3,4,1,0,8,7)),
    #           EightPuzzle((0,2,5,8,7,3,1,4,6)),
    #           EightPuzzle((1,7,8,3,2,4,6,0,5)),
    #           EightPuzzle((4,0,7,2,1,8,6,3,5)),
    #           EightPuzzle((4,1,7,3,5,2,8,0,6)),
    #           EightPuzzle((7,1,2,0,4,6,5,3,8)),
    #           EightPuzzle((1,3,4,6,2,5,0,7,8)),
    #           EightPuzzle((7,5,0,6,2,1,4,3,8))]
    compare_search_algorithms(puzzles, kind=kind)

    
if __name__ == "__main__":
    pass
    puzzle_benchmark(EIGHT_PUZZLE)
    #puzzle_benchmark(DUCK_PUZZLE)
