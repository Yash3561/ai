from grid import GRID_SIZE, grid
import heapq  # Required for A* Priority Queue
from collections import deque
from config import GRID_SIZE, wumpus_position, pit_position  # Import shared constants


# ai.py

def dfs(start, goal):
    stack = [[start]]  # Stack to store paths
    visited = set()

    while stack:
        path = stack.pop()
        current = path[-1]

        print(f"\n-DFS Visiting: {current}, Path: {path}")

        if current == goal:
            return path

        if current not in visited:
            visited.add(current)
            x, y = current

            # Generate neighbors
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for neighbor in neighbors:
                if (
                    0 <= neighbor[0] < GRID_SIZE and
                    0 <= neighbor[1] < GRID_SIZE and
                    neighbor not in wumpus_position and  # Avoid Wumpus
                    neighbor not in pit_position  # Avoid pits
                ):
                    if neighbor not in path:
                        stack.append(path + [neighbor])

    return None  # No path found





from collections import deque

def bfs(start, goal):
    queue = deque([[start]])  # Queue to store paths
    visited = set()

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == goal:
            return path  # Found the shortest path

        if current not in visited:
            visited.add(current)
            x, y = current
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for neighbor in neighbors:
                if (
                    0 <= neighbor[0] < GRID_SIZE and
                    0 <= neighbor[1] < GRID_SIZE and
                    neighbor not in wumpus_position and  # Avoid Wumpus
                    neighbor not in pit_position  # Avoid pits
                ):
                    queue.append(path + [neighbor])

        print(f"\n-BFS Visiting: {path}, Current Node: {current}")
    return None  # No path found

def dijkstra(start, goal):
    # Priority queue: (cost, path)
    priority_queue = []
    heapq.heappush(priority_queue, (0, [start]))

    visited = {}  # Keeps track of the minimum cost to reach each node

    while priority_queue:
        cost, path = heapq.heappop(priority_queue)
        current = path[-1]

        # Debug output
        print(f"\n-Dijkstra Visiting: {current}, Cost: {cost}, Path: {path}")

        # If the goal is reached, return the path
        if current == goal:
            return path

        x, y = current
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        for neighbor in neighbors:
            if (
                0 <= neighbor[0] < GRID_SIZE and
                0 <= neighbor[1] < GRID_SIZE and
                neighbor not in wumpus_position and  # Avoid Wumpus
                neighbor not in pit_position  # Avoid pits
            ):
                new_cost = cost + 1
                if neighbor not in visited or new_cost < visited[neighbor]:
                    visited[neighbor] = new_cost
                    heapq.heappush(priority_queue, (new_cost, path + [neighbor]))

    return None  # Return None if no path is found


def a_star(start, goal):
    priority_queue = []
    heapq.heappush(priority_queue, (0, [start]))  # Push with initial priority 0
    visited = {}

    while priority_queue:
        cost, path = heapq.heappop(priority_queue)
        current = path[-1]

        if current == goal:
            return path  # Return the optimal path

        if current not in visited or cost < visited[current]:
            visited[current] = cost
            x, y = current
            # Possible moves: up, down, left, right
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for neighbor in neighbors:
                if (
                    0 <= neighbor[0] < GRID_SIZE and
                    0 <= neighbor[1] < GRID_SIZE and
                    neighbor not in wumpus_position and  # Avoid Wumpus
                    neighbor not in pit_position  # Avoid pits
                ):
                    new_cost = cost + 1
                    heapq.heappush(priority_queue, (new_cost + heuristic(neighbor, goal), path + [neighbor]))
        print(f"\n-A* Visiting: {path}, Current Node: {current}")


    return []  # No path found


def heuristic(a, b):
    x1, y1 = a
    x2, y2 = b
    # Add penalties for Wumpus or pits to discourage paths near them
    penalty = 0
    if (x1, y1) == wumpus_position:  # Example penalty for Wumpus
        penalty += 10
    return abs(x1 - x2) + abs(y1 - y2) + penalty





def get_neighbors(x, y):
    neighbors = []
    # Check all 4 directions
    if x > 0: neighbors.append((x - 1, y))  # Up
    if x < GRID_SIZE - 1: neighbors.append((x + 1, y))  # Down
    if y > 0: neighbors.append((x, y - 1))  # Left
    if y < GRID_SIZE - 1: neighbors.append((x, y + 1))  # Right
    return neighbors
