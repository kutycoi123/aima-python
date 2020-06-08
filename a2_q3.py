from a2_q1 import rand_graph
from a2_q2 import check_teams
import time
import csp as CSP
from utils import *
N = 31

class IceBreakerSolution:
    def __init__(self, csp, solution, runtime, nAssigned):
        self.csp = csp
        self.runtime = runtime
        self.solution = solution
        self.nAssigned = nAssigned
    def getNumOfTeams(self):
        return len(set(self.solution.values()))
    def output(path):
        with open(path, 'a+') as outfile:
            outfile.write("\n===============================")
            outfile.write("Graph: " + str(self.csp.neighbors)+"\n")
            outfile.write("Solution: " + str(self.solution)+"\n")
            outfile.write("Runtime: " + str(self.runtime)+"\n")
            outfile.write("Number of times CSP variables were assigned and unassigned:" + str(self.nAssigned)+"\n")
        
# CSP Backtracking Search

# Variable ordering


def first_unassigned_variable(assignment, csp):
    """The default variable order."""
    return first([var for var in csp.variables if var not in assignment])


def mrv(assignment, csp):
    """Minimum-remaining-values heuristic."""
    return argmin_random_tie([v for v in csp.variables if v not in assignment],
                             key=lambda var: num_legal_values(csp, var, assignment))


def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count(csp.nconflicts(var, val, assignment) == 0 for val in csp.domains[var])


# Value ordering


def unordered_domain_values(var, assignment, csp):
    """The default value order."""
    return csp.choices(var)


def lcv(var, assignment, csp):
    """Least-constraining-values heuristic."""
    return sorted(csp.choices(var), key=lambda val: csp.nconflicts(var, val, assignment))


# Inference


def no_inference(csp, var, value, assignment, removals):
    return True


def forward_checking(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
    return True


def mac(csp, var, value, assignment, removals, constraint_propagation=CSP.AC3b):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)[0]


# The search, proper


def my_backtracking_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=no_inference):
    """[Figure 6.5]"""

    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    #assert result is None or csp.goal_test(result)
    return result



if __name__ == "__main__":
    graphs = [rand_graph(0.1, N), rand_graph(0.2, N), rand_graph(0.3, N),
              rand_graph(0.4, N), rand_graph(0.5, N), rand_graph(0.6, N)]
    test_graph = graphs[5]
    start = time.time()
    for colors in range(1,N):
        csp = CSP.MapColoringCSP(list(range(colors)), test_graph)
        res = my_backtracking_search(csp, select_unassigned_variable=mrv, order_domain_values=lcv, inference=forward_checking)
        #res = CSP.min_conflicts(csp, max_steps=100000)
        print(res)
        if res:
            end = time.time()
            print(check_teams(csp.neighbors, res))
            print("Solution:", res)
            print("Graph:", test_graph)
            tmp = IceBreakerSolution(csp, res, end-start, csp.nassigns)
            print("Colors:", colors)
            print("Num of teams:", tmp.getNumOfTeams())
            break
   
    print("Time elapsed:", end - start)
    

