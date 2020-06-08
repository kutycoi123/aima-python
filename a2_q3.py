from a2_q1 import rand_graph
from a2_q2 import check_teams
import time
from csp import CSP, parse_neighbors, forward_checking, mrv, lcv, backtracking_search, UniversalDict, different_values_constraint, AC3b

N = 31

class MY_CSP(CSP):

    def __init__(self, variables, domains, neighbors, constraints):
        super().__init__(variables, domains, neighbors, constraints)
        self.nUnassigns = 0

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]
            self.nUnassigns += 1
    
def MapColoringCSP(colors, neighbors):
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    return MY_CSP(list(neighbors.keys()), UniversalDict(colors), neighbors, different_values_constraint)

def mac(csp, var, value, assignment, removals, constraint_propagation=AC3b):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)[0]

class IceBreakerSolution:
    def __init__(self, csp, solution, runtime):
        self.csp = csp
        self.runtime = runtime
        self.solution = solution
    def getNumOfTeams(self):
        return len(set(self.solution.values()))
    def output(self, path):
        with open(path, 'a+') as outfile:
            outfile.write("\n===============================\n")
            outfile.write("Graph: " + str(self.csp.neighbors)+"\n")
            outfile.write("Solution: " + str(self.solution)+"\n")
            outfile.write("Number of teams: " + str(self.getNumOfTeams()) + "\n")
            outfile.write("Runtime: " + str(self.runtime)+"\n")
            outfile.write("Number of times CSP variables were assigned: " + str(self.csp.nassigns)+"\n")
            outfile.write("Number of times CSP variables were unassigned: " + str(self.csp.nUnassigns)+"\n")
        


            
if __name__ == "__main__":
    graphs = [rand_graph(0.1, N), rand_graph(0.2, N), rand_graph(0.3, N),
              rand_graph(0.4, N), rand_graph(0.5, N), rand_graph(0.6, N)]
    graphs = [{0: [3, 5, 6, 8, 10, 11, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28], 1: [3, 4, 5, 6, 7, 9, 10, 12, 13, 15, 16, 18, 19, 22, 24, 25, 27, 29], 2: [3, 5, 6, 7, 13, 15, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30], 3: [0, 1, 2, 6, 9, 11, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 27, 28, 29, 30], 4: [1, 5, 6, 8, 9, 10, 12, 13, 14, 15, 16, 20, 21, 23, 25, 26, 27, 28, 29, 30], 5: [0, 1, 2, 4, 6, 7, 9, 10, 12, 13, 14, 15, 16, 17, 18, 20, 22, 23, 24, 27, 30], 6: [0, 1, 2, 3, 4, 5, 7, 9, 10, 12, 13, 14, 15, 16, 19, 21, 22, 24, 25, 27, 28, 29], 7: [1, 2, 5, 6, 9, 11, 12, 13, 16, 18, 19, 22, 24, 25, 27, 28, 29, 30], 8: [0, 4, 10, 11, 13, 15, 16, 18, 19, 20, 22, 25, 27, 28], 9: [1, 3, 4, 5, 6, 7, 11, 14, 15, 18, 19, 20, 21, 24, 26, 28, 29, 30], 10: [0, 1, 4, 5, 6, 8, 11, 12, 13, 14, 16, 17, 18, 20, 21, 23, 24, 25, 27, 28, 30], 11: [0, 3, 7, 8, 9, 10, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28], 12: [1, 4, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 23, 24, 25, 28, 30], 13: [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 15, 17, 20, 21, 24, 26, 27, 28], 14: [3, 4, 5, 6, 9, 10, 12, 16, 19, 20, 24, 26, 28, 29, 30], 15: [0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 16, 18, 19, 20, 23, 24, 25, 26, 30], 16: [0, 1, 3, 4, 5, 6, 7, 8, 10, 11, 14, 15, 17, 19, 21, 23, 25, 27, 30], 17: [2, 5, 10, 11, 12, 13, 16, 18, 19, 20, 24, 26, 29], 18: [0, 1, 2, 3, 5, 7, 8, 9, 10, 11, 15, 17, 19, 21, 22, 23, 25, 26, 28, 29, 30], 19: [0, 1, 2, 3, 6, 7, 8, 9, 11, 12, 14, 15, 16, 17, 18, 20, 23, 24, 26, 27, 28, 30], 20: [0, 2, 3, 4, 5, 8, 9, 10, 11, 13, 14, 15, 17, 19, 22, 25, 26, 27, 29, 30], 21: [0, 2, 3, 4, 6, 9, 10, 11, 12, 13, 16, 18, 22, 24, 25, 26, 27, 28, 30], 22: [0, 1, 2, 3, 5, 6, 7, 8, 11, 18, 20, 21, 23, 24, 25, 28, 29, 30], 23: [0, 2, 3, 4, 5, 10, 12, 15, 16, 18, 19, 22, 25, 26, 30], 24: [0, 1, 2, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 17, 19, 21, 22, 26, 27, 30], 25: [0, 1, 4, 6, 7, 8, 10, 11, 12, 15, 16, 18, 20, 21, 22, 23, 28, 29, 30], 26: [2, 4, 9, 11, 13, 14, 15, 17, 18, 19, 20, 21, 23, 24, 28], 27: [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 13, 16, 19, 20, 21, 24, 28, 30], 28: [0, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 18, 19, 21, 22, 25, 26, 27, 29], 29: [1, 2, 3, 4, 6, 7, 9, 14, 17, 18, 20, 22, 25, 28], 30: [2, 3, 4, 5, 7, 9, 10, 12, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 27]}]
    for graph in graphs:
        start = time.time()
        for colors in range(1,N):
            csp = MapColoringCSP(list(range(colors)), graph)
            res = backtracking_search(csp, select_unassigned_variable=mrv, order_domain_values=lcv, inference=mac)

            if res:
                end = time.time()
                print(check_teams(csp.neighbors, res))
                print("Solution:", res)
                print("Graph:", graph)
                tmp = IceBreakerSolution(csp, res, end-start)
                #tmp.output("first_csp.txt")
                print("Colors:", colors)
                print("Num of teams:", tmp.getNumOfTeams())
                print("Num of assigns:", csp.nassigns)
                print("Num of unassings:", csp.nUnassigns)
                break
        print("Time elapsed:", end - start)
    

