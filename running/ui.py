import pygame
from grid import GRID_SIZE, grid

# Set up the display
def init_ui():
    pygame.init()
    window = pygame.display.set_mode((400, 400))
    pygame.display.set_caption('Wumpus World')
    return window

def draw_grid(window):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            pygame.draw.rect(window, (255, 255, 255), (i * 100, j * 100, 100, 100), 2)
            
            # Draw agent, Wumpus, pits, gold, etc.
            if grid[i][j] == 'A':
                pygame.draw.circle(window, (0, 255, 0), (i * 100 + 50, j * 100 + 50), 30)  # Agent (green)
            elif grid[i][j] == 'W':
                pygame.draw.circle(window, (255, 0, 0), (i * 100 + 50, j * 100 + 50), 30)  # Wumpus (red)
            elif grid[i][j] == 'P':
                pygame.draw.circle(window, (0, 0, 255), (i * 100 + 50, j * 100 + 50), 30)  # Pit (blue)
            elif grid[i][j] == 'G':
                pygame.draw.circle(window, (255, 255, 0), (i * 100 + 50, j * 100 + 50), 30)  # Gold (yellow)

def update_ui(window):
    pygame.display.update()
