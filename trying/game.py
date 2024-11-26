import pygame
from grid import init_grid
from agent import move_agent
from ai import bfs
from config import GRID_SIZE
from ui import init_ui, draw_grid, update_ui

def main():
    # Initialize Pygame window and game state
    window = init_ui()
    init_grid()  # Initialize grid with Wumpus, pits, agent, etc.

    agent_x, agent_y = 0, 0  # Initial position of the agent
    goal = (GRID_SIZE - 1, GRID_SIZE - 1)  # Assuming goal is at the bottom-right corner
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Drawing the grid and updating the window
        window.fill((0, 0, 0))  # Clear the screen
        draw_grid(window)
        update_ui(window)
        
        # Move agent (manual or AI-based)
        # For AI, use bfs or other AI algorithms to move the agent
        path = bfs((0, 0), goal)  # Example: Use BFS to get the path
        for (x, y) in path:
            agent_x, agent_y = x, y  # Move the agent to the next position in the path
        
        pygame.time.wait(500)  # Slow down the game loop
    
    pygame.quit()

if __name__ == "__main__":
    main()
