from grid import GRID_SIZE, grid
from ai import get_neighbors  # Import get_neighbors from ai.py

# Agent's position (initially at (0, 0))
agent_position = (0, 0)

# Function to move the agent
def move_agent(agent_x, agent_y, direction):
    if direction == "up" and agent_x > 0:
        agent_x -= 1
    elif direction == "down" and agent_x < GRID_SIZE - 1:
        agent_x += 1
    elif direction == "left" and agent_y > 0:
        agent_y -= 1
    elif direction == "right" and agent_y < GRID_SIZE - 1:
        agent_y += 1
    return agent_x, agent_y

# Function to get the agent's perception of its current location
def perceive(x, y):
    percepts = {"Breeze": False, "Stench": False, "Glitter": False}
    for nx, ny in get_neighbors(x, y):
        if grid[nx][ny] == "P":
            percepts["Breeze"] = True
        if grid[nx][ny] == "W":
            percepts["Stench"] = True
    if grid[x][y] == "G":
        percepts["Glitter"] = True
    return percepts