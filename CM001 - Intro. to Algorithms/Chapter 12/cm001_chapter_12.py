# -*- coding: utf-8 -*-
"""CM001 - Chapter 12.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hqjSLzAGdAhnoUDTRo9gl2viGpaJieO1

#Weighted graph radius
"""

import heapq
from collections import defaultdict

def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

def graph_radius(graph):
    min_radius = float('infinity')
    vertices = list(graph.keys())

    for vertex in vertices:
        distances = dijkstra(graph, vertex)
        max_distance = max(distances.values())
        min_radius = min(min_radius, max_distance)

    return min_radius

# Example usage:
# Define a weighted graph as an adjacency list
weighted_graph = {
    'A': {'B': 2, 'C': 4},
    'B': {'A': 2, 'C': 1},
    'C': {'A': 4, 'B': 1}
}

radius = graph_radius(weighted_graph)
print("Radius of the graph:", radius)

"""#Weighted ratios"""

def calculate_weighted_ratios(graph):
    weighted_ratios = {}

    for vertex, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            weighted_ratios[(vertex, neighbor)] = weight / sum(neighbors.values())

    return weighted_ratios

# Example usage:
# Define a weighted graph as an adjacency list
weighted_graph = {
    'A': {'B': 2, 'C': 4},
    'B': {'A': 2, 'C': 1},
    'C': {'A': 4, 'B': 1}
}

weighted_ratios = calculate_weighted_ratios(weighted_graph)
print("Weighted Ratios:")
for edge, ratio in weighted_ratios.items():
    print(f"{edge}: {ratio}")

"""#Johnson's Algorithm"""

import heapq

def bellman_ford(graph, source):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[source] = 0
    predecessors = {vertex: None for vertex in graph}

    for _ in range(len(graph) - 1):
        for vertex in graph:
            for neighbor, weight in graph[vertex].items():
                if distances[vertex] + weight < distances[neighbor]:
                    distances[neighbor] = distances[vertex] + weight
                    predecessors[neighbor] = vertex

    return distances, predecessors

def reweight_edges(graph, distances):
    reweighted_graph = {vertex: {neighbor: weight + distances[vertex] - distances[neighbor] for neighbor, weight in neighbors.items()} for vertex, neighbors in graph.items()}
    return reweighted_graph

def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

def johnsons_algorithm(graph):
    graph['new_vertex'] = {vertex: 0 for vertex in graph}
    distances, predecessors = bellman_ford(graph, 'new_vertex')
    del graph['new_vertex']

    if any(distances[neighbor] > distances[vertex] + weight for vertex, neighbors in graph.items() for neighbor, weight in neighbors.items()):
        raise ValueError("Graph contains a negative cycle")

    reweighted_graph = reweight_edges(graph, distances)

    shortest_paths = {}
    for vertex in graph:
        shortest_paths[vertex] = dijkstra(reweighted_graph, vertex)

        # Adjust distances back by subtracting the reweighting
        shortest_paths[vertex] = {neighbor: distance - distances[vertex] + distances[neighbor] for neighbor, distance in shortest_paths[vertex].items()}

    return shortest_paths

# Example usage:
# Define a weighted graph as an adjacency list
weighted_graph = {
    'A': {'B': 2, 'C': 4},
    'B': {'A': 2, 'C': 1},
    'C': {'A': 4, 'B': 1}
}

shortest_paths = johnsons_algorithm(weighted_graph)
print("Shortest Paths:")
for vertex, paths in shortest_paths.items():
    print(f"From vertex {vertex}: {paths}")

"""Source: https://www.geeksforgeeks.org/johnsons-algorithm/"""

import sys

# Number of vertices in the graph
V = 4

# A utility function to find the vertex with minimum distance value, from
# the set of vertices not yet included in shortest path tree


def minDistance(dist, sptSet):
	# Initialize min value
	min_val = sys.maxsize
	min_index = 0

	for v in range(V):
		if sptSet[v] == False and dist[v] <= min_val:
			min_val = dist[v]
			min_index = v

	return min_index

# A utility function to print the constructed distance array


def printSolution(dist):
	print("Following matrix shows the shortest distances between every pair of vertices")
	for i in range(V):
		for j in range(V):
			if dist[i][j] == sys.maxsize:
				print("{:>7s}".format("INF"), end="")
			else:
				print("{:>7d}".format(dist[i][j]), end="")
		print()

# Solves the all-pairs shortest path problem using Johnson's algorithm


def floydWarshall(graph):
	dist = [[0 for x in range(V)] for y in range(V)]

	# Initialize the solution matrix same as input graph matrix. Or
	# we can say the initial values of shortest distances are based
	# on shortest paths considering no intermediate vertex.
	for i in range(V):
		for j in range(V):
			dist[i][j] = graph[i][j]

	# Add all vertices one by one to the set of intermediate vertices.
	# Before start of a iteration, we have shortest distances between all
	# pairs of vertices such that the shortest distances consider only the
	# vertices in set {0, 1, 2, .. k-1} as intermediate vertices.
	# After the end of a iteration, vertex no. k is added to the set of
	# intermediate vertices and the set becomes {0, 1, 2, .. k}
	for k in range(V):
		# Pick all vertices as source one by one
		for i in range(V):
			# Pick all vertices as destination for the
			# above picked source
			for j in range(V):
				# If vertex k is on the shortest path from
				# i to j, then update the value of dist[i][j]
				if dist[i][k] + dist[k][j] < dist[i][j]:
					dist[i][j] = dist[i][k] + dist[k][j]

	# Print the shortest distance matrix
	printSolution(dist)


# driver program to test above function
if __name__ == "__main__":

	''' Let us create the following weighted graph
			10
	(0)------->(3)
		|		 /|\
	5 |		 |
		|		 | 1
	\|/		 |
	(1)------->(2)
			3		 '''

	graph = [[0, 5, sys.maxsize, 10],
			[sys.maxsize, 0, 3, sys.maxsize],
			[sys.maxsize, sys.maxsize, 0, 1],
			[sys.maxsize, sys.maxsize, sys.maxsize, 0]
		]

	# Print the solution
	floydWarshall(graph)

graph = [
    [0, 2, 4, sys.maxsize],
    [2, 0, 1, sys.maxsize],
    [4, 1, 0, sys.maxsize],
    [sys.maxsize, sys.maxsize, sys.maxsize, 0]
]
floydWarshall(graph)