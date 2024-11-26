# grid.py

import pygame

# Grid size
GRID_SIZE = 5

# Grid layout with initial objects (empty, Wumpus, Gold, Pit)
grid = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# For testing purposes, let's add some objects
grid[2][2] = "W"  # Wumpus
grid[0][4] = "G"  # Glitter (Gold) at (0, 4)
grid[4][0] = "P"  # Pit

# Draw the grid
def draw_grid(screen, agent_position, font):
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    screen.fill(BLACK)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (row, col) == agent_position:
                pygame.draw.rect(screen, BLUE, rect)  # Draw agent position in blue
                text = font.render("A", True, WHITE)
                screen.blit(text, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))
            elif grid[row][col] == "W":
                pygame.draw.rect(screen, RED, rect)  # Wumpus in red
                text = font.render("W", True, WHITE)
                screen.blit(text, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))
            elif grid[row][col] == "G":
                pygame.draw.rect(screen, YELLOW, rect)  # Glitter in yellow
                text = font.render("G", True, WHITE)
                screen.blit(text, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))
            elif grid[row][col] == "P":
                pygame.draw.rect(screen, GREEN, rect)  # Pit in green
                text = font.render("P", True, WHITE)
                screen.blit(text, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))
            else:
                pygame.draw.rect(screen, WHITE, rect)  # Empty space in white
            pygame.draw.rect(screen, BLACK, rect, 2)  # Draw grid lines
