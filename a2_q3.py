from a2_q1 import rand_graph
from a2_q2 import check_teams
import time
import csp as CSP
from utils import *
N = 31

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


#def mac(csp, var, value, assignment, removals, constraint_propagation=AC3b):
#    """Maintain arc consistency."""
#    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)


# The search, proper


def my_inference(csp, var, value, assignment, removals):
    return CSP.AC3(csp, removals=removals)[0]

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
                    if result is not None and csp.goal_test(result):
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    #assert result is None or csp.goal_test(result)
    #print(result)
    #print(csp.goal_test(result))
    return result



if __name__ == "__main__":
    graphs = [rand_graph(0.1, N), rand_graph(0.2, N), rand_graph(0.3, N),
              rand_graph(0.4, N), rand_graph(0.5, N), rand_graph(0.6, N)]
    #print(graphs[0])
    test_graph = CSP.MapColoringCSP(range(31), graphs[5])
    #test_graph = csp.MapColoringCSP([0,1,2], {0: [1, 2], 1: [0], 2: [0], 3: []})
    res = my_backtracking_search(test_graph, inference=my_inference)
    #res = csp.min_conflicts(test_graph)
    if res:
        print(check_teams(graphs[5], res))
        print(res)
    else:
        print("No solution")

