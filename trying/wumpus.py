import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 4
CELL_SIZE = 100
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Colors for items
COLORS = {
    "A": BLUE,   # Agent
    "W": RED,    # Wumpus
    "P": BLACK,  # Pit
    "G": YELLOW, # Gold
    " ": WHITE   # Empty space
}

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wumpus World')

# Randomly place Wumpus, pits, and gold
def place_item(grid, item, count=1):
    for _ in range(count):
        while True:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if grid[x][y] == " ":
                grid[x][y] = item
                break

# Initialize the grid
grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
place_item(grid, "W", 1)  # Place 1 Wumpus
place_item(grid, "P", 3)  # Place 3 pits
place_item(grid, "G", 1)  # Place 1 gold

# Place the agent at the starting position (0,0)
agent_x, agent_y = 0, 0
grid[agent_x][agent_y] = "A"

# Helper to get neighbors of a cell
def get_neighbors(x, y, grid_size):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_size and 0 <= ny < grid_size:
            neighbors.append((nx, ny))
    return neighbors

# Display the grid using Pygame
def draw_grid():
    screen.fill(WHITE)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, COLORS[grid[x][y]], rect)
            pygame.draw.rect(screen, BLACK, rect, 2)  # Grid lines

# Display the message when game ends
def display_message(message):
    font = pygame.font.SysFont(None, 48)
    text = font.render(message, True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(2000)

# Game loop for user input and movement
def game_loop():
    global agent_x, agent_y

    # Game loop
    running = True
    while running:
        draw_grid()
        
        # Check for events (key presses)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and agent_x > 0:
                    agent_x -= 1
                elif event.key == pygame.K_DOWN and agent_x < GRID_SIZE - 1:
                    agent_x += 1
                elif event.key == pygame.K_LEFT and agent_y > 0:
                    agent_y -= 1
                elif event.key == pygame.K_RIGHT and agent_y < GRID_SIZE - 1:
                    agent_y += 1

        # Check for win or loss conditions
        if grid[agent_x][agent_y] == "G":
            display_message("You found the gold! You win!")
            running = False
        elif grid[agent_x][agent_y] == "P":
            display_message("You fell into a pit! Game over.")
            running = False
        elif grid[agent_x][agent_y] == "W":
            display_message("You encountered the Wumpus! Game over.")
            running = False

        # Place agent on the grid
        grid[agent_x][agent_y] = "A"
        pygame.display.update()

    pygame.quit()

# Run the game
game_loop()
