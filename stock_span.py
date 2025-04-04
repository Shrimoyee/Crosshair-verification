import math

def factorial(n: int) -> int:
    '''Computes the factorial of a number.'''
    
    assert(isinstance(n,int) and n>=0), "Precondition: n must be a non-negative integer."
    result = 1
    for i in range(1, n + 1):
        result *= i
        assert result == math.factorial(i), "Invariant: Partial factorial must be correct."
    assert(result == math.factorial(n)), "Postcondition: Factorial must be correct."
    return result

def stock_span(prices: list[int]) -> list[int]:
    '''Computes the stock span values.'''

    assert(isinstance(prices,list) and all(p > 0 for p in prices)), "Precondition: All values in Prices must be positive and it must be a list"
    stack, spans = [], [0] * len(prices)
    for i, price in enumerate(prices):
        while stack and prices[stack[-1]] <= price:
            stack.pop()
        spans[i] = i - stack[-1] if stack else i + 1
        stack.append(i)
    assert(len(spans)==len(prices)), "Postcondition: Output length must match input."
    return spans

def astar(graph: dict, start: str, goal: str) -> list[str]:
    '''Finds shortest path using A* algorithm.'''

    assert start in graph and goal in graph, "Precondition: Start and goal must be in the graph."

    open_set, came_from = {start}, {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

    while open_set:
        current = min(open_set, key=lambda node: g_score[node]) 
        open_set.remove(current)

        assert all(node not in came_from for node in open_set), "Invariant: Open set should contain only unvisited nodes."
        assert all(node in graph for node in came_from), "Invariant: Every node in came_from must exist in the graph."
        assert all(g_score[node] >= g_score[came_from[node]] for node in came_from if node in g_score), "Invariant: Shortest path estimate (g-score) must not increase for an explored node."

        if current == goal:
            break  

        for neighbor in graph[current]: 
            tentative_g_score = g_score[current] + graph[current][neighbor]
            if tentative_g_score < g_score[neighbor]: 
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                open_set.add(neighbor)

    path = reconstruct_path(came_from, start, goal)

    assert path[0] == start and path[-1] == goal, "Postcondition: Path must start at 'start' and end at 'goal'."

    assert all(path[i] in graph and path[i + 1] in graph[path[i]] for i in range(len(path) - 1)), \
        "Postcondition: Every node in the path must be connected in the graph."

    return path


def reconstruct_path(came_from, start, goal):
    '''Reconstructs the path from start to goal.'''
    path = []
    while goal in came_from:
        path.append(goal)
        goal = came_from[goal]
    path.append(start)
    path.reverse()
    return path
