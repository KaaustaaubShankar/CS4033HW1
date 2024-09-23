from app import bfs, dfs, best_first_search, a_star_search, heuristic_with_bucharest, romania_map, heuristic_with_common_neighbor, heuristic_bucharest
import numpy as np
import matplotlib.pyplot as plt
import time

start_city = 'Arad'
goal_city = 'Bucharest'
# Initialize lists to store times and paths
bfs_times = []
dfs_times = []
best_first_times = []
a_star_times = []
a_star_b_times = []
a_star_t_times = []

bfs_path = None
dfs_path = None
best_first_path = None
a_star_path = None
a_star_hueristic_b_path = None
a_star_hueristic_t_path = None

# BFS tests

for _ in range(100):
    start_time = time.perf_counter()
    bfs_path = bfs(romania_map, start_city, goal_city)
    bfs_times.append(time.perf_counter() - start_time)  # Measure time for each iteration
bfs_time = sum(bfs_times) / len(bfs_times)  # Calculate average time

# DFS tests

for _ in range(100):
    start_time = time.perf_counter()
    dfs_path = dfs(romania_map, start_city, goal_city)
    dfs_times.append(time.perf_counter() - start_time)
dfs_time = sum(dfs_times) / len(dfs_times)

# Best first tests

for _ in range(100):
    start_time = time.perf_counter()
    best_first_path = best_first_search(romania_map, start_city, goal_city, heuristic_bucharest)
    best_first_times.append(time.perf_counter() - start_time)
best_time = sum(best_first_times) / len(best_first_times)

# A* tests and heuristics

for _ in range(100):
    start_time = time.perf_counter()
    a_star_path = a_star_search(romania_map, start_city, goal_city, heuristic_bucharest)
    a_star_times.append(time.perf_counter() - start_time)
a_star_time = sum(a_star_times) / len(a_star_times)

goal_city = 'Craiova'

for _ in range(100):
    start_time = time.perf_counter()
    a_star_hueristic_b_path = a_star_search(romania_map, start_city, goal_city, lambda city: heuristic_with_bucharest(city, goal_city))
    a_star_b_times.append(time.perf_counter() - start_time)
a_star_b_time = sum(a_star_b_times) / len(a_star_b_times)


for _ in range(100):
    start_time = time.perf_counter()
    a_star_hueristic_t_path = a_star_search(romania_map, start_city, goal_city, lambda city: heuristic_with_common_neighbor(city, goal_city, romania_map))
    a_star_t_times.append(time.perf_counter() - start_time)
a_star_t_time = sum(a_star_t_times) / len(a_star_t_times)

# Store value for the number of nodes searched for each path
bfs_nodes = len(bfs_path)
dfs_nodes = len(dfs_path)
best_first_nodes = len(best_first_path)
a_star_nodes = len(a_star_path)
a_star_hueristic_b_nodes = len(a_star_hueristic_b_path)
a_star_hueristic_t_nodes = len(a_star_hueristic_t_path)

# Initialize iterables for graph creation
algos = ["BFS", "DFS", "Best First", "A Star", "A Star B", "A Star T"]
node_counts = [bfs_nodes, dfs_nodes, best_first_nodes, a_star_nodes, a_star_hueristic_b_nodes, a_star_hueristic_t_nodes]

# Write results to a text file
with open("search_results.txt", "w") as file:
    file.write("Search Algorithm Results\n")
    file.write("========================\n")
    file.write(f"Average BFS time: {bfs_time} seconds\n")
    file.write(f"BFS path: {bfs_path}\n\n")
    file.write(f"Average DFS time: {dfs_time} seconds\n")
    file.write(f"DFS path: {dfs_path}\n\n")
    file.write(f"Average Best First time: {best_time} seconds\n")
    file.write(f"Best First path: {best_first_path}\n\n")
    file.write(f"Average A* time: {a_star_time} seconds\n")
    file.write(f"A* path: {a_star_path}\n\n")
    file.write(f"Average A* (Heuristic with Bucharest) time: {a_star_b_time} seconds\n")
    file.write(f"A* (Heuristic with Bucharest) path: {a_star_hueristic_b_path}\n\n")
    file.write(f"Average A* (Triangle Heuristic) time: {a_star_t_time} seconds\n")
    file.write(f"A* (Triangle Heuristic) path: {a_star_hueristic_t_path}\n\n")
    
    # Optional: Write the node counts for the bar graph
    file.write("Nodes Searched Per Search Function\n")
    for algo, count in zip(algos, node_counts):
        file.write(f"{algo}: {count} nodes searched\n")

# Bar graph creation
plt.bar(algos, node_counts, color=["#ef476f", "#f78c6b", "#ffd166", "#06d6a0", "#118ab2", "#073b4c"])
plt.title("Nodes Searched Per Search Function")
plt.xlabel("Algorithm Type")
plt.ylabel("Nodes Searched")
plt.show()
