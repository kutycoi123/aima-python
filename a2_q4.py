from a2_q1 import rand_graph
from a2_q2 import check_teams
import time
import random
import concurrent.futures
from csp import CSP, UniversalDict, different_values_constraint
from utils import argmin_random_tie


N = 105
STEPS = 10000
class MY_CSP(CSP):

    def __init__(self, variables, domains, neighbors, constraints):
        super().__init__(variables, domains, neighbors, constraints)
        self.nUnassigns = 0 # number of times that variables are unassigned

    def unassign(self, var, assignment): #override method
        if var in assignment:
            del assignment[var]
            self.nUnassigns += 1

            
def MapColoringCSP(colors, neighbors):
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    return MY_CSP(list(neighbors.keys()), UniversalDict(colors), neighbors, different_values_constraint)

def min_conflicts(csp, max_steps=100000):
    """Solve a CSP by stochastic Hill Climbing on the number of conflicts."""
    # Generate a complete assignment for all variables (probably with conflicts)
    csp.current = current = {}
    for var in csp.variables:
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    # Now repeatedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = csp.conflicted_vars(current)
        if not conflicted:
            return current, i
        var = random.choice(conflicted)
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    return None, max_steps


def min_conflicts_value(csp, var, current):
    """Return the value that will give var the least number of conflicts.
    If there is a tie, choose at random."""
    return argmin_random_tie(csp.domains[var], key=lambda val: csp.nconflicts(var, val, current))

class IceBreakerSolution:
    def __init__(self, csp, solution, algorithm_runtime, solution_runtime, steps):
        self.csp = csp
        self.algorithm_runtime = algorithm_runtime
        self.solution_runtime = solution_runtime
        self.solution = solution
        self.steps = steps
    def getNumOfTeams(self):
        return len(set(self.solution.values()))
    def output(self, path):
        with open(path, 'a+') as outfile:
            outfile.write("\n===============================\n")
            outfile.write("Graph: " + str(self.csp.neighbors)+"\n")
            outfile.write("Solution: " + str(self.solution)+"\n")
            outfile.write("Number of teams: " + str(self.getNumOfTeams()) + "\n")
            outfile.write("Number of times CSP variables were assigned: " + str(self.csp.nassigns)+"\n")
            outfile.write("Number of times CSP variables were unassigned: " + str(self.csp.nUnassigns)+"\n")
            outfile.write("Number of steps for min_conflicts to find a solution: " + str(self.steps)+"\n")
            outfile.write("Runtime for only solvable graph: " + str(self.solution_runtime)+"\n")
            outfile.write("Runtime for entire algorithm: " + str(self.algorithm_runtime) + "\n")

def solve(graph):
    algo_start = time.time()
    for colors in range(1,N+1):
        sol_start = time.time()
        csp = MapColoringCSP(list(range(colors)), graph)
        sol,steps = min_conflicts(csp,STEPS)
        if sol and csp.goal_test(sol):
            sol_end = time.time()
            tmp = IceBreakerSolution(csp, sol, sol_end-algo_start, sol_end-sol_start, steps)
            return tmp
    return None

def run_q4():
    for _ in range(5):
        graphs = [rand_graph(0.1, N), rand_graph(0.2, N), rand_graph(0.3, N),
                  rand_graph(0.4, N), rand_graph(0.5, N), rand_graph(0.6, N)]
        for graph in graphs:
            res = solve(graph)
            if res:
                # Uncomment line below to write result to file
                #res.output('out.txt')
                print('Graph:', graph)
                print('Solution:', res.solution)
                print('Number of teams:', res.getNumOfTeams())
                print('Number of assigns:', res.csp.nassigns)
                print('Number of unassigns:', res.csp.nUnassigns)
                print('Number of steps:', res.steps)
                print('Runtime for only solvable graph:',res.solution_runtime)
                print('Runtime for entire algorithm:',res.algorithm_runtime)


if __name__ == '__main__':
    run_q4()
