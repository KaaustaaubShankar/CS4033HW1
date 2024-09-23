from app import bfs, dfs, best_first_search, a_star_search, heuristic_with_bucharest, romania_map, heuristic_with_common_neighbor,heuristic_bucharest
import numpy as np
import matplotlib.pyplot as plt
import time

start_city = 'Arad'
goal_city = 'Bucharest'

#BFS tests
start_time = time.perf_counter()
bfs_path = bfs(romania_map, start_city, goal_city)
bfs_time = time.perf_counter() - start_time
print(f'BFS search to Bucharest path: {bfs_path}')
print(f'Took: {bfs_time}\n')

#DFS tests
start_time = time.perf_counter()
dfs_path = dfs(romania_map, start_city, goal_city)
dfs_time = time.perf_counter() - start_time
print(f'DFS search to Bucharest path: {dfs_path}')
print(f'Took: {dfs_time}\n')

#Best first tests
start_time = time.perf_counter()
best_first_path = best_first_search(romania_map, start_city, goal_city, heuristic_bucharest)
best_time = time.perf_counter() - start_time
print(f'Best first search to Bucharest path: {best_first_path}')
print(f'Took: {best_time}\n')


#a  star tests and heuristics
start_time = time.perf_counter()
a_star_path = a_star_search(romania_map, start_city, goal_city, heuristic_bucharest)
a_star_time = time.perf_counter() - start_time
print("A* search (to Bucharest) path:", a_star_path)
print(f'Took: {a_star_time}')

goal_city = 'Craiova'
start_time = time.perf_counter()
a_star_hueristic_b_path = a_star_search(romania_map, start_city, goal_city, lambda city: heuristic_with_bucharest(city, goal_city))
a_star_b_time = time.perf_counter() - start_time
print("A* search (heuristic with bucharest heuristic) path:", a_star_hueristic_b_path)
print(f'Took: {a_star_b_time}\n')

start_time = time.perf_counter()
a_star_hueristic_t_path = a_star_search(romania_map, start_city, goal_city, lambda city: heuristic_with_common_neighbor(city, goal_city,romania_map))
a_star_t_time = time.perf_counter() - start_time
print("A* search (triangle heuristic) path:", a_star_hueristic_t_path)
print(f'Took: {a_star_t_time}\n')


#Store value for the number of nodes searched for each path
bfs_nodes = len(bfs_path)
dfs_nodes = len(dfs_path)
best_first_nodes = len(best_first_path)
a_star_path = len(a_star_path)
a_star_hueristic_b_path = len(a_star_hueristic_b_path)
a_star_hueristic_t_path = len(a_star_hueristic_t_path)

#Initialize itterables for graph creation
algos = ["BFS", "DFS", "Best First", "A Star", "A Star B", "A Star T"]
node_counts = [bfs_nodes, dfs_nodes, best_first_nodes, a_star_path, a_star_hueristic_b_path, a_star_hueristic_t_path]
y_axis = range(1, 11)


#bar graph creation

plt.bar(algos, node_counts, color = ["#ef476f", "#f78c6b", "#ffd166", "#06d6a0", "#118ab2", "#073b4c"])
plt.title("Nodes Searched Per Search Function")
plt.xlabel("Algorithm Type")
plt.ylabel("Nodes Searched")

plt.show()