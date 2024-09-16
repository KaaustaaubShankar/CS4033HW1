from collections import deque
import heapq

# Romania map as defined in the textbook
romania_map = {
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Zerind': [('Oradea', 71), ('Arad', 75)],
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
    'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
    'Sibiu': [('Oradea', 151), ('Arad', 140), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu': [('Bucharest', 90)],
    'Urziceni': [('Bucharest', 85), ('Hirsova', 98), ('Vaslui', 142)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)]
}

# Straight-Line Distance (SLD) to Bucharest 
heuristic_bucharest = {
    'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Drobeta': 242, 'Eforie': 161,
    'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226, 'Lugoj': 244,
    'Mehadia': 241, 'Neamt': 234, 'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193,
    'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374
}

def heuristic_with_bucharest(start, goal):
    if start in heuristic_bucharest and goal in heuristic_bucharest:
        # Using Bucharest as the intermediate city
        return min(heuristic_bucharest[start] + heuristic_bucharest[goal], heuristic_bucharest[start])
    return 0  # Fallback to 0 for unknown cities

# Heuristic 2: Triangle inequality with a common neighboring city
def heuristic_with_common_neighbor(start, goal, graph):
    neighbors_start = {neighbor for neighbor, _ in graph[start]}
    neighbors_goal = {neighbor for neighbor, _ in graph[goal]}
    common_neighbors = neighbors_start.intersection(neighbors_goal)

    if common_neighbors:
        common_city = next(iter(common_neighbors))  # Take the first common neighbor
        return heuristic_bucharest[start] + heuristic_bucharest[common_city]
    
    closest_city = next(iter(neighbors_start))  # Take the first neighbor of start
    return heuristic_bucharest[start] + heuristic_bucharest[closest_city]

# BFS algorithm
def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        (city, path) = queue.popleft()
        if city in visited:
            continue
        visited.add(city)

        for (neighbor, _) in graph[city]:
            if neighbor == goal:
                return path + [neighbor]
            else:
                queue.append((neighbor, path + [neighbor]))

    return None  # No path found

# DFS algorithm
def dfs(graph, start, goal, path=None, visited=None):
    if path is None:
        path = [start]
    if visited is None:
        visited = set()

    visited.add(start)

    if start == goal:
        return path

    for (neighbor, _) in graph[start]:
        if neighbor not in visited:
            new_path = dfs(graph, neighbor, goal, path + [neighbor], visited)
            if new_path:
                return new_path

    return None  # No path found

# Best-First Search
def best_first_search(graph, start, goal, heuristics):
    queue = [(heuristics[start], start, [start])]
    visited = set()

    while queue:
        _, city, path = heapq.heappop(queue)
        if city in visited:
            continue
        visited.add(city)

        if city == goal:
            return path

        for neighbor, _ in graph[city]:
            if neighbor not in visited:
                heapq.heappush(queue, (heuristics[neighbor], neighbor, path + [neighbor]))

    return None  # No path found

# A* Search
def a_star_search(graph, start, goal, heuristics):
    #see if heuristics is a function or a dictionary so we can convert it into a dictionary
    def get_heuristic(city):
        if callable(heuristics):  # Check if heuristics is a function
            return heuristics(city)
        else:
            return heuristics[city]  # Assume it's a dictionary

    queue = [(0 + get_heuristic(start), 0, start, [start])]
    visited = set()

    while queue:
        (estimated_cost, actual_cost, city, path) = heapq.heappop(queue)
        if city in visited:
            continue
        visited.add(city)

        if city == goal:
            return path

        for neighbor, distance in graph[city]:
            if neighbor not in visited:
                new_cost = actual_cost + distance
                estimated_cost = new_cost + get_heuristic(neighbor)
                heapq.heappush(queue, (estimated_cost, new_cost, neighbor, path + [neighbor]))

    return None  # No path found


start_city = 'Arad'
goal_city = 'Bucharest'

path = a_star_search(romania_map, start_city, goal_city, heuristic_bucharest)
print("A* search (to Bucharest) path:", path)

goal_city = 'Craiova'
path = a_star_search(romania_map, start_city, goal_city, lambda city: heuristic_with_bucharest(city, goal_city))
print("A* search (triangle heuristic) path:", path)

path = a_star_search(romania_map, start_city, goal_city, lambda city: heuristic_with_common_neighbor(city, goal_city,romania_map))
print("A* search (triangle heuristic) path:", path)
