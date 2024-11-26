import pygame
import random
import time

# Pygame initialization
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_SIZE = 4
CELL_SIZE = 150
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Colors for different game elements
AGENT_COLOR = BLUE
WUMPUS_COLOR = RED
PIT_COLOR = GRAY
GOLD_COLOR = YELLOW

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wumpus World")

# Font for text
font = pygame.font.SysFont("Arial", 24)

# Grid setup and items
grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
agent_x, agent_y = 0, 0

def draw_grid():
    """Draws the grid and the objects in it."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 3)
            if grid[row][col] == "A":  # Agent
                pygame.draw.rect(screen, AGENT_COLOR, rect)
                pygame.draw.line(screen, BLACK, rect.center, rect.center)
                screen.blit(font.render('A', True, BLACK), rect.center)
            elif grid[row][col] == "W":  # Wumpus
                pygame.draw.rect(screen, WUMPUS_COLOR, rect)
                screen.blit(font.render('W', True, BLACK), rect.center)
            elif grid[row][col] == "P":  # Pit
                pygame.draw.rect(screen, PIT_COLOR, rect)
                screen.blit(font.render('P', True, BLACK), rect.center)
            elif grid[row][col] == "G":  # Gold
                pygame.draw.rect(screen, GOLD_COLOR, rect)
                screen.blit(font.render('G', True, BLACK), rect.center)

def show_text(text, y_offset):
    """Displays text on the screen."""
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (20, y_offset))

# Function to place items randomly on the grid
def place_item(item, count=1):
    """Places items randomly in the grid."""
    for _ in range(count):
        while True:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if grid[x][y] == " ":
                grid[x][y] = item
                break

# Set up initial grid (place items randomly)
def setup_grid():
    """Setup the game grid with items."""
    global agent_x, agent_y
    grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    place_item("W", 1)  # Place Wumpus
    place_item("P", 3)  # Place Pits
    place_item("G", 1)  # Place Gold
    grid[0][0] = "A"  # Agent starts at (0,0)
    agent_x, agent_y = 0, 0

# Main Menu screen
def main_menu():
    """Display the main menu."""
    running = True
    while running:
        screen.fill(WHITE)
        show_text("Welcome to Wumpus World!", 100)
        show_text("Press 1 to Play with AI", 200)
        show_text("Press 2 to Play Manually", 250)
        show_text("Press Q to Quit", 300)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play_game(True)  # AI mode
                    running = False
                elif event.key == pygame.K_2:
                    play_game(False)  # Manual mode
                    running = False
                elif event.key == pygame.K_q:
                    running = False

# Game loop
def play_game(is_ai):
    """The main game loop."""
    setup_grid()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Draw the grid and update screen
        screen.fill(WHITE)
        draw_grid()
        
        # Display different messages based on the mode
        if is_ai:
            show_text("AI Mode: Searching for the Gold...", 500)
            # AI movement logic will be added here later
        else:
            show_text("Manual Mode: Use Arrow keys to move!", 500)
        
        pygame.display.update()

        if not is_ai:
            handle_manual_movement()  # Handle manual movement
        
        time.sleep(0.2)  # Control game speed

# Manual movement handling
def handle_manual_movement():
    """Handles user movement input for manual play."""
    global agent_x, agent_y
    keys = pygame.key.get_pressed()

    # Handle movement with arrow keys
    if keys[pygame.K_UP] and agent_x > 0:
        agent_x -= 1
    elif keys[pygame.K_DOWN] and agent_x < GRID_SIZE - 1:
        agent_x += 1
    elif keys[pygame.K_LEFT] and agent_y > 0:
        agent_y -= 1
    elif keys[pygame.K_RIGHT] and agent_y < GRID_SIZE - 1:
        agent_y += 1

    # Update grid with new agent position
    grid[agent_x][agent_y] = "A"

# Start game by showing the main menu
main_menu()

pygame.quit()
