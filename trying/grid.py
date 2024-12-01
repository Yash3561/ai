import pygame
from config import GRID_SIZE, wumpus_position, pit_position, glitter_position

# Grid layout with initial objects (empty, Wumpus, Gold, Pit)
grid = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Ensure (0, 0) is always safe
if (0, 0) in wumpus_position:
    wumpus_position.remove((0, 0))
if (0, 0) in pit_position:
    pit_position.remove((0, 0))
if glitter_position == (0, 0):
    glitter_position = None  # Reset gold placement if at (0, 0)

# Populate the grid with Wumpus positions
for (x, y) in wumpus_position:
    grid[x][y] = "W"  # Wumpus

# Populate the grid with Pit positions
for (x, y) in pit_position:
    grid[x][y] = "P"  # Pit

# Adjust Gold position to ensure it's not adjacent to (0, 0)
if glitter_position:
    gold_x, gold_y = glitter_position
    if abs(gold_x - 0) + abs(gold_y - 0) <= 1:  # Adjacent to (0, 0)
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                # Find a valid position far from (0, 0) and not on a Wumpus or Pit
                if grid[x][y] == "" and abs(x - 0) + abs(y - 0) > 1:
                    glitter_position = (x, y)
                    grid[x][y] = "G"  # Place Gold
                    break
    else:
        grid[gold_x][gold_y] = "G"  # Place Gold if not adjacent
else:
    # If gold position was reset, dynamically place gold
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == "" and abs(x - 0) + abs(y - 0) > 1:
                glitter_position = (x, y)
                grid[x][y] = "G"
                break

# Draw the grid
def draw_grid(screen, agent_position, font, path=[]):
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
    LIGHT_BLUE = (173, 216, 230)  # Light blue to highlight path

    screen.fill(BLACK)

    # Draw the grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            # Highlight path in light blue
            if (row, col) in path:
                pygame.draw.rect(screen, LIGHT_BLUE, rect)  # Highlight path in light blue
            
            # Draw agent position in blue
            if (row, col) == agent_position:
                pygame.draw.rect(screen, BLUE, rect)  # Draw agent position in blue
                text = font.render("A", True, WHITE)
                screen.blit(text, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))
            # Draw Wumpus in red
            elif grid[row][col] == "W":
                pygame.draw.rect(screen, RED, rect)  # Wumpus in red
                text = font.render("W", True, WHITE)
                screen.blit(text, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))
            # Draw Glitter in yellow
            elif grid[row][col] == "G":
                pygame.draw.rect(screen, YELLOW, rect)  # Glitter in yellow
                text = font.render("G", True, WHITE)
                screen.blit(text, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))
            # Draw Pit in green
            elif grid[row][col] == "P":
                pygame.draw.rect(screen, GREEN, rect)  # Pit in green
                text = font.render("P", True, WHITE)
                screen.blit(text, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))
            else:
                pygame.draw.rect(screen, WHITE, rect)  # Empty space in white
            
            # Draw grid lines
            pygame.draw.rect(screen, BLACK, rect, 2)  

    pygame.display.update()  # Update the display
    
def generate_fol_sentences(grid):
    """Generates FOL sentences from the given Wumpus World grid."""
    rows, cols = len(grid), len(grid[0])
    fol_sentences = []

    # # Header to link the grid to FOL output
    fol_sentences.append("\n\n### FOL Representation for the Generated Grid ###\n")
    # fol_sentences.append("Grid Representation:")
    # for row in grid:
    #     fol_sentences.append(" ".join(row))

    fol_sentences.append("\n### Facts ###")

    # Facts: Add contents of each cell
    for x in range(rows):
        for y in range(cols):
            cell = grid[x][y]
            if cell == 'W':
                fol_sentences.append(f"\n - Wumpus({x}, {y})")
            elif cell == 'P':
                fol_sentences.append(f"\n - Pit({x}, {y})")
            elif cell == 'G':
                fol_sentences.append(f"\n - Gold({x}, {y})")
            elif cell == 'A':
                fol_sentences.append(f"\n - Agent({x}, {y})")
    print("\n\n - THE REST OF CELLS ARE SAFE CELLS.")

    fol_sentences.append("\n### Rules ###")
    # Rules: Perceptions based on adjacency
    for x in range(rows):
        for y in range(cols):
            neighbors = [
                (x-1, y), (x+1, y), (x, y-1), (x, y+1)  # Up, Down, Left, Right
            ]
            valid_neighbors = [
                (nx, ny) for nx, ny in neighbors if 0 <= nx < rows and 0 <= ny < cols
            ]

            # Breeze rule
            if valid_neighbors:
                breeze_rule = f"\n- Breeze({x}, {y}) ⇔ " + " ∨ ".join(
                    [f"- Pit({nx}, {ny})" for nx, ny in valid_neighbors]
                )
                fol_sentences.append(breeze_rule)

            # Stench rule
            if valid_neighbors:
                stench_rule = f"\n- Stench({x}, {y}) ⇔ " + " ∨ ".join(
                    [f"- Wumpus({nx}, {ny})" for nx, ny in valid_neighbors]
                )
                fol_sentences.append(stench_rule)

    # Safety rule
    fol_sentences.append("\n### Safety Constraints ###")
    for x in range(rows):
        for y in range(cols):
            fol_sentences.append(f"\n- Safe({x}, {y}) ⇔ ¬Pit({x}, {y}) ∧ ¬Wumpus({x}, {y})")

    return fol_sentences
