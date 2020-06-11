from a2_q1 import rand_graph
from a2_q2 import check_teams
import time
from csp import CSP, parse_neighbors, forward_checking, mrv, lcv, backtracking_search, UniversalDict, different_values_constraint

N = 31

class MY_CSP(CSP):

    def __init__(self, variables, domains, neighbors, constraints):
        super().__init__(variables, domains, neighbors, constraints)
        self.nUnassigns = 0 # number of times that variables are unassigned
        self.nPrunes = 0 # number of times that variables are pruned

    def unassign(self, var, assignment): #override method
        if var in assignment:
            del assignment[var]
            self.nUnassigns += 1
    def prune(self, var, value, removals): #override method
        self.curr_domains[var].remove(value)
        self.nPrunes += 1
        if removals is not None:
            removals.append((var, value))
            
def MapColoringCSP(colors, neighbors):
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    return MY_CSP(list(neighbors.keys()), UniversalDict(colors), neighbors, different_values_constraint)

class IceBreakerSolution:
    def __init__(self, csp, solution, algorithm_runtime, solution_runtime):
        self.csp = csp
        self.algorithm_runtime = algorithm_runtime
        self.solution_runtime = solution_runtime
        self.solution = solution
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
            outfile.write("Number of prune: " + str(self.csp.nPrunes)+"\n")
            outfile.write("Solution Runtime: " + str(self.solution_runtime)+"\n")
            outfile.write("Algorithm runtime: " + str(self.algorithm_runtime)+"\n")
            

def run_q3():
    graphs = [rand_graph(0.1, N), rand_graph(0.2, N), rand_graph(0.3, N),
              rand_graph(0.4, N), rand_graph(0.5, N), rand_graph(0.6, N)]

    total_start = time.time()
    for graph in graphs:
        algo_start = time.time()
        for colors in range(1,N+1):
            sol_start = time.time()
            csp = MapColoringCSP(list(range(colors)), graph)
            res = backtracking_search(csp, select_unassigned_variable=mrv, order_domain_values=lcv, inference=forward_checking)
            if res:
                end = time.time()
                tmp = IceBreakerSolution(csp, res, end-algo_start, end-sol_start)
                tmp.output("csp_5.txt")
                print(check_teams(csp.neighbors, res))
                print("Graph:", graph)
                print("Solution:", res)
                print("Colors:", colors)
                print("Num of teams:", tmp.getNumOfTeams())
                print("Num of assigns:", csp.nassigns)
                print("Num of unassings:", csp.nUnassigns)
                print("Num of prunes:", csp.nPrunes)
                print("Runtime:", end - sol_start)
                break
    print("Total runtime for 6 graphs:", time.time() - total_start)
    


            
if __name__ == "__main__":
    run_q3()

