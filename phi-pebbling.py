import numpy as np
from itertools import combinations_with_replacement
from collections import deque

#Convert edge list format to numpy adjacency matrix.
def edge_list_to_adjacency_matrix(edge_data):
    n = len(edge_data)
    adj_matrix = np.zeros((n, n), dtype=int)
    
    for i, neighbors in enumerate(edge_data):
        if isinstance(neighbors, (list, tuple)):
            for neighbor in neighbors:
                if 0 <= neighbor < n:
                    adj_matrix[i][neighbor] = 1
                    adj_matrix[neighbor][i] = 1  # Undirected graph
        else:
            # Single neighbor
            neighbor = neighbors
            if 0 <= neighbor < n:
                adj_matrix[i][neighbor] = 1
                adj_matrix[neighbor][i] = 1
    
    return adj_matrix

# Generate all possible distributions after the initial phi-step phase
def generate_free_move_distributions(adj_matrix, initial_pebbles):
    n = len(adj_matrix)
    distributions = []
    
    def backtrack(vertex_idx, current_dist, remaining_moves):
        if vertex_idx == n:
            distributions.append(current_dist.copy())
            return
        
        pebbles_at_vertex = initial_pebbles[vertex_idx]
        
        if pebbles_at_vertex == 0:
            backtrack(vertex_idx + 1, current_dist, remaining_moves)
            return
        
        possible_destinations = [vertex_idx]  # Can stay at same vertex
        for neighbor in range(n):
            if adj_matrix[vertex_idx][neighbor] == 1:
                possible_destinations.append(neighbor)
        
        def distribute_pebbles(pebbles_left, temp_dist):
            if pebbles_left == 0:
                new_dist = current_dist.copy()
                for dest, count in temp_dist.items():
                    new_dist[dest] += count
                backtrack(vertex_idx + 1, new_dist, remaining_moves)
                return
            
            # Try placing next pebble at each possible destination
            for dest in possible_destinations:
                temp_dist[dest] = temp_dist.get(dest, 0) + 1
                distribute_pebbles(pebbles_left - 1, temp_dist)
                temp_dist[dest] -= 1
                if temp_dist[dest] == 0:
                    del temp_dist[dest]
        
        distribute_pebbles(pebbles_at_vertex, {})
    
    backtrack(0, [0] * n, sum(initial_pebbles))
    return distributions

# Check if we can move a pebble to the target vertex using Phi-pebbling rules
def can_move_pebbles(adj_matrix, pebbles, target):

    n = len(adj_matrix)
    
    # Phase 1: phi-step
    free_move_distributions = generate_free_move_distributions(adj_matrix, pebbles)
    
    if len(free_move_distributions) > 1000:
        # Sample a subset of distributions
        import random
        random.seed(42)  # For reproducible results
        free_move_distributions = random.sample(free_move_distributions, 1000)
    
    # Phase 2: standard pebbling
    for initial_state in free_move_distributions:
        if can_standard_pebble(adj_matrix, initial_state, target):
            return True
    
    return False

#check if we can reach target using only standard pebbling
def can_standard_pebble(adj_matrix, pebbles, target):
    n = len(adj_matrix)
    current_pebbles = pebbles.copy()

    if current_pebbles[target] > 0:
        return True
    
    # Try all possible sequences of standard pebbling moves using BFS
    queue = deque([tuple(current_pebbles)])
    visited = set()
    visited.add(tuple(current_pebbles))
    
    # Limit search depth to prevent infinite loops
    max_iterations = 10000
    iterations = 0
    
    while queue and iterations < max_iterations:
        iterations += 1
        state = list(queue.popleft())
        
        if state[target] > 0:
            return True
        
        for u in range(n):
            if state[u] >= 2:  
                for v in range(n):
                    if adj_matrix[u][v] == 1:  
                        new_state = state.copy()
                        new_state[u] -= 2
                        new_state[v] += 1
                        
                        new_state_tuple = tuple(new_state)
                        if new_state_tuple not in visited:
                            visited.add(new_state_tuple)
                            queue.append(new_state)
    
    return False

