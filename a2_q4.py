from a2_q1 import rand_graph
from a2_q2 import check_teams
import time
import random
import concurrent.futures
from csp import CSP, UniversalDict, different_values_constraint
from utils import argmin_random_tie


N = 105

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
    def __init__(self, csp, solution, runtime, steps):
        self.csp = csp
        self.runtime = runtime
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
            outfile.write("Runtime: " + str(self.runtime)+"\n")



def solve(graph):
    start = time.time()
    for colors in range(1,N+1):
        csp = MapColoringCSP(list(range(colors)), graph)
        print(colors)
        sol,steps = min_conflicts(csp,10000)
        if sol and csp.goal_test(sol):
            end = time.time()
            tmp = IceBreakerSolution(csp, sol, end-start, steps)
            return tmp
    return None

def run_q4():
    graphs = [rand_graph(0.1, N), rand_graph(0.2, N), rand_graph(0.3, N),
              rand_graph(0.4, N), rand_graph(0.5, N), rand_graph(0.6, N)]
    total_start = time.time()
    for graph in graphs:
        res = solve(graph)
        if res:
            res.output('csp_min_1.txt')
            print('Graph:', graph)
            print('Solution:', res.solution)
            print('Number of teams:', res.getNumOfTeams())
            print('Number of assigns:', res.csp.nassigns)
            print('Number of unassigns:', res.csp.nUnassigns)
            print('Number of steps:', res.steps)
    print('Total running time:', time.time() - total_start)


if __name__ == '__main__':
    run_q4()
