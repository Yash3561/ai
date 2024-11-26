# main.py

import pygame
import time
from agent import agent_position, move_agent
from ai import bfs
from grid import GRID_SIZE, grid, draw_grid

# Glitter (Gold) position
glitter_position = (0, 4)  # Example position (top-right corner)

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wumpus World Game")

# Font for text
font = pygame.font.SysFont(None, 30)

# Function to handle manual input for movement
def handle_manual_input():
    global agent_position
    running = True
    while running:
        draw_grid(screen, agent_position, font)
        pygame.display.flip()

        # Check if agent reaches glitter
        if agent_position == glitter_position:
            print("You found the glitter! Congratulations!")
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    agent_position = move_agent(agent_position[0], agent_position[1], "up")
                if event.key == pygame.K_DOWN:
                    agent_position = move_agent(agent_position[0], agent_position[1], "down")
                if event.key == pygame.K_LEFT:
                    agent_position = move_agent(agent_position[0], agent_position[1], "left")
                if event.key == pygame.K_RIGHT:
                    agent_position = move_agent(agent_position[0], agent_position[1], "right")
                time.sleep(0.1)  # Small delay for smooth movement

# Function to run AI agent (using BFS)
def ai_mode():
    global agent_position
    start = (0, 0)
    goal = glitter_position  # Targeting the glitter (Gold)
    path = bfs(start, goal)

    if not path:
        print("No path found!")
        return

    for move in path:
        agent_position = move
        draw_grid(screen, agent_position, font)
        pygame.display.flip()

        # Check if agent reaches glitter
        if agent_position == glitter_position:
            print("AI found the glitter!")
            break  # End the AI movement

        time.sleep(0.5)  # Pause between each step to show AI movement

# Main function to choose between manual and AI mode
def main():
    global agent_position
    agent_position = (0, 0)  # Reset agent's starting position

    # Main loop
    running = True
    while running:
        screen.fill((0, 0, 0))

        # Display options for manual or AI mode
        text = font.render("Press M for Manual, A for AI", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # Manual mode
                    handle_manual_input()
                elif event.key == pygame.K_a:  # AI mode
                    ai_mode()
                elif event.key == pygame.K_ESCAPE:  # Exit
                    running = False

    pygame.quit()

if __name__ == "__main__":
    main()
