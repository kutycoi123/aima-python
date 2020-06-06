from a2_q1 import rand_graph
def check_teams(graph, csp_sol):
    for node in graph:
        for neighbor in graph[node]:
            if csp_sol[node] == csp_sol[neighbor]:
                return False
    return True


