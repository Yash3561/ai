from grid import GRID_SIZE, grid
from collections import deque

# ai.py

from collections import deque

# BFS implementation to find the shortest path
def bfs(start, goal):
    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == goal:
            return path

        if current not in visited:
            visited.add(current)
            x, y = current
            # Possible moves: up, down, left, right
            neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            for neighbor in neighbors:
                if 0 <= neighbor[0] < 5 and 0 <= neighbor[1] < 5:  # Assuming grid size of 5x5
                    queue.append(path + [neighbor])
    return []  # No path found


def get_neighbors(x, y):
    neighbors = []
    # Check all 4 directions
    if x > 0: neighbors.append((x - 1, y))  # Up
    if x < GRID_SIZE - 1: neighbors.append((x + 1, y))  # Down
    if y > 0: neighbors.append((x, y - 1))  # Left
    if y < GRID_SIZE - 1: neighbors.append((x, y + 1))  # Right
    return neighbors
