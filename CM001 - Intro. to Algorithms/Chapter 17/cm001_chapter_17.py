# -*- coding: utf-8 -*-
"""CM001 - Chapter 17.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1E97XH8951kwSXcin28GohwqMbTc4Z9FF

#Bellman-Ford SSSP in DAG using Dynamic Programming
"""

from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)

    def add_edge(self, u, v, w):
        self.graph[u].append((v, w))

    def topological_sort_util(self, v, visited, stack):
        visited[v] = True
        if v in self.graph:
            for node, weight in self.graph[v]:
                if not visited[node]:
                    self.topological_sort_util(node, visited, stack)
        stack.append(v)

    def topological_sort(self):
        visited = {v: False for v in range(self.V)}
        stack = []

        for i in range(self.V):
            if not visited[i]:
                self.topological_sort_util(i, visited, stack)

        return stack[::-1]

    def shortest_path(self, source):
        topological_order = self.topological_sort()
        distance = {v: float('inf') for v in range(self.V)}
        distance[source] = 0

        for u in topological_order:
            for v, w in self.graph[u]:
                if distance[u] != float('inf') and distance[u] + w < distance[v]:
                    distance[v] = distance[u] + w

        return distance

# Example usage:
if __name__ == "__main__":
    g = Graph(6)
    g.add_edge(0, 1, 5)
    g.add_edge(0, 2, 3)
    g.add_edge(1, 3, 6)
    g.add_edge(1, 2, 2)
    g.add_edge(2, 4, 4)
    g.add_edge(2, 5, 2)
    g.add_edge(2, 3, 7)
    g.add_edge(3, 4, -1)
    g.add_edge(4, 5, -2)

    source = 1
    shortest_distances = g.shortest_path(source)
    for vertex in range(g.V):
        print(f"Shortest distance from {source} to {vertex} is {shortest_distances[vertex]}")

"""# Floyd-Warshall APSP using Dynamic Programming"""

INF = float('inf')

def floyd_warshall(graph):
    V = len(graph)
    dist = [[0]*V for _ in range(V)]

    # Initialize dist matrix with graph weights
    for i in range(V):
        for j in range(V):
            dist[i][j] = graph[i][j]

    # Calculate shortest paths
    for k in range(V):
        for i in range(V):
            for j in range(V):
                # Update distance if there's a shorter path through vertex k
                if dist[i][k] != INF and dist[k][j] != INF and dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist

# Example usage:
if __name__ == "__main__":
    graph = [
        [0, 5, INF, 10],
        [INF, 0, 3, INF],
        [INF, INF, 0, 1],
        [INF, INF, INF, 0]
    ]

    shortest_paths = floyd_warshall(graph)
    print("Shortest distances between all pairs:")
    for row in shortest_paths:
        print(row)

"""#Arithmetic parenthesization"""

def matrix_chain_order(p):
    n = len(p) - 1  # Number of matrices
    m = [[0] * n for _ in range(n)]  # Minimum number of scalar multiplications
    s = [[0] * n for _ in range(n)]  # Splitting index

    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    return m, s

def print_optimal_parens(s, i, j):
    if i == j:
        print("A" + str(i), end="")
    else:
        print("(", end="")
        print_optimal_parens(s, i, s[i][j])
        print_optimal_parens(s, s[i][j] + 1, j)
        print(")", end="")

# Example usage:
if __name__ == "__main__":
    # Example matrices dimensions: A1: 10x30, A2: 30x5, A3: 5x60
    dimensions = [10, 30, 5, 60]

    m, s = matrix_chain_order(dimensions)
    print("Minimum number of scalar multiplications:", m[0][-1])
    print("Optimal parenthesization:", end=" ")
    print_optimal_parens(s, 0, len(dimensions) - 2)

"""#Piano/guitar fingering problem"""

def piano_fingering(notes):
    # Define finger numbers for each note
    fingers = [1, 2, 3, 4, 5]

    # Define the cost matrix: cost[i][j] represents the cost of transitioning from finger i to finger j
    cost = [[0, 1, 1, 1, 1],  # Finger 1 to all other fingers
            [1, 0, 1, 1, 1],  # Finger 2 to all other fingers
            [1, 1, 0, 1, 1],  # Finger 3 to all other fingers
            [1, 1, 1, 0, 1],  # Finger 4 to all other fingers
            [1, 1, 1, 1, 0]]  # Finger 5 to all other fingers

    # Initialize DP table and fingerings
    dp = [[float('inf')] * len(fingers) for _ in range(len(notes))]
    fingerings = [[-1] * len(fingers) for _ in range(len(notes))]

    # Initialize base case
    dp[0] = [0] * len(fingers)

    # Dynamic programming: fill the DP table
    for i in range(1, len(notes)):
        for j in range(len(fingers)):
            for k in range(len(fingers)):
                if dp[i][j] > dp[i - 1][k] + cost[k][j]:
                    dp[i][j] = dp[i - 1][k] + cost[k][j]
                    fingerings[i][j] = k

    # Backtrack to find optimal fingerings
    optimal_fingerings = []
    last_finger = dp[-1].index(min(dp[-1]))
    optimal_fingerings.append(last_finger)
    for i in range(len(notes) - 1, 0, -1):
        last_finger = fingerings[i][last_finger]
        optimal_fingerings.append(last_finger)

    optimal_fingerings.reverse()

    return optimal_fingerings

# Example usage:
if __name__ == "__main__":
    # Example notes (C major scale)
    notes = ["C", "D", "E", "F", "G", "A", "B", "C"]

    fingerings = piano_fingering(notes)
    print("Optimal fingerings:", fingerings)