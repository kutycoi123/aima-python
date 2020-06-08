from random import choices
def rand_graph(p, n):
    graph = {}
    CONNECTED = 1
    NOT_CONNECTED = 0
    for node in range(n):
        graph[node] = []
    for node in range(n):
        for neighbor in range(node+1, n):
            rand_choice = choices([CONNECTED, NOT_CONNECTED], [p, 1-p])
            if rand_choice[0] == CONNECTED:
                graph[node].append(neighbor)
                graph[neighbor].append(node)
    return graph

