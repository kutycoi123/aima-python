from random import choices
def rand_graph(p, n):
    graph = {}
    CONNECTED = 1
    NOT_CONNECTED = 0
    choice = [CONNECTED, NOT_CONNECTED] # 0 means not-connected, 1 means connected
    for node_begin in range(n):
        graph[node_begin] = [] 
        for node_end in range(n):
            if node_begin != node_end:
                rand_choice = choices(choice, [p, 1-p])
                if rand_choice[0] == CONNECTED:
                    graph[node_begin].append(node_end)
    return graph