# Generate key pebble distributions to test
def generate_key_distributions(num_vertices, n_pebbles):
    distributions = []
    
    # Single vertex distributions
    for v in range(num_vertices):
        dist = [0] * num_vertices
        dist[v] = n_pebbles
        distributions.append(dist)
    
    # Even distribution
    base_pebbles = n_pebbles // num_vertices
    remainder = n_pebbles % num_vertices
    even_dist = [base_pebbles] * num_vertices
    for i in range(remainder):
        even_dist[i] += 1
    distributions.append(even_dist)
    
    # Other strategic distributions
    if num_vertices >= 2 and n_pebbles >= 2:
        # Split between two vertices
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                dist = [0] * num_vertices
                dist[i] = n_pebbles // 2
                dist[j] = n_pebbles - dist[i]
                distributions.append(dist)
    
    return distributions

# Check if n pebbles are sufficient to reach any vertex from any initial configuration
def can_pebble_all_vertices(adj_matrix, n_pebbles):
    num_vertices = len(adj_matrix)
    
    distributions_to_check = generate_key_distributions(num_vertices, n_pebbles)
    
    for target in range(num_vertices):
        for dist in distributions_to_check:
            if not can_move_pebbles(adj_matrix, dist, target):
                return False
    
    return True

def check_n_pebbles_sufficient(edge_data, n_pebbles):
    """
    Main function: Check if n pebbles are sufficient for the pebbling number.
    
    Args:
        edge_data: Edge list or adjacency list representation
        n_pebbles: Number of pebbles to test
    
    Returns:
        bool: True if n pebbles work, False otherwise
    """
    # Convert to adjacency matrix if needed
    if isinstance(edge_data[0], (list, tuple)) or not hasattr(edge_data, 'shape'):
        adj_matrix = edge_list_to_adjacency_matrix(edge_data)
    else:
        adj_matrix = np.array(edge_data)
    
    return can_pebble_all_vertices(adj_matrix, n_pebbles)

# Example usage #1:
if __name__ == "__main__":
    # Petersen Graph (adjacency list format)
    petersen_graph = [
    [1, 4, 5],     # vertex 0
    [0, 2, 6],     # vertex 1  
    [1, 3, 7],     # vertex 2
    [2, 4, 8],     # vertex 3
    [0, 3, 9],     # vertex 4
    [0, 7, 8],     # vertex 5
    [1, 8, 9],     # vertex 6
    [2, 5, 9],     # vertex 7
    [3, 5, 6],     # vertex 8
    [4, 6, 7]      # vertex 9
]
    
    print("Testing Phi-Pebbling of Petersen Graph :")
    print(f"Graph has {len(petersen_graph)} vertices")
    
    # Convert to adjacency matrix and print some info
    adj_matrix = edge_list_to_adjacency_matrix(petersen_graph)
    print(f"Adjacency matrix shape: {adj_matrix.shape}")
    print(f"Number of edges: {np.sum(adj_matrix) // 2}")
    
    for n in range(1, 10):
        result = check_n_pebbles_sufficient(petersen_graph, n)
        print(f"{n} pebbles: {'Sufficient' if result else 'Not sufficient'}")
        
        # Stop early if we find a sufficient number
        if result:
            print(f"Phi-Pebbling number of Petersen Graph: {n}")
            break

# Example usage #2:
if __name__ == "__main__":
    # Diameter 2 Graph Counterexample (adjacency list format)
    diam_2_counterexample = [
    [10,4,7,9],
    [11,4,5,8],
    [12,5,6,7],
    [13,6,8,9],
    [0,1,10,11],
    [1,2,11,12],
    [2,3,12,13],
    [0,2,10,12],
    [1,3,11,13],
    [0,3,10,13],
    [11,12,13,0,4,7,9],
    [10,12,13,1,4,5,8],
    [10,11,13,2,5,6,7],
    [10,11,12,3,6,8,9],
    [10,11,12,13] 
]
    
    print("Testing Phi-Pebbling Diameter 2 Graph Counterexample:")
    print(f"Graph has {len(diam_2_counterexample)} vertices")
    
    # Convert to adjacency matrix and print some info
    adj_matrix = edge_list_to_adjacency_matrix(diam_2_counterexample)
    print(f"Adjacency matrix shape: {adj_matrix.shape}")
    print(f"Number of edges: {np.sum(adj_matrix) // 2}")
    
    for n in range(1, 17):
        result = check_n_pebbles_sufficient(diam_2_counterexample, n)
        print(f"{n} pebbles: {'Sufficient' if result else 'Not sufficient'}")
        
        # Stop early if we find a sufficient number
        if result:
            print(f"Phi-Pebbling number of Diameter 2 Graph Counterexample: {n}")
            break
